""" This script downloads datasets that are easily retrievable and places them in the data/raw directory """

# import necessary libraries and functions
import os
from urllib.request import urlretrieve
import zipfile


output_dir = "./data/raw"

# Make sure the directory exists
os.makedirs(output_dir, exist_ok=True)

# SECTION: download the shp file of SA2 borders in Australia

# Base URL for ABS statistics
BASE_URL = "https://www.abs.gov.au/statistics/standards/"
# Path to the ASGS edition and time period
ASGS_VERSION = "australian-statistical-geography-standard-asgs-edition-3/"
TIME_PERIOD = "jul2021-jun2026/"
# Path to the download files and the specific file name
DOWNLOAD_PATH = "access-and-downloads/digital-boundary-files/"
FILE_NAME = "SA2_2021_AUST_SHP_GDA2020.zip"

# Complete URL for the SA2 borders digital boundary file
SA2_BORDERS_LINK = BASE_URL + ASGS_VERSION + TIME_PERIOD + DOWNLOAD_PATH + FILE_NAME

# output directories
local_zip_path = f"{output_dir}/{FILE_NAME}"
local_output_dir = f"{output_dir}/SA2_2021_map"

# download the zip file for the SA2 borders and extract the contents of the zip file
urlretrieve(SA2_BORDERS_LINK, local_zip_path) 
with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
   zip_ref.extractall(local_output_dir)

# delete orginal zip file  
os.remove(local_zip_path)

print("SA2 Borders Download Complete")



# SECTION: download the historical rental data

# output directories
local_output_dir = f"{output_dir}/moving-annual-rent-suburb-march-quarter-2024.xlsx"

# URL for historical rental data
BASE_URL = "https://www.dffh.vic.gov.au/"
FILE_NAME = "moving-annual-rent-suburb-march-quarter-2024-excel"
HISTORICAL_RENTAL_LINK = BASE_URL + FILE_NAME

# retrieve historical rental data
urlretrieve(HISTORICAL_RENTAL_LINK, local_output_dir) 

print("Historical Rental Data Download Complete")


# SECTION: download the ABS data
years = [2016, 2021]
BASE_URL = "https://www.abs.gov.au/census/find-census-data/datapacks/download/"

for year in years:
    # URL for the ABS data
    FILE_NAME = f"{year}_GCP_SA2_for_VIC_short-header.zip"
    ABS_DATA_LINK = BASE_URL + FILE_NAME

    # output directories
    local_zip_path = f"{output_dir}/{FILE_NAME}"
    local_output_dir = f"{output_dir}/{year}_GCP_SA2_for_VIC_short-header"

    # retrieve the ABS data
    urlretrieve(ABS_DATA_LINK, local_zip_path) 
    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        zip_ref.extractall(local_output_dir)

    # delete orginal zip file  
    os.remove(local_zip_path)