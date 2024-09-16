""" This script downloads datasets that are easily retrievable and places them in the data/landing directory """

# import necessary libraries and functions
import os
import zipfile
import urllib.request


output_dir = "./data/landing"

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
urllib.request.urlretrieve(SA2_BORDERS_LINK, local_zip_path) 
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
urllib.request.urlretrieve(HISTORICAL_RENTAL_LINK, local_output_dir) 

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

    
# SECTION: download the train station data - (METROPOLITIAN STATIONS)

# output directories
local_output_dir = f"{output_dir}/Annual_Metropolitan_Train_Station_Entries_2023-24.csv"

# URL for train station data
BASE_URL = "https://vicroadsopendatastorehouse.vicroads.vic.gov.au/"
DOWNLOAD_PATH = "opendata/Public_Transport/Patronage/Annual_metropolitan_train_station_entries/"
FILE_NAME = "Annual_Metropolitan_Train_Station_Entries_2023-24.csv"
TRAIN_LINK = BASE_URL + DOWNLOAD_PATH + FILE_NAME

# retrieve train station data
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(TRAIN_LINK, headers=headers)
with urllib.request.urlopen(req) as response:
    with open(local_output_dir, 'wb') as f:
        f.write(response.read())

print("Train Stations in VIC Data Download Complete")

# SECTION: download Crime records in Victoria data

# output directory
local_output_dir = f"{output_dir}/LGA_Criminal_Incidents_Year_Ending_March.csv"

# URL for crime data
BASE_URL = "https://files.crimestatistics.vic.gov.au/"
DOWNLOAD_PATH = "2024-06/"
FILE_NAME = "Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.xlsx"
CRIME_RECORDS_LINK = BASE_URL + DOWNLOAD_PATH + FILE_NAME

# retrieve historical rental data
urllib.request.urlretrieve(CRIME_RECORDS_LINK, local_output_dir) 

print("Crime Data Download Complete")
#https://files.crimestatistics.vic.gov.au/2024-06/Data_Tables_LGA_Criminal_Incidents_Year_Ending_March_2024.xlsx
