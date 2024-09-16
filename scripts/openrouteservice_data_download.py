import requests
import json
import time
import pandas as pd
import folium

# In this script ors is an acronym for openstreetmap

def api_call(BASE_API_LINK, headers, payload_data, CBD):

    # API call limit is 40 per minute, here we make sure we do not breach that adhearing to the ORS's API policies
    call_interval = 60 / 39 # 39 is used as a boundary (make sure we never do 40 api calls in a minute)
    time.sleep(call_interval)
    response = requests.post(BASE_API_LINK, headers=headers, json=payload_data)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Success: {response.status_code}")
        # Process and print the response data
        data = response.json()

        distance = data["routes"][0]["summary"]["distance"] # km
        duration = data["routes"][0]["summary"]["duration"] # secs

        # create a dictionary of results of time and distances
        if CBD:
            distance_CBD_record = {
                "suburb_centre_latitude": payload_data["coordinates"][0][1],
                "suburb_centre_longitude": payload_data["coordinates"][0][0],
                "distance_to_CBD": distance,
                "time_to_CBD": duration,
            }
        else:
            distance_CBD_record = {
                "suburb_centre_latitude": payload_data["coordinates"][0][1],
                "suburb_centre_longitude": payload_data["coordinates"][0][0],
                "distance_to_station": distance,
                "time_to_station": duration,
            }
        return distance_CBD_record
    else:
        print(f"Error: {response.status_code}")
        print(response.text)  # Print error message for debugging
        return None


def download_ors_proximity_data(suburb_and_coords_df, api_key):
    """ 
        Donwloads all distance and time by car from the centre of the suburbs in the given dataframe to the CBD.
        This is done through an API and the distances and time is outputted into a JSON file.
    """
    CBD_lng = 144.9623
    CBD_lat = -37.8124
    proximity_to_CBD = {}

    # Define the API endpoint and API key
    ORS_BASE_URL = "https://api.openrouteservice.org"
    DIRECTIONS_SERVICE = "/v2/directions/driving-car"
    BASE_API_LINK = ORS_BASE_URL + DIRECTIONS_SERVICE
    API_KEY = api_key

    # Set the headers
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    api_call_count = 0

    # loop through all suburbs and get distance and time from CBD
    for suburb_index in list(suburb_and_coords_df.index):
    
        # retrieve suburb: name, longitude and latitude coordinates
        suburb = suburb_and_coords_df.iloc[suburb_index]["Suburb(s)"]
        start_lng = suburb_and_coords_df.loc[suburb_index, "center_longitude"]
        start_lat = suburb_and_coords_df.loc[suburb_index, "center_latitude"]
        
        # Define the request payload
        payload_data = {
            "coordinates": [
                [start_lng, start_lat],  # Note the order: [longitude, latitude]
                [CBD_lng, CBD_lat]
            ]
        }
        api_call_count += 1
        # Make the POST request
        distance_CBD_record = api_call(BASE_API_LINK, headers, payload_data, True)
        if distance_CBD_record != None:
            # Define the request payload for station 1
            payload_data = {
                "coordinates": [
                    [suburb_and_coords_df.loc[suburb_index, "closest_station_1_LONGITUDE"], 
                    suburb_and_coords_df.loc[suburb_index, "closest_station_1_LATITUDE"]], 
                    [start_lng, start_lat]
                ]
            }
            distance_train1_record = api_call(BASE_API_LINK, headers, payload_data, False)

            # Define the request payload for station 2
            payload_data = {
                "coordinates": [
                    [suburb_and_coords_df.loc[suburb_index, "closest_station_2_LONGITUDE"], 
                    suburb_and_coords_df.loc[suburb_index, "closest_station_2_LATITUDE"]], 
                    [start_lng, start_lat]
                ]
            }
            distance_train2_record = api_call(BASE_API_LINK, headers, payload_data, False)
            # Define the request payload for station 3
            payload_data = {
                "coordinates": [
                    [suburb_and_coords_df.loc[suburb_index, "closest_station_3_LONGITUDE"], 
                    suburb_and_coords_df.loc[suburb_index, "closest_station_3_LATITUDE"]], 
                    [start_lng, start_lat]
                ]
            }

            distance_train3_record = api_call(BASE_API_LINK, headers, payload_data, False)
            if distance_train3_record["distance_to_station"] < distance_train2_record["distance_to_station"]:
                if distance_train3_record["distance_to_station"] < distance_train1_record["distance_to_station"]:
                    closest_station_record = distance_train3_record
                else:
                    closest_station_record = distance_train1_record
            else:
                if distance_train1_record["distance_to_station"] < distance_train2_record["distance_to_station"]:
                    closest_station_record = distance_train1_record
                else:
                    closest_station_record = distance_train2_record
            
            distance_CBD_record["distance_to_station"] = closest_station_record["distance_to_station"]
            distance_CBD_record["time_to_station"] = closest_station_record["time_to_station"]
            proximity_to_CBD[suburb] = distance_CBD_record
        else:
            proximity_to_CBD[suburb] = {

            }
        print(f"suburb(s) no. {api_call_count} complete")
    # Output File path
    file_path = "../data/landing/proximity_data.json"

    # output the results of the API search
    with open(file_path, 'w') as file:
        json.dump(proximity_to_CBD, file, indent=4)