import json
import requests
from concurrent.futures import ThreadPoolExecutor
import DataRefiner as DR
from tqdm import tqdm

# Initialize an empty list to store the @id values
id_list = []

# Specify the URLs to fetch the GeoJSON files
node_geojson_url = 'https://raw.githubusercontent.com/CodeTheCity/Moderdeen/main/History/ListOfNodes.geojson'
way_geojson_url = 'https://raw.githubusercontent.com/CodeTheCity/Moderdeen/main/History/ListOfWays.geojson'

print("Started getting IDs")

# Function to fetch IDs from GeoJSON and add them to the id_list
def fetch_ids_from_geojson(geojson_url):
    try:
        # Fetch the GeoJSON data from the URL
        response = requests.get(geojson_url)
        if response.status_code == 200:
            geojson_data = response.json()

            # Check if the GeoJSON has a 'features' key and it's a list
            if 'features' in geojson_data and isinstance(geojson_data['features'], list):
                # Iterate through each feature in the GeoJSON
                for feature in geojson_data['features']:
                    # Check if '@id' is present in the feature's properties
                    if 'properties' in feature and '@id' in feature['properties']:
                        # Append the '@id' value to the id_list
                        id_list.append(feature['properties']['@id'])
                print(f"Got IDs from {geojson_url}")
        else:
            print(f"Failed to fetch GeoJSON data from the URL: {geojson_url}")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Fetch IDs from both GeoJSON files
fetch_ids_from_geojson(node_geojson_url)
fetch_ids_from_geojson(way_geojson_url)

combined_data = []

# Function to fetch data for a given id_value and append it to combined_data
def fetch_data_and_append(id_value):
    url = f"https://api.openstreetmap.org/api/0.6/{id_value}/history.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data = DR.extract_data(data)
        return data
    else:
        print(f"Failed to fetch data for {id_value}")
        return None

# Create a ThreadPoolExecutor with a maximum of 4 worker threads
with ThreadPoolExecutor(max_workers=4) as executor:
    # Use executor.map to parallelize fetching data for id_list
    results = executor.map(fetch_data_and_append, id_list)
    for result in tqdm(results, total=len(id_list), desc="Getting JSONs"):
        if result:
            combined_data.append(result)

# Write the combined JSON data to a file
output_file_path = 'combined_data.json'
with open(output_file_path, 'w') as output_file:
    json.dump(combined_data, output_file, indent=2)

print(f"Combined data for {len(combined_data)} @id values and saved to {output_file_path}")
