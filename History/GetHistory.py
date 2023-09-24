import json
import requests
import DataRefiner as DR
from tqdm import tqdm

# Initialize an empty list to store the @id values
id_list = []

# Specify the path to your export.geojson file
geojson_file_path = 'ListOfNodes.geojson'
print("Started getting IDs")
try:
    # Open and read the GeoJSON file
    with open(geojson_file_path, 'r') as file:
        geojson_data = json.load(file)

    # Check if the GeoJSON has a 'features' key and it's a list
    if 'features' in geojson_data and isinstance(geojson_data['features'], list):
        # Iterate through each feature in the GeoJSON
        for feature in geojson_data['features']:
            # Check if '@id' is present in the feature's properties
            if 'properties' in feature and '@id' in feature['properties']:
                # Append the '@id' value to the id_list
                id_list.append(feature['properties']['@id'])
    print("Got IDs")
except FileNotFoundError:
    print(f"File '{geojson_file_path}' not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

combined_data = []

# Loop through the @id values and fetch data from the API with a loading bar
print("Getting jsons")
for id_value in tqdm(id_list):
    url = f"https://api.openstreetmap.org/api/0.6/{id_value}/history.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        data = DR.extract_data(data)
        combined_data.append(data)
    else:
        print(f"Failed to fetch data for {id_value}")

# Write the combined JSON data to a file
output_file_path = 'combined_data.json'
with open(output_file_path, 'w') as output_file:
    json.dump(combined_data, output_file, indent=2)

print(f"Combined data for {len(combined_data)} @id values and saved to {output_file_path}")
