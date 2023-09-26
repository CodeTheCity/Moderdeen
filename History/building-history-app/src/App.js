import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [selectedBuilding, setSelectedBuilding] = useState('default');
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    // Fetch the JSON data from the URL
    fetch('https://raw.githubusercontent.com/CodeTheCity/Moderdeen/main/History/combined_data.json')
      .then(response => response.json())
      .then(data => {
        setData(data);
      });
  }, []);

  // Function to create a table row for a building
  function createTableRow(building) {
    return (
      <tr key={building.id}>
        <td>{building.id}</td>
        <td>{building.name}</td>
        <td>{building.timestamp}</td>
        <td>{building.version}</td>
        <td>{building.amenity}</td>
        <td>{building.lat}</td>
        <td>{building.lon}</td>
        <td>{building.building_number || '-'}</td>
        <td>{building.postcode || '-'}</td>
        <td>{building.note || '-'}</td>
      </tr>
    );
  }

  // Filter buildings based on year
  function filterBuildingsByYear(year) {
    const filteredBuildings = data.filter(building => {
      const buildingYear = new Date(building[0].timestamp).getFullYear();
      return buildingYear.toString() === year;
    });
    return filteredBuildings;
  }

  // Handle building selection change
  function handleBuildingChange(event) {
    const selectedValue = event.target.value;
    setSelectedBuilding(selectedValue);
    setSearchText('');
  }

  // Handle search input change
  function handleSearchInputChange(event) {
    const value = event.target.value;
    setSearchText(value);
    setSelectedBuilding('default');
  }

  // Extract unique building names from the data
  const buildingNames = Array.from(
    new Set(data.map(building => building[building.length - 1].name))
  );

  return (
    <div className="App">
      <h1>Building History Viewer</h1>
      <div className="container">
        <label htmlFor="searchInput">Keyword</label>
        <input
          type="text"
          id="searchInput"
          placeholder="Search for a keyword"
          value={searchText}
          onChange={handleSearchInputChange}
        />
        <label htmlFor="buildingDropdown">Select a Building:</label>
        <select
          id="buildingDropdown"
          value={selectedBuilding}
          onChange={handleBuildingChange}
        >
          <option value="default">Pick one</option>
          <option value="searchByYear">Search by Year</option>
          {buildingNames.map((name, index) => (
            <option key={index} value={name}>
              {name}
            </option>
          ))}
        </select>
        <table id="buildingTable">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Timestamp</th>
              <th>Version</th>
              <th>Amenity</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>Building Number</th>
              <th>Postcode</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            {selectedBuilding === 'searchByYear' ? (
              filterBuildingsByYear(searchText).map(building =>
                createTableRow(building[0])
              )
            ) : (
              data
                .filter(building =>
                  selectedBuilding === 'default'
                    ? true
                    : building[building.length - 1].name === selectedBuilding
                )
                .map(building => createTableRow(building[0]))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
