// API call to USGS API to get earthquake data
var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";

var platespath="GeoJSON/PB2002_boundaries.json";

var colors=["#bd0026","#f03b20","#fd8d3c","#feb24c","#fed976","#ffffb2"]

// GET request to the query URL
d3.json(queryUrl, function(data) {
    
  console.log(data),
  createFeatures(data.features);
});

function createFeatures(earthquakeData) {

  // each feature a popup describing with information
  function onEachFeature(feature, layer) {
    layer.bindPopup("<h3 > Magnitude: "+ feature.properties.mag + 
      "</h3><h3>Location: " + feature.properties.place +
      "</h3><hr><h3>" + new Date(feature.properties.time) + "</h3>" );
  }

  // GeoJSON layer containing the features
  // Run the onEachFeature function once for each piece of data in the array
  var earthquakes = L.geoJSON(earthquakeData, {
    onEachFeature: onEachFeature,
    pointToLayer : pointToLayer
  });

 
  createMap(earthquakes);
}

function getColor(magnitude){
  
  return magnitude >= 5 ?  "#bd0026"  :
  magnitude >= 4 ? "#f03b20":
      magnitude >= 3 ? "#fd8d3c" :
          magnitude >= 2 ?"#feb24c" :
              magnitude >= 1 ? "#fed976":
                 "#ffffb2";

}

// Create Circles with a light gray circumferance line!
function pointToLayer(feature,latlng) {
  
    return new L.circle(latlng, {
        stroke: true,
        color: "blue",
        weight: .4,
        fillOpacity: .6,
        fillColor: getColor(feature.properties.mag),
        radius:  feature.properties.mag * 35000
    })
}

function createMap(earthquakes) {

  // satellite map
  var satelliteMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors,\
    <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.satellite",
    accessToken: API_KEY
    });

  // light and dark map visualization
  var streetMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
  //var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, \
    <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery A© <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 15,
    id: "mapbox.light",
    accessToken: API_KEY
  });

  
  var darkMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, \
    <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery A© <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 15,
    id: "mapbox.dark",
    accessToken: API_KEY
  });

  //outdoors map
  var outdoorsMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution:"Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, \
    <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery A© <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.outdoors",
    accessToken: API_KEY
  });

  // plates layer
  d3.json(platespath, function(platesData){
    // Tectonic plates layer
    var platesStyle = {
    "color": "#ff7800",
    "weight": 2,
    "opacity": 1,
    fillOpacity: 0,
    };
    var plates = L.geoJSON(platesData, {
    style: platesStyle
    });
  

  // Define a baseMaps object
  var baseMaps = {
    "Light Map": streetMap,
    "Dark Map": darkMap,
    "Satellite": satelliteMap,
    "Outdoors": outdoorsMap
  };

  // Create overlay object 
  var overlayMaps = {
    "Earthquakes": earthquakes,
    "Fault Lines":plates
  };

  // Create our map
  var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 4,
    layers: [streetMap, earthquakes]
  });

  // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: true
  }).addTo(myMap);

  // Setting up the legend
  var legend = L.control({ position: "bottomright" });

  legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var limits = ["5+", "4-5", "3-4", "2-3", "1-2", "0-1"];
    var labelsColor = [];
    var labelsText = [];

    // Add min & max
    limits.forEach(function(limit, index) {
        //labelsText.push(`<span class="legend-label">${limits[index]}</span>`)
        labelsColor.push(`<li style="background-color: ${colors[index]};"><span class="legend-label">${limits[index]}</span></li>`); // <span class="legend-label">${limits[index]}</span>
        
    });

    //var labelsTextHtml = `${labelsText.join("<br>")}`;

    var labelsColorHtml =  "<ul>" + labelsColor.join("") + "</ul>";
    
    var legendInfo = "<h4>Earthquake<br>Magnitude</h4>" +
        "<div class=\"labels\">" +labelsColorHtml+"</div>";
    div.innerHTML = legendInfo;

   return div;
 };

    // Adding legend to the map
    legend.addTo(myMap);

})

};