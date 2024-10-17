# Real Estate Consulting Project

### Group 8

## Team members:

* Jayden Thai
* Zac Pathak
* Dong Li
* Joshua Li
* Muhammad Harith Kamil

## Research Goal

Aim: To deliver insights on rental properties in the suburbs of Victoria for consulting an online real estate company.

Primary Objectives:

* Forecast Rental Prices in Victorian Suburbs
* Determine the Most Important Features in Predicting Rent Prices
* Forecast Top 10 Suburbs with Highest Projected Growth
* Calculate the Most Liveable and Affordable Suburbs

## Datasets:

• Rental properties dataset acquired from scraping *domain.com.au*

• Historical dataset acquired from "[https://www.dffh.vic.gov.au/publications/rental-report](https://www.dffh.vic.gov.au/publications/rental-report)"

• GDA2020 shapefile acquired from "[https://data.gov.au/dataset/ds-dga-bdf92691-c6fe-42b9-a0e2-a4cd716fa811/details](https://data.gov.au/dataset/ds-dga-bdf92691-c6fe-42b9-a0e2-a4cd716fa811/details)"

• PTV dataset for public transport "[https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/](https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/)"

• Open Street Map (OSM) dataset for groceries stores in Victoria region.

• Public hospital dataset "[https://data.gov.au/data/dataset/88a95824-c0e7-4ec0-bb78-b36223dd16a8/resource/43b9e4a4-0752-44c7-b825-bc32c46cf3b7/download/public_hospital_list.csv](https://data.gov.au/data/dataset/88a95824-c0e7-4ec0-bb78-b36223dd16a8/resource/43b9e4a4-0752-44c7-b825-bc32c46cf3b7/download/public_hospital_list.csv)"

• Population and Income data are acquired from *Australian Bureau of Statistics*

• Australian postcodes *[https://github.com/schappim/australian-postcodes/blob/master/australian-postcodes-2021-04-23.csv](https://github.com/schappim/australian-postcodes/blob/master/australian-postcodes-2021-04-23.csv)*

## Project Pipeline:

0. Run the `requirements.txt` to install all the necessary libraries
1. Run the `download_datasets` in `scripts` to get:

   Tourism Data:
   - File: tourism.xlsx
   - Source: TRA - State Tourism Satellite Accounts 2022-23.

   Coastline Data:
   - Files extracted from coastline.zip in the coastline folder.
   - Source: Australian coastline data in shapefile format.

   SA2 Borders (Australia):
   - Files extracted from SA2_2021_AUST_SHP_GDA2020.zip in the SA2_2021_map folder.
   - Source: Australian Bureau of Statistics (ABS) - Digital boundary files for SA2 borders.

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
   - Source: VicRoads - Train station entry data.

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
2. Run the `suburb_scraper` in `scripts` to get dataset for public hospital.
3. (Optional) Run the `domain_com_scrape.py` in `scripts` to scrape data from *domain.com.au* \[This takes 5 hours to run and is not actively employed\]
4. Run the `location_scraper` in `scripts` to get dataset for shop records.
5. Run in order and follow instructions for these folders from `notebooks`:
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
    - Speedtest_preprocessing
        1. ookla
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
    - Coast_preprocessing
        1. coast
    - Business_Listing
        1. business_listing_preprocessing
        2. business_ARIMA
6. To merge all the data run `Data_merging`
7. 

