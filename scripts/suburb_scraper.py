import requests
import csv
import json

# Fetch the CSV content from the URL
url = 'https://raw.githubusercontent.com/michalsn/australian-suburbs/master/data/suburbs.csv'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    csv_data = response.text  # Get the CSV text from the response

    # Save the CSV content to a file
    input_filename = 'data/raw/suburbs.csv'
    with open(input_filename, 'w', newline='', encoding='utf-8') as file:
        file.write(csv_data)
    print(f"CSV data saved to {input_filename}")

    # Proceed with filtering the CSV and other operations
    output_filename = 'data/raw/vic_suburbs.csv'
    with open(input_filename, 'r') as infile:
        reader = csv.DictReader(infile)
        
        # Prepare for writing filtered data
        fieldnames = reader.fieldnames
        filtered_rows = [row for row in reader if row['state'] == 'VIC']

    # Write filtered data to a new CSV file
    with open(output_filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Filtered data has been written to {output_filename}")

    # Initialize an empty dictionary to store the result
    result_dict = {}

    # Read the filtered CSV file
    with open(output_filename, 'r') as infile:
        reader = csv.DictReader(infile)
        
        # Process each row
        for row in reader:
            # Extract and format the key
            suburb_key = f"{row['suburb'].replace(' ', '-').lower()}-{row['state'].lower()}-{row['postcode']}"
            
            # Create the dictionary entry
            result_dict[suburb_key] = {
                "ssc_code": row['ssc_code'],
                "suburb": row['suburb'],
                "urban_area": row['urban_area'],
                "postcode": row['postcode'],
                "state": row['state'],
                "state_name": row['state_name'],
                "type": row['type'],
                "local_goverment_area": row['local_goverment_area'],
                "statistic_area": row['statistic_area'],
                # "elevation": row['elevation'],
                # "population": row['population'],
                # "median_income": row['median_income'],
                "sqkm": row['sqkm'],
                "lat": row['lat'],
                "lng": row['lng'],
                # "timezone": row['timezone']
            }

    # Save the dictionary to a JSON file
    with open('data/raw/vic_suburbs.json', 'w') as outfile:
        json.dump(result_dict, outfile, indent=4)

    print("Dictionary has been created and saved to 'output_dict.json'")

else:
    print(f"Failed to retrieve the CSV. HTTP Status Code: {response.status_code}")
