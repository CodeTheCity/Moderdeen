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



## History
To get more uptodate data run GetHistory.py and run
node
  ["addr:street"="Union Street"]
  ["addr:city"="Aberdeen"]
  ;
out;
 in https://overpass-turbo.eu/ and export as a geojson and rename to ListOfNodes.geojson

 run by cd in History the python GetHistory.py
 
## Todo
Mabye show img of stores