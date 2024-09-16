import pandas as pd

from concurrent.futures import ThreadPoolExecutor, as_completed

from playwright.sync_api import sync_playwright

# Load school data
school_df = pd.read_csv('school_data.csv')

# Function to get coordinates for a single school
def get_coordinates_for_school(school, i):
    lat, lon = None, None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Launch browser in headless mode
            page = browser.new_page()

            page.goto(school, timeout=10000)  # Navigate to the school URL

            # Wait for the "Directions" link with a maximum wait time of 5 seconds
            try:
                direction_link = page.wait_for_selector("a[title='Get directions in Google Map']", timeout=5000)

                # Extract the href attribute containing the coordinates
                href = direction_link.get_attribute('href')
                
                # Parse out latitude and longitude
                if 'daddr=' in href:
                    coords = href.split('daddr=')[1]
                    lat, lon = coords.split(',')
                    print(f"School {i}: Latitude: {lat:<10}, Longitude: {lon:<10}")
                else:
                    print(f"Coordinates not found for school {i}")

            except Exception:
                print(f"Directions link not found for school {i}")

            # Close the browser for this school
            browser.close()

    except Exception as e:
        print(f"An error occurred for school {i}: {e}")
    
    # Return the lat, lon, and index for updating DataFrame later
    return i, lat, lon

# Function to run the multi-threaded scraping using Playwright
def get_coordinates_multi_thread(school_df):

    # Using ThreadPoolExecutor to process multiple schools concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit tasks to executor for each school
        futures = [executor.submit(get_coordinates_for_school, school, i) for i, school in enumerate(school_df['href'])]

        # As futures complete, get the results and update the DataFrame
        for future in as_completed(futures):
            i, lat, lon = future.result()  # Get the result of each future
            school_df.loc[school_df.index == i, 'latitude'] = lat
            school_df.loc[school_df.index == i, 'longitude'] = lon

    return school_df

# Function to run the multi-threaded scraping using Playwright for missing values
def get_coordinates_for_null_entries(school_df):
    # Identify rows where latitude or longitude is null
    null_entries = school_df[school_df['latitude'].isnull() | school_df['longitude'].isnull()]

    # Using ThreadPoolExecutor to process multiple schools concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit tasks to executor for each school with missing coordinates
        futures = [executor.submit(get_coordinates_for_school, row['href'], idx) for idx, row in null_entries.iterrows()]

        # As futures complete, get the results and update the DataFrame
        for future in as_completed(futures):
            i, lat, lon = future.result()  # Get the result of each future
            school_df.loc[school_df.index == i, 'latitude'] = lat
            school_df.loc[school_df.index == i, 'longitude'] = lon

    return school_df

# Run the multi-threaded function for rows with missing latitude or longitude
school_df = get_coordinates_for_null_entries(school_df)

# Save the updated results back to CSV
school_df.to_csv('school_data.csv', index=False)

# Run the multi-threaded function
school_df = get_coordinates_multi_thread(school_df)
school_df = get_coordinates_for_null_entries(school_df)

# Save the results back to CSV
school_df.to_csv('school_data.csv', index=False)
