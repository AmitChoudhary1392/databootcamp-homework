// from data.js
var UfoData = data;


//create function for data entry into table
function appendTable(tableData) {
    tableData.map((ufo) => {
        
        //reference for table body to add row
        var row =d3.select('tbody').append('tr');

        //populate table rows
        Object.values(ufo).forEach((detail)=> {
        
            row.append('td').text(detail);
        });
        
    });
}

//import data into the table
//UfoData.forEach(appendTable);
appendTable(UfoData);

// Part 1: Use a date form in your HTML document and write JavaScript code that will listen for events and search through the date/time column to find rows that match user input.

// // Click event of datetime filter
/* var filter = d3.select("#filter-btn");
filter.on("click", function() {

    // Remove existing table
    d3.select("tbody").html("");

    // Prevent the page from refreshing
    d3.event.preventDefault();

    // Get the value property of the input element
    var dateTime = d3.select("#datetime").property("value");
    console.log(dateTime);

    // Filter reports
    var filteredData = UfoData.filter(record => record.datetime === dateTime);
    console.log(filteredData)

    // Display the filtered dataset
    //filteredData.forEach(appendTable);
    appendTable(filteredData)

}); */


// Part 2: Using multiple input tags and/or select dropdowns, write JavaScript code so the user can set multiple filters 
//and search for UFO sightings using the following criteria based on the table columns: date/time, city, state, country, shape

// Click event of datetime filter
var filter = d3.select("#filter-btn");

// Filter data when clicking
filter.on("click", function() {

    // Remove existing table
    d3.select("tbody").html("");

    // Prevent the page from refreshing
   d3.event.preventDefault();
    
    var appliedFilters={};

////*********************************longer version of code****************************************************** */

    // Get the value property of the input element
    //console log to check the filter selected

    /* var dateTime = d3.select("#datetime").property("value").trim();
    console.log(`Date: ${dateTime}`);
    
    var city = d3.select("#city").property("value").toLowerCase().trim();
    console.log(`City: ${city}`);
        
    var state = d3.select("#state").property("value").toLowerCase().trim();
    console.log(`State: ${state}`);
    
    var country = d3.select("#country").property("value").toLowerCase().trim();
    console.log(`Country: ${country}`);
    
    var shape = d3.select("#shape").property("value").toLowerCase().trim();
    console.log(`Shape: ${shape}`);
    appliedFilters={"datetime":datetime,
                    "city":city,
                    "state":state,
                    "country":country,
                    "shape":shape}; */

//************************************************************************************** */    

    //Select all input forms from user
    var inputs=d3.selectAll('input');

    //identify the filters applied and store them in an object
    inputs.nodes().forEach(input=>{
        var key=input.getAttribute('id');
        var value=input.value.toLowerCase().trim();
        console.log(`Filter Applied on ${key}: ${value}`);
        appliedFilters[key]=value;
        
    });

    //delete the filter keys with no input values
    Object.entries(appliedFilters).forEach(([key,value])=>{
        if (value===""){
            delete appliedFilters[key];
        };
    });

    console.log(appliedFilters);

    // Filter records based on applied filters
    var filteredData = UfoData.filter(record => {

        return Object.entries(appliedFilters).every(([key, value])=>{
            
            return record[key]===value;
        });
    });   

    console.log(filteredData);


     // Display the filtered dataset
     var flag = d3.select("#no-matching-flag");

     flag.html("");
    
     //no matching records
     if (filteredData.length === 0) {
         var row = flag.append("h3");
         row.text("No matching record.");
    
     }
     //records found, append table
     else {
         appendTable(filteredData);
     }
     
}); 




