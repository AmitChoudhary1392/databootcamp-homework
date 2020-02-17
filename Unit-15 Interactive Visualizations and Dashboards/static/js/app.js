//initialise function for default dashboard
function init(){
    
    //import JSON data
    d3.json('samples.json').then(function(data){
       
        //create variable to store unique test subject IDS
        var sampleIDs = [];
        data.names.forEach((record) => {
            if (!(sampleIDs.includes(record))) {
                sampleIDs.push(record);
            };
        });
        console.log(sampleIDs);
       
        // select HTML element to append Test subject ID NOs
        var sampleIDsMenu = d3.select('#selDataset');
        
        //append dropdown menu for test subjects
        sampleIDs.forEach((record) => {
            var item = sampleIDsMenu.append("option")
                                    .text(record)
                                    .property('value',record);
        });
       
        //default graphs and data on the dashboard
        metaData(sampleIDs[0]);
        drawChart(sampleIDs[0]);
        
        //event listener
        sampleIDsMenu.on('change', function(){
            //interactive visualisations for selected test subject
            metaData(this.value);
            drawChart(this.value);
        });

    });

};


function metaData(sampleID){

   // import json data
    d3.json('samples.json').then(function(data){
                
        //select HTML element for populating metadata
        var metaDataTab = d3.select('#sample-metadata').html('');

         //use d3 to select the HTML element for gauge plot
        var gaugeChart= d3.select("#gauge").html("");

        //Select metadata to append
        Object.entries(data.metadata).forEach(([key, value])=>{
           
            if(value.id==sampleID){
                        
                Object.entries(value).forEach(([k,v])=>{
                        metaDataTab.append('p')
                                   .text(`${k}: ${v}`);
                                    
                }); 
                
                var wfreq = value.wfreq ;

                // Trig to calc meter point
                var degrees = 180 - (wfreq*20),
                    radius = .5;
                var radians = degrees * Math.PI / 180;
                var x = radius * Math.cos(radians);
                var y = radius * Math.sin(radians);

                // Path: create a  triangle for pointer
                var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
                    pathX = String(x),
                    space = ' ',
                    pathY = String(y),
                    pathEnd = ' Z';
                var path = mainPath.concat(pathX,space,pathY,pathEnd);

                var data = [{ type: 'scatter',
                    x: [0], y:[0],
                    marker: {size: 28, color:'850000'},
                    showlegend: false,
                    //name: 'BellyButtonDiversity ',
                    text: `Wfreq: ${wfreq}`,
                    hoverinfo: 'text'},
                    {mode:'gauge+number', 
                    value:wfreq,
                    values: [50/9,50/9,50/9,50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50],
                    rotation: 90,
                    text: ['8-9','7-8','6-7', '5-6', '4-5', '3-4',
                            '2-3', '1-2', '0-1',''],
                    textinfo: 'text',
                    textposition:'inside',
                    hoverinfo:'text',
                    marker: {colors:['rgba(14, 127, 0, .5)', 'rgba(110, 154, 22, .5)',
                                        'rgba(170, 202, 42, .5)', 'rgba(202, 209, 95, .5)',
                                        'rgba(210, 206, 145, .5)', 'rgba(232, 226, 202, .5)',
                                        'rgba(255,237,160,0.6)','rgba(255,255,178,0.6)',
                                        'rgba(237,248,177,0.4)','rgba(255, 255, 255, 0)']},
                    hole: .5,
                    type: 'pie',
                    showlegend: false
                }];

                var layout = {
                    shapes:[{
                        type: 'path',
                        path: path,
                        fillcolor: '850000',
                        line: {
                        color: '850000'
                        }
                    }],
                    title: '<b>Belly Button Washing Frequency</b> <br> Scrubs per week.',
                    height: 600,
                    width: 600,
                    xaxis: {zeroline:false, showticklabels:false,
                            showgrid: false, range: [-1, 1]},
                    yaxis: {zeroline:false, showticklabels:false,
                            showgrid: false, range: [-1, 1]}
                };

                Plotly.newPlot('gauge', data, layout);                         
            }; 
        }); 
    });
};

function drawChart(sampleID) {
    console.log("buildchart function triggered");

   // Use `d3.json` to fetch the sample data for the plots
   d3.json('samples.json').then(function(response){
        
    //use d3 to select the HTML element for bubble plot
    var bubble = d3.select('#bubble').html('');
    //use d3 to select the HTML element for bar plot
    var barChart= d3.select("#bar").html("");
       
    var combined_data=[];

    Object.entries(response.samples).forEach(([key,value])=>{
        
        if (value.id==sampleID){
            
            //for creating horizontal bar chart
            combined_data.push({
                otu_ids: value.otu_ids,
                otu_labels: value.otu_labels,
                sample_values:value.sample_values
            });
            
            var sorted_data= combined_data.sort(function(a,b){
                return b.sample_values-a.sample_values;
            });                 /// sorting can be ignored in this case, as data is already sorted

            console.log(sorted_data[0]);

            //select top 10 results
            var sorted_ids = sorted_data[0].otu_ids.slice(0,10);
            var sorted_labels = sorted_data[0].otu_labels.slice(0,10);
            var sorted_values = sorted_data[0].sample_values.slice(0,10);

            console.log(sorted_ids);
            console.log(sorted_values);
            console.log(sorted_labels);
                                            
              var trace_bar = [{
                x: sorted_values.reverse(),             // since data is already sorted, lines 86 to 104 can be ignored AND instead value.sample_values can be used directly
                y: sorted_ids.reverse().map(id=>{return 'OTU '+ id}),       // since data is already sorted, lines 86 to 104 can be ignored AND instead value.Otu_ids can be used directly
                type: 'bar',
                marker: {
                  color: 'rgba(50,171,96,0.6)',
                  line: {
                    color: 'rgba(50,171,96,1.0)',
                    width: 1
                  }
                },
                orientation: 'h',
              }];

              var layout_bar = {
                  title: `Top 10 OTU in Test Subject ${sampleID}`,
                  xaxis: {
                  range: [0, sorted_values],
                  domain: [0, 0.8],
                  zeroline: true,
                  showline: false,
                  showticklabels: true,
                  showgrid: true
                },

                margin: {
                  l: 70,
                  r: 10,
                  t: 40,
                  b: 70
                },
                width: 400,
                height: 600,
                paper_bgcolor: 'rgb(248,248,255)',
                plot_bgcolor: 'rgb(248,248,255)',

              };
            Plotly.newPlot("bar", trace_bar, layout_bar,{responsive:true});
            
            //define trace for bubble scatter plot
            var trace_bubble = [{
                    type: "Scatter",
                    name: "Belly Button Bubble Chart",
                    x:value.otu_ids,    //array of otu_ids
                    y:value.sample_values,      //array of sample_values
                    mode:'markers',
                    marker:{
                            color:value.otu_ids,
                            size:value.sample_values.map(element=>element/1.2),
                            colorscale:'Portland'
                            },          
                    hovertext:value.otu_labels
            }];
        
            //define layout for bubble chart
            var layout_bubble = {
                title: "Belly Button Diversity Bubble Chart",
                autosize: true,
                xaxis:{
                    title: 'OTU ID',
                    zeroline: false
                    },
                yaxis: {
                    title: ''
                    }
                
            };
        
            Plotly.newPlot("bubble", trace_bubble, layout_bubble,{responsive:true});
        };

    });
 
    });
};

init();