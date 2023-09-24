import requests
import time

# Fixed address for Union Street, Aberdeen, UK
FIXED_ADDRESS = "Union+Street&city=Aberdeen&country=UK"
# Function to perform forward geocoding
def forward_geocode(building_number):
    url = f"https://geocode.maps.co/search?street={building_number}+{FIXED_ADDRESS}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:  # Check if data is not an empty list
            first_element = data[0]  # Access the first element of the list
            return first_element.get("lat"), first_element.get("lon")
    return None, None


# Function to perform reverse geocoding
def reverse_geocode(lat, lon):
    url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data["display_name"]
    return None

def extract_data(json_data):
    extracted_data = {}

    for element in json_data.get("elements", []):
        # Extract relevant information
        id_value = element.get("id", "Unknown")
        name = element["tags"].get("name", "Unknown")
        alt_name = element["tags"].get("alt_name", "Unknown")
        old_name = element["tags"].get("old_name", "Unknown")
        amenity = element["tags"].get("amenity", "Unknown")
        shop = element["tags"].get("shop", "Unknown")
        disused_shop = element["tags"].get("disused:shop", "Unknown")
        disused_amenity = element["tags"].get("disused:amenity", "Unknown")

        # Use the first non-empty name (prefer "name" over "alt_name")
        if name != "Unknown":
            original_name = name.replace('\u2019', "'")
            name = name.lower()
        elif alt_name  != "Unknown":
            original_name = alt_name.replace('\u2019', "'")
            name = alt_name.lower()
        elif old_name != "Unknown":
            name = old_name  # Use old_name as the name
            original_name = "Closed: " + old_name.replace('\u2019', "'")  # Keep the original casing
        else:
            name = "Unknown"
            original_name = "Unknown"

        timestamp = element.get("timestamp", None)
        lat = element.get("lat", None)
        lon = element.get("lon", None)
        building_number = element["tags"].get("addr:housenumber", None)
        postcode = element["tags"].get("addr:postcode", None)
        # Check if lat and lon are None, and perform forward geocoding with the fixed address
        if lat is None and lon is None and building_number:
            lat, lon = forward_geocode(building_number)
            time.sleep(0.5)  # To avoid exceeding the rate limit (2 calls per second)

        # Check if building_number or postcode is not known, and perform reverse geocoding
        if (building_number is None or postcode is None) and lat is not None and lon is not None:
            address_data = reverse_geocode(lat, lon)
            if address_data:
                parts = address_data.split(", ")
                if len(parts) > 6:
                    building_number, postcode = parts[0], parts[-2]
        # Check if amenity is null but "shop" is present, use "shop" as amenity
        if amenity is None and shop:
            amenity = shop
        elif amenity is None and shop is None and disused_amenity:
            amenity = disused_amenity

        # Check if disused:shop is "yes" and add "Disused" prefix to the name
        if disused_shop == "yes":
            if name != "Unknown":
                name = "Disused " + name
            if original_name:
                original_name = "Disused " + original_name

        # Check if this item with the same name already exists (case-insensitive comparison)
        if name in extracted_data:
            existing_item = extracted_data[name]
            # Check if the current item has a newer timestamp
            if timestamp < existing_item["timestamp"]:
                # Update the existing item with the newer information
                extracted_data[name] = {
                    "id": id_value,
                    "name": original_name,  # Keep the original casing
                    "timestamp": timestamp,
                    "version": element.get("version", None),
                    "amenity": amenity,
                    "lat": lat,
                    "lon": lon,
                    "building_number": (
                        building_number if building_number is not None else existing_item["building_number"]
                    ) if building_number is not None else "Unknown",  # Turn into "Unknown" if null
                    "postcode": (
                        postcode if postcode is not None else existing_item["postcode"]
                    ) if postcode is not None else "Unknown",  # Turn into "Unknown" if null
                    "note": element.get("tags").get("note", "N/A"),  # Add the "note" field
                }
        else:
            # This is the first item with this name, add it to the dictionary
            extracted_data[name] = {
                "id": id_value,
                "name": original_name,  # Keep the original casing
                "timestamp": timestamp,
                "version": element.get("version", None),
                "amenity": amenity,
                "lat": lat,
                "lon": lon,
                "building_number": building_number if building_number is not None else "Unknown",  # Turn into "Unknown" if null
                "postcode": postcode if postcode is not None else "Unknown",  # Turn into "Unknown" if null
                "note": element.get("tags").get("note", "N/A"),  # Include the "note" field
            }

    # Convert the dictionary values to a list of items, excluding the lowercase name
    extracted_data_list = []
    for value in extracted_data.values():
        extracted_data_list.append({
            "id": value["id"],
            "name": value["name"],
            "timestamp": value["timestamp"],
            "version": value["version"],
            "amenity": value["amenity"],
            "lat": value["lat"],
            "lon": value["lon"],
            "building_number": value["building_number"],
            "postcode": value["postcode"],
            "note": value["note"],  # Include the "note" field
        })

    return extracted_data_list
