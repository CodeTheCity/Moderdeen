import requests
import time

# Fixed address for Union Street, Aberdeen, UK
FIXED_ADDRESS = "Union+Street&city=Aberdeen&country=UK"
def forward_geocode(building_number, name):
    if building_number:
        url = f"https://geocode.maps.co/search?street={building_number}+{FIXED_ADDRESS}"
    elif name:
        url = f"https://geocode.maps.co/search?q={name.replace(' ', '+')}&street=union+street&city=aberdeen&country=uk"
    else:
        return None, None
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            first_element = data[0]
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
            name = old_name.lower()  # Use old_name as the name
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
        if lat is None and lon is None and (building_number or name != "Unknown"):
            lat, lon = forward_geocode(building_number, name)
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

        if name in extracted_data:
            existing_item = extracted_data[name]

            # Check if the current item has a newer timestamp
            if timestamp < existing_item["timestamp"]:
                # Update the existing item with the newer information
                # and fill in missing values if they are null
                existing_item["lat"] = lat if lat is not None else existing_item["lat"]
                existing_item["lon"] = lon if lon is not None else existing_item["lon"]
                existing_item["building_number"] = (
                    building_number if building_number is not None else existing_item["building_number"]
                )
                existing_item["postcode"] = (
                    postcode if postcode is not None else existing_item["postcode"]
                )

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
                "building_number": building_number if building_number is not None else "Unknown",
                "postcode": postcode if postcode is not None else "Unknown",
                "note": element.get("tags").get("note", "N/A"),
            }

    # Convert the dictionary values to a list of items
    extracted_data_list = list(extracted_data.values())
    return extracted_data_list
