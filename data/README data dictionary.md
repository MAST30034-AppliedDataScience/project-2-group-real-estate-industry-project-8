# Data Dictionary

The process for downloading and forming the dataset can be found in the main README.

The following dictionary is for the dataset used in our modelling and analysis. There was other data collected which was not utilised in this final dataset as it was deemed to be irrelevant or of poor quality such as internet speed test data or current domain.com.au data. The dataset separates each row by suburb and year. Years extending past 2024 uses values predicted using ARIMA.

## "Processed Data Final.csv" dataframe:

- **distance_to_CBD**: Distance between suburb centroid and the CBD centroid in metres (value has a log transform)
- **time_to_CBD**: Time between suburb centroid and CBD centroid when travelling by car in seconds (value has a log transform)
- **distance_to_station**: Distance between suburb centroid and the closest train station in metres (value has a log transform)
- **time_to_station**: Time between suburb centroid and the closest train station in seconds (value has a log transform)
- **year**: the year the values in the row correspond to
- **Average_household_size**: The number of people living in a household on average in the suburb (value has a log transform)
- **Average_num_psns_per_bedroom**: Average_household_size divided by average number of bedrooms of households in the suburb (value has a log transform)
- **Median_age_persons**: The median age in a suburb (value has a log transform)
- **Tot_P_P**: Total population of a suburb (value has a log transform)
- **SAL_CODE**: The SAL code of a suburb defined by the ABS in th 2021 census
- **median_score**: Median VCE study score in the suburb (value has a log transform)
- **average_price**: Mean price of schools in a suburb (value has a log transform)
- **proximity_to_beach**: Difference in euclidean distance based off coordinate values (latitude and longitude) (value has a log transform)
- **airbnb_count**: Total number of airbnb’s in a suburb (value has a log transform)
- **commercial_density**: The number of commercial establishments (e.g., offices, shops) in the suburb per square kilometres (value has a log transform).
- **education_density**: The number of educational institutions (e.g., schools, colleges) in the suburb per square kilometres (value has a log transform).
- **food_establishments_density**: The number of food-related establishments (e.g., restaurants, cafes) in the suburb per square kilometres (value has a log transform).
- **healthcare_density**: The number of healthcare facilities (e.g., clinics, hospitals) in the suburb per square kilometres (value has a log transform).
- **industrial_density**: The numberof industrial areas or factories in the suburb per square kilometres (value has a log transform).
- **public_transport_density**: The number of public transportation options (e.g., bus stops, train stations) in the suburb per square kilometres (value has a log transform).
- **recreation_density**: The number of recreational facilities (e.g., parks, gyms, sports centres) in the suburb per square kilometres (value has a log transform).
- **residential_density**: The number of residential buildings (e.g., houses, apartments) in the suburb per square kilometres (value has a log transform).
- **shopping_density**: The number of shopping centres or retail establishments in the suburb per square kilometres (value has a log transform).
- **pop_density**: The population density of the suburb, measured as the number of people per square kilometres (value has a log transform).
- **interest_rate**: The interest rate during the respective year.
- **Median_tot_fam_inc_weekly/inflation**: The median total weekly family income in AUD, adjusted for inflation (value has a log transform).
- **Median_tot_hhd_inc_weekly/inflation**: The median total weekly household income in AUD, adjusted for inflation (value has a log transform).
- **Median_tot_prsnl_inc_weekly/inflation**: The median total weekly personal income in AUD, adjusted for inflation (value has a log transform).
- **gdp_cbd/inflation/beach**: The adjusted gross domestic product (GDP) contribution of the CBD area relative to proximity to the beach, factoring in inflation (value has a log transform).
- **gdp_cbd/inflation/cbd**: The adjusted GDP contribution of the CBD area relative to itself, factoring in inflation (value has a log transform).
- **gdp/inflation/airbnb**: The adjusted GDP contribution relative to Airbnb activity in the suburb, factoring in inflation (value has a log transform).
- **average_weekly_rent/inflation/household_size** (_Our response variable_): The average weekly rent in AUD for each suburb divided by inflation and Average_household_size. Note that average weekly rent for each suburb was derived from the entire suburb cluster, so suburbs from the same cluster will have the same weekly rent, but since household_size may differ the values will not be the exact same.
- **A Crimes against the person/per_person**: The number of crimes against individuals (e.g., assaults) in the suburb, adjusted per person (value has a log transform).
- **B Property and deception offences/per_person**: The number of property and deception-related crimes (e.g., theft, fraud) in the suburb, adjusted per person (value has a log transform).
- **C Drug offences/per_person**: The number of drug-related offences (e.g., possession, trafficking) in the suburb, adjusted per person (value has a log transform).
- **D Public order and security offences/per_person**: The number of public order offences (e.g., disturbances, trespassing) in the suburb, adjusted per person (value has a log transform).
- **E Justice procedures offences/per_person**: The number of offences related to justice procedures (e.g., breaches of court orders) in the suburb, adjusted per person (value has a log transform).
- **F Other offences/per_person**: The number of miscellaneous offences (e.g., regulatory breaches) in the suburb, adjusted per person (value has a log transform).
