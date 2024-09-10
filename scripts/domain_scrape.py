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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# constants
BASE_URL = "https://www.domain.com.au"

# output folder
output_folder = "data/raw"
output_file = os.path.join(output_folder, "property_metadata.json")

# create the folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to add a random delay if needed
def random_delay():
    time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds

# Function to check if there are no more pages
def is_error_page(bs_object):
    error_message = bs_object.find("h1", {"data-testid": "error-page__message-header"})
    return error_message is not None and "Oops..." in error_message.text

# Begin code
url_links = []
property_metadata = defaultdict(dict)
page = 1

# Generate list of urls to visit
while True:
    url = f"{BASE_URL}/rent/?sort=suburb-asc&state=vic&page={page}"
    logging.info(f"Visiting {url}")

    # find the unordered list (ul) elements which are the results, then
    # find all href (a) tags that are from the base_url website.
    try:        
        bs_object = BeautifulSoup(urlopen(Request(url, headers={'User-Agent': "PostmanRuntime/7.6.0"})), "lxml")

        # Check if we have hit the error page meaning there are no more pages
        if is_error_page(bs_object):
            logging.info(f"Reached a page with no results. Stopping at page {page}.")
            break

        # find the unordered list (ul) elements which are the results, then
        # find all href (a) tags that are from the base_url website.
        index_links = bs_object \
            .find("ul", {"data-testid": "results"}) \
            .findAll("a", href=re.compile(f"{BASE_URL}/*"))

        for link in index_links:
            if 'address' in link.get('class', []):
                url_links.append(link['href'])
                        
        # Uncomment this to introduce delay to avoid getting banned
        # random_delay()

        page += 1

    except (HTTPError, URLError) as e:
        logging.error(f"Error fetching {url}: {e}")
        break

# for each url, scrape some basic metadata
pbar = tqdm(url_links[1:])
success_count, total_count = 0, 0
for property_url in pbar:
    try:
        bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
        total_count += 1

        # looks for the header class to get property name
        property_metadata[property_url]['name'] = bs_object \
            .find("h1", {"class": "css-164r41r"}) \
            .text

        # looks for the div containing a summary title for cost
        property_metadata[property_url]['cost_text'] = bs_object \
            .find("div", {"data-testid": "listing-details__summary-title"}) \
            .text

        # get rooms and parking
        rooms = bs_object \
            .find("div", {"data-testid": "property-features"}) \
            .findAll("span", {"data-testid": "property-features-text-container"})

        # rooms
        property_metadata[property_url]['rooms'] = [
            re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Bed' in feature.text or 'Bath' in feature.text
        ]
        # parking
        property_metadata[property_url]['parking'] = [
            re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
            if 'Parking' in feature.text
        ]

        property_metadata[property_url]['desc'] = re \
            .sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
            .strip('</p>')
        success_count += 1

    except AttributeError:
        logging.error(f"Issue with {property_url}")

    pbar.set_description(f"{(success_count/total_count * 100):.0f}% successful")
    # Uncomment to add random delay if needed
    # random_delay()


# export the property metadata to the 'data/raw' folder as a JSON file
with open(output_file, 'w') as json_file:
    json.dump(property_metadata, json_file, indent=4)

print(f"Data successfully exported to {output_file}")

