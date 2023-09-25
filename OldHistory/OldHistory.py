import requests
import json
from tqdm import tqdm  # Import tqdm for the loading bar

# Define the URL of the JSON file and the fixed address
JSON_URL = "https://raw.githubusercontent.com/CodeTheCity/Moderdeen/main/OldHistory/HistoricalBuildings.json"
FIXED_ADDRESS = "Union+Street&city=Aberdeen&country=UK"

# Function to perform geocoding
def geocode_location(location):
    house_number = location.get("House Number", "")
    name = location.get("Business Name", "")

    if house_number:
        address = f"{house_number}+{FIXED_ADDRESS}"
    elif name:
        address = f"{name.replace(' ', '+')}&street=union+street&city=aberdeen&country=uk"
    else:
        return None

    url = f"https://geocode.maps.co/search?street={address}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            # Extract latitude and longitude from the first result
            first_result = data[0]
            location["Latitude"] = first_result.get("lat", "")
            location["Longitude"] = first_result.get("lon", "")
        else:
            location["Latitude"] = ""
            location["Longitude"] = ""
    else:
        location["Latitude"] = ""
        location["Longitude"] = ""

# Function to read, update, and save JSON data
def main():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        
        # Remove the BOM manually
        json_text = response.text.lstrip('\ufeff')
        json_data = json.loads(json_text)
        
        # Create a loading bar using tqdm
        progress_bar = tqdm(json_data, desc="Geocoding Progress", ncols=100)
        
        for entry in progress_bar:
            geocode_location(entry)

        with open("ModifiedHistory.json", "w") as output_file:
            json.dump(json_data, output_file, indent=2)
        
        print("Geocoding and saving completed successfully.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
