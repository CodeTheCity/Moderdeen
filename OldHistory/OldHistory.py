import requests
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

JSON_URL = "https://raw.githubusercontent.com/CodeTheCity/Moderdeen/main/OldHistory/HistoricalBuildings.json"
FIXED_ADDRESS = "Union+Street&city=Aberdeen&country=UK"

def geocode_location(session, location):
    house_number = location.get("House Number", "")
    name = location.get("Business Name", "")
    residential = location.get("Residential", "")
    building_name = location.get("Building Name ", "")
    location["Address"] = "Union Street"
    location["City"] = "Aberdeen"
    business_type = location.get("Business Type", "")
    agent = location.get("Local Agent", "")
    phone = location.get("Phone Number", "")
    telegraph = location.get("Telegraph Address", "")
    date = location.get("Business Established","")

    # Check and set "Residential" to "Unknown" if it's empty
    if residential == "":
        location["Residential"] = "Unknown"

    # Check and set "Building Name" to "Unknown" if it's empty
    if building_name == "":
        location["Building Name "] = "Unknown"

    # Check and set "Business Type" to "Unknown" if it's empty
    if business_type == "":
        location["Business Type"] = "Unknown"

    # Check and set "Local Agent" to "Unknown" if it's empty
    if agent == "":
        location["Local Agent"] = "Unknown"

    # Check and set "Phone Number" to "Unknown" if it's empty
    if phone == "":
        location["Phone Number"] = "Unknown"

    # Check and set "Telegraph Address" to "Unknown" if it's empty
    if telegraph == "":
        location["Telegraph Address"] = "Unknown"

    if date == "":
        location["Business Established"] = "Unknown"

    if house_number:
        address = f"street={house_number}+{FIXED_ADDRESS}"
    elif name:
        address = f"q={name.replace(' ', '+')}&street={FIXED_ADDRESS}"
    else:
        location["Business Name"] = "Unknown"
        location["House Number"] = "Unknown"
        return None
    if name == "":
        location["Business Name"] = "Unknown"
    if house_number == "":
        location["House Number"] = "Unknown"
        
    url = f"https://geocode.maps.co/search?{address}"

    response = session.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            first_result = data[0]
            if "Aberdeen" in first_result.get("display_name", ""):
                location["Latitude"] = first_result.get("lat", "")
                location["Longitude"] = first_result.get("lon", "")
            else:
                location["Latitude"] = ""
                location["Longitude"] = ""
        else:
            location["Latitude"] = ""
            location["Longitude"] = ""
            
    else:
        location["Latitude"] = ""
        location["Longitude"] = ""

def main():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        json_text = response.text.lstrip('\ufeff')
        json_data = json.loads(json_text)
        progress_bar = tqdm(json_data, desc="Geocoding Progress", ncols=100)
        with ThreadPoolExecutor(max_workers=5) as executor:
            with requests.Session() as session:
                list(executor.map(lambda entry: geocode_location(session, entry), progress_bar))
        with open("ModifiedHistory.json", "w") as output_file:
            json.dump(json_data, output_file, indent=2)
        print("Geocoding and saving completed successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
