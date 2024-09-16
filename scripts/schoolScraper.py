
import os
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from geopy.geocoders import Nominatim
import pandas as pd
import time

# Set up the Chrome WebDriver
driver = webdriver.Chrome()
url = 'https://www.aroundschools.com.au/schools/search/?search=state:%22VIC%22'
driver.get(url)

output_folder = "data/raw"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Wait for the school elements to load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'SchoolListRow__StyledSchoolListRow')]"))
)



def click_load_more_button(driver):
    while True:
        try:
            # Wait until the "Load More" button is clickable
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Load more schools')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            # Click the button
            load_more_button.click()

        except TimeoutException:
            print("No more 'Load More' buttons found or timed out.")
            break
        except NoSuchElementException:
            print("No more 'Load More' buttons found.")
            break


def load_all_schools(driver):
    # Click the "Load More" button until all schools are loaded
    click_load_more_button(driver)

    # Find all school elements
    schools = driver.find_elements(By.XPATH, "//a[contains(@class, 'SchoolListRow__StyledSchoolListRow')]")
    print(f"Total schools found: {len(schools)}")

    # Get the list of schools
    # Create a DataFrame to store the scraped data
    school_df = pd.DataFrame(columns=['school_name', 'school_type', 'median_score', 'price_local'])

    for school in schools:
        # Store the href link of the school
        href = school.get_attribute('href')


        # List of elements to scrape
        elements = [
            ('school_name', ".//span[contains(@class, 'SchoolListRow__SchoolNameText')]"),
            ("school_type", ".//div[contains(@class, 'bnccCr')]"),  # Adjusted the class name
            ("median_score", ".//div[contains(@class, 'fYBuun')]"),  # Adjusted the class name
            ('price_local', ".//div[contains(@class, 'bnIkXu')]")  # Adjusted the class name
        ]

        new_row = {}

        # Loop through each element and extract the text
        for name, class_name in elements:
            try:
                element = school.find_element(By.XPATH, class_name)
                new_row[name] = element.get_property('textContent').strip()
            except NoSuchElementException:
                new_row[name] = None  # Handle missing elements
        
        # Find the parent container of the badges
        parent_element = driver.find_element(By.CLASS_NAME, "LevelBadge__StyledLevelBadge-sc-154evpz-0")

        # Find all badges within the parent container
        badges = parent_element.find_elements(By.CLASS_NAME, "LevelBadge__BadgeSelector-sc-154evpz-1")

        # Loop through each badge and determine its active/inactive state
        for badge in badges:
            class_name = badge.get_attribute('class')
            badge_text = badge.text.strip()  # Get the text of the badge
            
            # Check if the badge is active based on the specific class name
            new_row[badge_text] = "eKkJfT" in class_name  # Active if "eKkJfT", otherwise inactive

                
        # Add the href to the row
        new_row['href'] = href

        # Append the new row to the DataFrame
        school_df = pd.concat([pd.DataFrame([new_row], dtype=object), school_df], ignore_index=True)
        print(f"Added: {new_row['school_name']}")


    
    return school_df


from selenium.common.exceptions import TimeoutException

school_df = load_all_schools(driver)

school_df.to_csv('data/raw/school_data.csv', index=False)


driver.quit()