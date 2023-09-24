CTC30 

# Pub Crawl Planner Web Application

This Markdown file explains the structure and functionality of a web application named "Pub Crawler Planner." The provided HTML and JavaScript code represents the front-end of this application.

## HTML Structure

The HTML structure of the web application is contained within a `<!DOCTYPE html>` document. Here's an overview of the key sections within the HTML:

### Document Head

- The `<head>` section includes essential metadata and external resources like CSS and JavaScript libraries.
- It sets the character encoding and defines the viewport for responsive design.
- The application's title is set to "Pub Crawl Planner."
- External CSS and JavaScript libraries are linked for map rendering and routing.

### Styling

- Custom CSS rules are defined within a `<style>` block to style the various components of the application, such as the header, map, form, checkboxes, and buttons.
- A Favicon is added to the web page for branding.

### Body Content

- The application's header contains a centered title, "Pub Crawler Planner."

- The main content is wrapped in a `<div>` with the id "container."

- Inside the container, the map and form elements are enclosed within the "map-container" `<div>`.

### Form

- A form with the id "locationForm" is created to select locations for the pub crawl.

- A scrollable container is provided to display checkboxes for locations.

### JavaScript

- The JavaScript code at the bottom of the document initializes the map using Leaflet, fetches GeoJSON data for locations, dynamically generates checkboxes for these locations, and handles the creation of routes between selected locations.

## JavaScript Functionality

Here's an explanation of the JavaScript functionality in the code:

1. **Map Initialization**:
   - Leaflet is used to initialize a map centered on geographical coordinates (latitude: 57.1459838, longitude: -2.0978495).
   - OpenStreetMap is used as the base tile layer.

2. **GeoJSON Data Fetching**:
   - GeoJSON data is fetched from a URL using the `fetch` API.
   - The fetched data is processed, and a GeoJSON layer is created and added to the map.
   - Popup markers with location names are added to the GeoJSON layer.

3. **Checkbox Generation**:
   - Checkboxes for each location are dynamically generated based on the GeoJSON data.
   - Each checkbox corresponds to a location and includes the location's name.

4. **Create Route Functionality**:
   - When the "Create Route" button is clicked, a route is generated between selected locations.
   - Existing routing controls are removed.
   - Selected checkboxes are used to create waypoints for the route.
   - A minimum of two locations must be selected to create a route.
   - The map is updated to show the route.

5. **Reset Map Functionality**:
   - After creating a route, a "Reset Map" button is created.
   - Clicking this button removes the routing control and shows all locations on the map again.

The web application allows users to plan a pub crawl by selecting locations, creating a route, and viewing it on the map. It provides a user-friendly interface with checkboxes for location selection and a map for visualizing the pub crawl route.

# Get History

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

## Dependencies
To run the GetHistory.py script, make sure you have the tqdm library installed. You can install it using pip:


```pip install tqdm```
 
## Example Usage
Here's an example of how you can use the historical data:
Load the historical data into your application using the GeoJSON file.
Use the data to display information about buildings, amenities, and other elements along Union Street in Aberdeen.
Explore and visualize the historical changes and evolution of Union Street over time.
Feel free to enhance and customize your project with this valuable historical data to create engaging visualizations or applications.
For more information on using the historical data in your project, refer to the provided Python script and HTML interface.
If you have any questions or need further assistance, please don't hesitate to ask.

# Building History Viewer Web Application

This HTML document represents a web application called "Building History Viewer." The application allows users to search and view historical data about buildings in Aberdeen. Below is an explanation of the structure and functionality of the provided HTML and JavaScript code.

## HTML Structure

The HTML structure of the web application is as follows:

### Document Head

- The `<head>` section includes metadata such as character encoding and viewport settings.

- The title of the web page is set to "Building History Viewer."

- An icon (favicon) is linked to the web page.

- CSS styles for the application are defined within a `<style>` block in the head.

### Body Content

- The `<body>` section contains the content visible to users.

- An `<h1>` element displays the application's title, "Building History Viewer."

- The main content is wrapped in a `<div>` with the class "container," which sets the maximum width, background color, and box shadow for the content.

- The content includes:
  - A search input field labeled "Keyword."
  - A dropdown labeled "Select a Building" that allows users to choose a specific building.
  - A table with an empty `<tbody>` element where building data will be displayed.
  - An embedded OpenStreetMap frame for displaying location data.

## JavaScript Functionality

The JavaScript code at the bottom of the HTML document provides the application's functionality:

- The `createTableRow` function is defined to create a table row (`<tr>`) for displaying building data.

- The application fetches JSON data from a URL (https://raw.githubusercontent.com/CodeTheCity/Moderdeen/main/History/combined_data.json) using the `fetch` API.

- The fetched JSON data is processed to group buildings by ID, considering the latest version of each building.

- The dropdown for selecting buildings is populated with options based on the grouped data.

- An event listener is added to the building dropdown to handle user selection. When a building is selected:
  - The map is updated to display the building's location using an embedded OpenStreetMap frame. If no valid coordinates are available for the selected building, default coordinates are used.
  - The table is updated to display the building's historical data.

- The `filterDropdownOptions` function filters the dropdown options based on user input in the search field. It hides options that do not match the entered keyword.

- An event listener is added to the search input field to filter dropdown options as the user types.

## Application Functionality

- Users can enter a keyword in the "Keyword" input field to filter the building dropdown options dynamically.

- Users can select a building from the dropdown to view its historical data and location on the map.

- The map displays a marker for the selected building's location. If coordinates are not available or valid, default map coordinates are used.

- The table below the map displays historical data for the selected building, including its ID, name, timestamp, version, amenity, latitude, longitude, building number, postcode, and notes.

- The table is updated based on the user's selection from the dropdown.

Overall, this web application allows users to explore historical data about buildings in Aberdeen, search for specific buildings, and view their locations on a map. It provides a user-friendly interface for accessing and visualizing building history information.
