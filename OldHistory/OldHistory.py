import requests
import json

def forward_geocode_from_json(json_url, output_file):
    # Fetch the JSON data from the provided URL
    response = requests.get(json_url)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    geocoded_data = []
    
    for item in data:
        address = item.get("Address")
        city = item.get("City")
        
        if address and city:
            # Construct the geocoding URL
            url = f"https://geocode.maps.co/search?q={address.replace(' ', '+')}&street={address.replace(' ', '+')}&city={city}&country=uk"
            response = requests.get(url)
            
            if response.status_code == 200:
                geocode_data = response.json()
                
                if geocode_data and len(geocode_data) > 0:
                    first_element = geocode_data[0]
                    lat_str = first_element.get("lat")
                    lon_str = first_element.get("lon")
                    
                    # Parse lat and lon as floats
                    lat = float(lat_str) if lat_str else None
                    lon = float(lon_str) if lon_str else None
                    
                    item["Latitude"] = lat
                    item["Longitude"] = lon
            
        geocoded_data.append(item)
    
    # Save the geocoded data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(geocoded_data, outfile, indent=4)
    
    return geocoded_data

# Usage example:
json_url = "https://example.com/your/json/file.json"
output_file = "geocoded_data.json"
geocoded_data = forward_geocode_from_json(json_url, output_file)

# The geocoded data is saved to "geocoded_data.json" in the current working directory.
