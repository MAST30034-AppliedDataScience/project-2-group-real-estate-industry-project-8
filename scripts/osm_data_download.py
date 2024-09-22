import overpy
import geojson
import os
from decimal import Decimal
import time

# Initialize the Overpass API
api = overpy.Overpass()

# Define the list of useful OSM tags/features
features_to_fetch = [
    # 1. Schools, colleges, universities, and other educational institutions
    {"tag": '["amenity"~"school|college|university|kindergarten|preschool"]', "name": "education"},
    
    # 2. Hospitals, clinics, pharmacies, and other healthcare facilities
    {"tag": '["amenity"~"hospital|clinic|pharmacy|dentist|doctors"]', "name": "healthcare"},
    
    # 3. Parks, gardens, playgrounds, and recreational areas
    {"tag": '["leisure"~"park|garden|playground|golf_course|sports_centre"]', "name": "recreation"},
    
    # 4. Residential and mixed-use land
    {"tag": '["landuse"~"residential|mixed_use|living_street"]', "name": "residential"},
    
    # 5. Commercial, retail, and business land
    {"tag": '["landuse"~"commercial|retail|business"]', "name": "commercial"},
    
    # 6. Industrial areas, warehouses, and factories
    {"tag": '["landuse"~"industrial|warehouse|factory"]', "name": "industrial"},
    
    # 7. Restaurants, cafes, bars, and food establishments
    {"tag": '["amenity"~"restaurant|cafe|bar|pub|fast_food"]', "name": "food_establishments"},
    
    # 8. Public transportation hubs
    {"tag": '["amenity"~"bus_station|tram_stop|subway_entrance|railway_station"]', "name": "public_transport"},
    
    # 9. Shopping facilities
    {"tag": '["shop"~"supermarket|mall|convenience|bakery|clothes"]', "name": "shopping"}
]



# Function to convert all Decimals to floats
def convert_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    else:
        return obj

# Define the directory for saving files
directory = "data/landing/osm_data"
os.makedirs(directory, exist_ok=True)

# Loop through each year from 2016 to the current year
for year in range(2016, 2024):  # Adjust end year accordingly
    print(f"Fetching data for the year {year}...")

    # Start time for fetching all features for the year
    start_time_year = time.time()

    # Create a list to hold all features for the year
    all_features = []

    # Loop through each feature
    for feature in features_to_fetch:
        feature_name = feature["name"]
        print(f"Fetching {feature_name} data for {year}...")

        # Start time for fetching a specific feature
        start_time_feature = time.time()

        # Build the Overpass query for the current feature and year
        query = f"""
        [out:json][timeout:600][date:"{year}-01-01T00:00:00Z"];
        (
          node{feature['tag']}(-39.2,140.5,-33.9,150.2);
          way{feature['tag']}(-39.2,140.5,-33.9,150.2);
          relation{feature['tag']}(-39.2,140.5,-33.9,150.2);
        );
        out center;
        """

        try:
            # Run the query
            print(f"Executing query for {feature_name} in {year}...")
            result = api.query(query)
        except Exception as e:
            print(f"Error fetching data for {feature_name} in {year}: {e}")
            continue  # Skip this feature and move to the next one

        # Process nodes for the current feature
        try:
            print(f"Processing {feature_name} nodes for {year}...")
            for node in result.nodes:
                lon = float(node.lon)
                lat = float(node.lat)

                properties = convert_decimals({
                    "id": int(node.id),
                    "tags": node.tags,
                    "element_type": "node",
                    "feature_type": feature_name
                })

                geojson_feature = geojson.Feature(
                    geometry=geojson.Point((lon, lat)),
                    properties=properties
                )
                all_features.append(geojson_feature)
        except Exception as e:
            print(f"Error processing nodes for {feature_name} in {year}: {e}")

        # Process ways for the current feature
        try:
            print(f"Processing {feature_name} ways for {year}...")
            for way in result.ways:
                try:
                    # Use center if available, otherwise calculate manually
                    if way.center_lat and way.center_lon:
                        lon = way.center_lon
                        lat = way.center_lat
                    else:
                        # Fallback to calculating center
                        lon, lat = Decimal(0), Decimal(0)
                        if way.nodes:
                            for node in way.nodes:
                                lon += node.lon
                                lat += node.lat
                            lon /= len(way.nodes)
                            lat /= len(way.nodes)
                        else:
                            # Skip this way if no center or nodes are available
                            print(f"Skipping way {way.id} due to missing nodes and no center.")
                            continue

                    properties = convert_decimals({
                        "id": int(way.id),
                        "tags": way.tags,
                        "element_type": "way",
                        "feature_type": feature_name
                    })

                    geojson_feature = geojson.Feature(
                        geometry=geojson.Point((float(lon), float(lat))),
                        properties=properties
                    )
                    all_features.append(geojson_feature)
                except Exception as e:
                    print(f"Error processing way {way.id} for {feature_name} in {year}: {e}")
        except Exception as e:
            print(f"Error processing ways for {feature_name} in {year}: {e}")

        # Process relations for the current feature
        try:
            print(f"Processing {feature_name} relations for {year}...")
            for relation in result.relations:
                try:
                    if relation.center_lat and relation.center_lon:
                        lon = relation.center_lon
                        lat = relation.center_lat

                        properties = convert_decimals({
                            "id": int(relation.id),
                            "tags": relation.tags,
                            "element_type": "relation",
                            "feature_type": feature_name
                        })

                        geojson_feature = geojson.Feature(
                            geometry=geojson.Point((float(lon), float(lat))),
                            properties=properties
                        )
                        all_features.append(geojson_feature)
                    else:
                        print(f"Skipping relation {relation.id} due to missing center coordinates.")
                except Exception as e:
                    print(f"Error processing relation {relation.id} for {feature_name} in {year}: {e}")
        except Exception as e:
            print(f"Error processing relations for {feature_name} in {year}: {e}")

        # End time for fetching and processing the current feature
        end_time_feature = time.time()
        elapsed_time_feature = end_time_feature - start_time_feature
        print(f"Finished fetching and processing {feature_name} data for {year} in {elapsed_time_feature:.2f} seconds.\n")

    # Create a GeoJSON FeatureCollection for all features of the year
    try:
        feature_collection = geojson.FeatureCollection(all_features)

        # Define the file path
        file_path = os.path.join(directory, f"features_{year}.geojson")

        # Save to a GeoJSON file
        print(f"Saving all features for {year} to file '{file_path}'...")
        with open(file_path, "w") as geojson_file:
            geojson.dump(feature_collection, geojson_file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving GeoJSON file for {year}: {e}")

    # End time for fetching all features for the year
    end_time_year = time.time()
    elapsed_time_year = end_time_year - start_time_year
    print(f"GeoJSON file for {year} saved successfully in {elapsed_time_year:.2f} seconds.\n")

print("All data fetched and saved successfully.")
