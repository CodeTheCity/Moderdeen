CTC30 


Radius of the seach was 700m, the cordinates are 57.1445 and -2.0967

[out:json];
(
  node["amenity"="pub"](around:700,57.1445,-2.0967); // Adjust the radius and coordinates as needed
);
out;

To get more uptodate data run GetHistory.py and run
node
  ["addr:street"="Union Street"]
  ["addr:city"="Aberdeen"]
  ;
out;
 in https://overpass-turbo.eu/ and export as a geojson and rename to ListOfNodes.geojson
 
