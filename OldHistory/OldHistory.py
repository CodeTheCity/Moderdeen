import csv
import requests
import json

# Replace 'your_remote_url_here' with the actual URL of the remote TSV file
remote_url = 'https://raw.githubusercontent.com/CodeTheCity/history_jam/master/1937_Union_Street.tsv'

try:
    response = requests.get(remote_url)
    response.raise_for_status()  # Check for any HTTP request errors

    # Create a temporary in-memory file-like object for CSV parsing
    tsvfile = csv.reader(response.text.strip().splitlines(), delimiter='\t')

    # Create a list to store the rows
    data = []

    # Skip the header row if present
    header = next(tsvfile, None)

    for row in tsvfile:
        data.append(row)

    # Define the output JSON file name
    json_output_file = 'data.json'

    # Save the TSV data as a JSON file
    with open(json_output_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)
    
    print(f"Data saved as {json_output_file}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
