def refine(json_data):
    extracted_data = []

    for element in json_data.get("elements", []):
        # Initialize a dictionary to store the extracted data for this element
        extracted_item = {}

        # Extract the version, id, name or alt_name (prefer name), timestamp, amenity, lat, lon
        extracted_item["version"] = element.get("version", None)
        extracted_item["OSM_id"] = element.get("id", None)
        extracted_item["name"] = element["tags"].get("name", element["tags"].get("alt_name", None))
        extracted_item["timestamp"] = element.get("timestamp", None)
        extracted_item["amenity"] = element["tags"].get("amenity", None)
        extracted_item["lat"] = element.get("lat", None)
        extracted_item["lon"] = element.get("lon", None)

        # Extract building number and postcode
        extracted_item["building_number"] = element["tags"].get("addr:housenumber", None)
        extracted_item["postcode"] = element["tags"].get("addr:postcode", None)

        # Append this extracted item to the list
        extracted_data.append(extracted_item)

    return extracted_data