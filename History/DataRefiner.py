import requests
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

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
            lat_str = first_element.get("lat")
            lon_str = first_element.get("lon")
            
            # Parse lat and lon as floats
            lat = float(lat_str) if lat_str else None
            lon = float(lon_str) if lon_str else None
            
            return lat, lon
    
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

def process_element(element):
    extracted_data = {}
    previous_name = None  # Initialize previous_name as None

    # Extract relevant information
    id_value = element.get("id", "Unknown")
    name = element["tags"].get("name", "Unknown")
    alt_name = element["tags"].get("alt_name", None)
    old_name = element["tags"].get("old_name", None)
    amenity = element["tags"].get("amenity", None)
    shop = element["tags"].get("shop", None)
    disused_shop = element["tags"].get("disused:shop", None)
    disused_amenity = element["tags"].get("disused:amenity", None)
    building = element["tags"].get("building", None)
    craft = element["tags"].get("craft", None)

    # Use the first non-empty name (prefer "name" over "alt_name")
    if name != "Unknown":
        original_name = name.replace('\u2019', "'").replace('\u00e8', 'è')
        name = name.lower()
    elif alt_name:
        original_name = alt_name.replace('\u2019', "'").replace('\u00e8', 'è')
        name = alt_name.lower()
    elif old_name:
        name = old_name.lower()  # Use old_name as the name
        original_name = "Closed: " + old_name.replace('\u2019', "'").replace('\u00e8', 'è')  # Keep the original casing
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

    if (building_number is None or postcode is None) and lat is not None and lon is not None:
        address_data = reverse_geocode(lat, lon)
        if address_data:
            parts = address_data.split(", ")
            if len(parts) > 6:
                # Check if parts[0] is a number
                if parts[0].isdigit():
                    building_number, postcode = parts[0], parts[-2]

    # Check if amenity is null but "shop" is present, use "shop" as amenity
    if amenity is None and shop:
        amenity = shop
    elif amenity is None and shop is None and building:
        amenity = building
    elif amenity is None and craft:
        amenity = craft
    elif amenity is None and shop is None and disused_amenity:
        amenity = disused_amenity
    else:
        amenity = "Unknown"
    
    # Check if disused:shop is " yes" and add "Disused" prefix to the name
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
        extracted_data = {
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
        
        # Check if there's a previous_name and update the current item's name
        if previous_name:
            extracted_data[name]["name"] = f"{original_name} (Formerly: {previous_name})".replace("Closed: ", "")
        
    previous_name = original_name  # Update previous_name for the next iteration

    return extracted_data

def extract_data(json_data):
    extracted_data_dict = defaultdict(list)

    # Create a ThreadPoolExecutor with a maximum of 4 worker threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(process_element, json_data.get("elements", []))
        for result in results:
            name = result.get("name", "Unknown").lower()  # Convert name to lowercase for comparison
            extracted_data_dict[name].append(result)

    extracted_data_list = []

    for name, items in extracted_data_dict.items():
        # Sort items by timestamp in descending order
        items.sort(key=lambda x: x["timestamp"], reverse=True)

        # Append the item with the latest timestamp to the result list
        extracted_data_list.append(items[0])

    return extracted_data_list
