import re
import json
import logging
import os
import time
import random
from tqdm import tqdm
from collections import defaultdict
import urllib.request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import IncompleteRead, HTTPException
from threading import Lock

# Configure logging to output to both file and console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
metadata_lock = Lock()

# constants
BASE_URL = "https://www.domain.com.au"
MAX_WORKERS = 28  # Number of concurrent threads
MAX_RETRIES = 3  # Maximum retries for failed requests
BATCH_SIZE = 5000  # Process URLs in batches
SAVE_INTERVAL = 1000  # Save progress after every 1000 records

# output folder
output_folder = "data/raw"
output_file = os.path.join(output_folder, "property_metadata.json")
urls_output_file = os.path.join(output_folder, "fetched_urls.json")

# create the folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to add a random delay
def random_delay():
    time.sleep(random.uniform(1, 2))  # Random delay between 1 to 1.5 seconds

def is_error_page(bs_object):
    """Determine if the page is an error page or has no results."""
    error_message = bs_object.find("h1", {"data-testid": "error-page__message-header"})
    if error_message and "Oops..." in error_message.text:
        return True

    no_matches_element = bs_object.find("h3", {"class": "css-1c8ubmt"})
    if no_matches_element and no_matches_element.get_text() == "No exact matches":
        return True

    return False

# Load the suburbs JSON file
input_filename = 'data/raw/vic_suburbs.json'

with open(input_filename, 'r') as file:
    suburb_data = json.load(file)

suburb_postcodes = list(suburb_data.keys())

url_links = []
property_metadata = defaultdict(dict)

# Generate list of URLs to visit
def fetch_links(suburb_postcode, seen_urls):
    page = 1
    local_url_links = []

    while True:
        retries = 0  # Retry counter is reset for each page
        
        while retries < MAX_RETRIES:  # Retry loop for each page
            url = f"{BASE_URL}/rent/{suburb_postcode}/?sort=suburb-asc&page={page}"
            logger.info(f"Visiting {url}")

            try:
                response = urlopen(Request(url, headers={'User-Agent': "PostmanRuntime/7.6.0"}), timeout=30)
                bs_object = BeautifulSoup(response, "lxml")

                if is_error_page(bs_object):
                    logger.info(f"No results found for {url}. Stopping at page {page}.")
                    return local_url_links  # Return the links fetched so far (if any)

                index_links = bs_object \
                    .find("ul", {"data-testid": "results"}) \
                    .findAll("a", href=re.compile(f"{BASE_URL}/*"))

                for link in index_links:
                    if 'address' in link.get('class', []):
                        href = link['href']
                        # Add only unseen URLs to the list
                        if href not in seen_urls:
                            local_url_links.append(href)
                            seen_urls.add(href)

                random_delay()
                page += 1
                break  # Exit the retry loop if the request is successful

            except (HTTPError, URLError, IncompleteRead, HTTPException, ValueError) as e:
                retries += 1
                logger.error(f"Error fetching {url}: {e}. Retrying... {retries}/{MAX_RETRIES}")
                if retries >= MAX_RETRIES:
                    logger.error(f"Failed to fetch {url} after {MAX_RETRIES} retries. Moving to the next page.")
                    return local_url_links  # Return the links fetched so far (if any)
    
    return local_url_links

# Export URLs to a file after fetching
def export_fetched_urls(fetched_urls):
    try:
        with open(urls_output_file, 'w') as file:
            json.dump(fetched_urls, file, indent=4)
        logger.info(f"Fetched URLs exported to {urls_output_file}")
    except Exception as e:
        logger.error(f"Error exporting URLs: {e}")

# Load URLs from a JSON file
def load_urls_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading URLs from {file_path}: {e}")
        return []

# Batch process the URLs and write to file incrementally
def process_in_batches(all_urls):
    for batch_start in range(0, len(all_urls), BATCH_SIZE):
        batch_urls = all_urls[batch_start:batch_start + BATCH_SIZE]
        logger.info(f"Processing batch {batch_start // BATCH_SIZE + 1} with {len(batch_urls)} URLs.")
        
        # Fetch metadata for the current batch
        fetch_metadata_batch(batch_urls)
        
        # Write intermediate results to file
        save_metadata_to_disk()

# Function to fetch metadata for a batch of URLs
def fetch_metadata_batch(batch_urls):
    global property_metadata
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_metadata, url) for url in batch_urls]

        # Use tqdm with write lock to keep the progress bar clean at the bottom
        with tqdm(total=len(futures), desc="Fetching metadata", position=0, leave=True) as pbar:
            for future in as_completed(futures):
                try:
                    url, metadata = future.result()
                    if metadata:
                        # Acquire lock before modifying shared data
                        with metadata_lock:
                            property_metadata[url] = metadata
                except Exception as e:
                    logger.error(f"Error in fetching metadata: {e}")
                pbar.update(1)

# Function to fetch metadata for a single URL
def fetch_metadata(property_url):
    logger.info(f"Fetching metadata for {property_url}")
    try:
        bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent': "PostmanRuntime/7.6.0"}), timeout=30), "lxml")

        property_data = {}

        # Property name
        property_data['name'] = bs_object.find("h1", {"class": "css-164r41r"}).text

        # Property cost
        property_data['cost_text'] = bs_object.find("div", {"data-testid": "listing-details__summary-title"}).text

        # Rooms and parking
        rooms = bs_object.find("div", {"data-testid": "property-features"}) \
            .findAll("span", {"data-testid": "property-features-text-container"})

        property_data['rooms'] = [
            re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Bed' in feature.text or 'Bath' in feature.text
        ]
        property_data['parking'] = [
            re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Parking' in feature.text
        ]

        property_data['desc'] = re.sub(r'<br\/>', '\n', str(bs_object.find("p"))).strip('</p>')

        return property_url, property_data

    except AttributeError as e:
        logger.error(f"Issue fetching metadata for {property_url}: {e}")
        return property_url, {}

# Function to save the current metadata to disk
def save_metadata_to_disk():
    global property_metadata
    if os.path.exists(output_file):
        with open(output_file, 'r') as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = {}
            # Update the existing data with new batch
            existing_data.update(property_metadata)
    else:
        existing_data = property_metadata

    with open(output_file, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
    
    logger.info(f"Data successfully exported to {output_file}")

# Main logic to fetch URLs and process in batches
if __name__ == "__main__":
    if os.path.exists(urls_output_file):
        # If URLs have already been fetched, load them and fetch metadata
        url_links = load_urls_from_json(urls_output_file)
        logger.info(f"Loaded {len(url_links)} URLs from {urls_output_file}")

        # Process URLs in batches to prevent memory overload
        process_in_batches(url_links)

        # Final save in case anything remains
        save_metadata_to_disk()

    else:
        seen_urls = set()  # Initialize the set of seen URLs
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(fetch_links, postcode, seen_urls) for postcode in suburb_postcodes]

            # Use tqdm with write lock to keep the progress bar clean at the bottom
            with tqdm(total=len(futures), desc="Fetching links", position=0, leave=True) as pbar:
                for future in as_completed(futures):
                    try:
                        url_links.extend(future.result())
                    except Exception as e:
                        logger.error(f"Error in fetching links: {e}")
                    pbar.update(1)

        # Export the fetched URLs to a file
        export_fetched_urls(url_links)

        # Process URLs in batches to prevent memory overload
        process_in_batches(url_links)

        # Final save in case anything remains
        save_metadata_to_disk()