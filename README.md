# Real Estate Consulting Project

### Group 8

## Team members:

- Jayden Thai
- Zac Pathak
- Dong Li
- Joshua Li
- Muhammad Harith Kamil

## Research Goal

Aim: To deliver insights on rental properties in the suburbs of Victoria for consulting an online real estate company.

Primary Objectives:

- Forecast Rental Prices in Victorian Suburbs
- Determine the Most Important Features in Predicting Rent Prices
- Forecast Top 10 Suburbs with Highest Projected Growth
- Calculate the Most Liveable and Affordable Suburbs

## Datasets:

Tourism Data:

- File: tourism.xlsx
- Source: TRA - State Tourism Satellite Accounts 2022-23.

Coastline Data:

- Files extracted from coastline.zip in the coastline folder.
- Source: Australian coastline data in shapefile format.

Historical Rental Data:

- File: moving-annual-rent-suburb-march-quarter-2024.xlsx
- Source: Department of Families, Fairness and Housing - Rental data for Victoria.

ABS Census Data:

- Various files in 2016_GCP_SSC, 2021_GCP_SAL, 2021_GCP_SA2, and 2016_GCP_SA2 folders.
- Source: ABS Census data for specific years and geographic classifications.

LGA Correspondences:

- File: CG_SSC_2016_SAL_2021.csv
- Source: ABS - Correspondence between SSC 2016 and SAL 2021.

Train Station Patronage Data:

- File: Annual_Metropolitan_Train_Station_Entries_2023-24.csv
- Source: VicRoads - Train station entry data (metropolitan).

- File: PTV_REGIONAL_TRAIN_STATION.shp
- Source: DataShare vic.gov - Train station entry data (regional).

Crime Records in Victoria:

- File: LGA_Criminal_Incidents_Year_Ending_March.csv
- Source: Crime Statistics Agency Victoria - Criminal incidents by LGA.

Open Space Data:

- Files extracted from da1c06e3ab6948fcb56de4bb3c722449_0.zip in the Open_Space folder.
- Source: Open Data ArcGIS - Open space shapefile data.

Suburbs and Locations (SAL) Data:

- Files extracted from SAL_2021_AUST_GDA2020_SHP.zip in the SAL_data folder.
- Source: ABS - SAL digital boundary files.

Population Projections:

- File: VIF2023_SA2_Pop_Hhold_Dwelling_Projections_to_2036_Release_2.xlsx
- Source: Victoria in Future (VIF) 2023 projections.

Business Listings:

- File: business_listing.csv
- Source: City of Melbourne - Business establishments with address and industry classification.

ANZSCIC Classification Data:

- File: anzsic-groups.csv
- Source: ABS - Australian and New Zealand Standard Industrial Classification (ANZSIC).

Victorian Schooling Data:

- File: school_data.csv
- Source: aroundschools.com

Airbnb Data:

- File: listing.csv
- Source: Inside airbnb

SA2 Borders (Australia):

- Files extracted from SA2_2021_AUST_SHP_GDA2020.zip in the SA2_2021_map folder. (unable to be implemented into analysis - see the summary notebook)
- Source: Australian Bureau of Statistics (ABS) - Digital boundary files for SA2 borders.

Domain Rental Data:

- File: property_metadata.json (unable to be implemented into analysis - see the summary notebook)
- Source: Domain.com

Internet Speed Tests:

- File: {year}\_fixed_broadband.csv, where year is the variable representing the year, year can take the values 2016, 2017, 2018, or 2019 (unable to be implemented into analysis - see the summary notebook)
- Source: ookla-open-data

Inflation Data:

- File: No file used (there was not a lot of data collected here so it was consequently hard coded into `Data_merging` notebook)
- Source: ABS for 2014-2024 & Statista forecasts (2025-2028)

## Project Pipeline:

### Summary of the Project

Running the pipeline requires following a lot of steps as outlined below. To understand
For a summary of our approach and key findings of the project, please read and run our notebook `Summary_Notebook`. This gives a high level summary of the pipeline along with limitations and assumptions made at every stage.

### How to Run the Pipeline

0. Run the `requirements.txt` to install all the necessary libraries
1. Run the `download_datasets` in `scripts` to get the following data:
   - Tourism
   - Coastline Data
   - SA2 Borders (Australia)
   - Historical Rental Data
   - ABS Census Data
   - LGA Correspondences
   - Train Station Patronage Data
   - Crime Records in Victoria
   - Open Space Data
   - Suburbs and Locations (SAL) Data
   - Population Projections
   - Business Listings
   - ANZSCIC Classification Data
2. (Optional) Run the `domain_com_scrape.py` in `scripts` to scrape data from _domain.com.au_ \[This takes 5 hours to run and is not actively employed\]
3. Run the `school_scraper` and then `location_scraper` both in `scripts` to get location coordinates of schools and other school related data.
4. Run in order and follow instructions inside the notebooks of these folders from `notebooks`:
   - ABS_data_preprocessing
     1. ABS_data_preprocessing
     2. ABS_ARIMA_interpolation
   - Crime_preprocessing
     1. crime_records_preprocessing
     2. crime_ARIMA
   - School_preprocessing
     1. school_data_preprocessing
   - Proximity_data_preprocessing
     1. proximity_preprocessing_1
     2. proximity_preprocessing_2
   - insideAirbnb_preprocessing
     1. processing
   - Tourism_preprocessing
     1. tourism
   - Population_projections
     1. population_preprocessing
   - OSM_preprocessing
     1. preprocessing
   - Open_Space_preprocessing
     1. Open_Space_preprocessing
   - Historical_rent_preprocessing
     1. historical_rent_preprocessing
   - Domain_preprocessing
     1. preprocessing_suburb
   - Speedtest_preprocessing (this section is optional to run, for the same reason as domain data)
     1. ookla
   - Coast_preprocessing
     1. coast
   - Business_Listing
     1. business_listing_preprocessing
     2. business_ARIMA
5. To merge all the data run `Data_merging`
6. Run `transformations` in `notebooks` to perform final feature engineering and data transformations
7. Run `Preliminary_analysis` in `notebooks`
8. Run `Graphs` in `notebooks`
9. Run `Final_Modelling` in `models`
10. Run `predictions` in `models`
11. Run `predictions_adjusted` in `models`
12. Run both `affordabilitiy` and `liveability` in `Livability_and_Affordability` in `notebooks` to retrieve affordability liveability scores of suburbs

# Additional Notes

### Google Drive

You can find all the datasets in a google drive at this link ['https://drive.google.com/drive/folders/1GIqOVAzaCzuQMXGhnxioaJINnMQO8qPm']. We supply this drive as can take too long to run the scrapers or as a back up in case any unexpected issues come up when running notebooks in the project pipeline. Please note that this google drive can only be accessed via a unimelb email account.

### Scrap Work & Notes

Our project contains a lot of scrap workings and notebooks, all of these files are contained in the folder `Scrap_Notebooks_and_Scripts` in `notebooks`. These are not necessary to run the pipeline or understand findings of the project but are supplied in the repository for any interested readers.
