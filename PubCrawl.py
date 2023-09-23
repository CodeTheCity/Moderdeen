import json

# Load the GeoJSON data from the file
with open('export.geojson', 'r') as file:
    data = json.load(file)

# Iterate through features and print names, street number, postcode, and street name
for feature in data['features']:
    name = feature['properties']['name'] if 'name' in feature['properties'] else 'N/A'
    street_number = feature['properties']['addr:housenumber'] if 'addr:housenumber' in feature['properties'] else 'N/A'
    postcode = feature['properties']['addr:postcode'] if 'addr:postcode' in feature['properties'] else 'N/A'
    street_name = feature['properties']['addr:street'] if 'addr:street' in feature['properties'] else 'N/A'

    print(f"Name: {name}")
    print(f"Street Number: {street_number}")
    print(f"Street Name: {street_name}")
    print(f"Postcode: {postcode}")
    print("\n")
