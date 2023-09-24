CTC30 

## PubCrawler
This gets all pubs on and around union street. to get more uptodate version run the code below on https://overpass-turbo.eu/ and export as a geojson and story into the PubCrawl dir and refresh the html.

    [out:json];
    (
      // Search for pubs directly on Union Street
      node["amenity"="pub"]["addr:street"="Union Street"]["addr:city"="Aberdeen"]; 
      // Search for pubs near Union Street (within a specified radius) and get their center points
      (
        node["amenity"="pub"]["addr:city"="Aberdeen"](around:500,57.1470,-2.1047);
        way["amenity"="pub"]["addr:city"="Aberdeen"](around:500,57.1470,-2.1047);
      );
    );
    out center;


# History

This section provides instructions on how to obtain and update historical data related to Union Street in Aberdeen, UK. The historical data includes information about buildings and other elements captured by OpenStreetMap contributors.

## Getting Historical Data

To obtain historical data, you can use the OpenStreetMap Overpass API. Follow these steps:

1. Go to [Overpass Turbo](https://overpass-turbo.eu/).

2. In the Overpass Turbo editor, use the following query to search for data related to Union Street in Aberdeen:

```
[out:json][timeout:999];
// gather results
(
node["addr:street"="Union Street"]["addr:city"="Aberdeen"];
way["addr:street"="Union Street"]["addr:city"="Aberdeen"];
);
out;

```

3. Click the "Run" button to execute the query.

Once the data is displayed on the map, click the "Export" button and select "GeoJSON" as the export format. Save the file with an appropriate name, e.g., ListOfNodes.geojson.

Store the exported GeoJSON file in the "History" directory of your project and commit it and push it to remote or change the link to your chosen json file.

Updating Historical Data
To keep the historical data up-to-date, you can use the provided Python script, GetHistory.py, which automates the process of fetching and updating data. Follow these steps:

Run the Python script GetHistory.py. This script uses the Overpass API to fetch the latest data related to Union Street.

The script will create or update the ListOfNodes.geojson file in the "History" directory with the latest data.

You can run this script periodically to ensure your historical data remains current.

##Dependencies
To run the GetHistory.py script, make sure you have the tqdm library installed. You can install it using pip:


```pip install tqdm```
 
##Example Usage
Here's an example of how you can use the historical data:
Load the historical data into your application using the GeoJSON file.
Use the data to display information about buildings, amenities, and other elements along Union Street in Aberdeen.
Explore and visualize the historical changes and evolution of Union Street over time.
Feel free to enhance and customize your project with this valuable historical data to create engaging visualizations or applications.
For more information on using the historical data in your project, refer to the provided Python script and HTML interface.
If you have any questions or need further assistance, please don't hesitate to ask.
