var GRAPH_LEGEND_FONT_SIZE = "14 px";

// Contains mappings of a building code -> image code
// If none is found, the building code is assumed to work
var imageMap = {
    "BT":"RC",
    "AI":"RC"
};

// Given a building code, changes the background in the container
function changeBackground(buildingCode) {
    console.log("changing background");

    var prePath = "images/";
    var image = prePath;
    
    if (imageMap.hasOwnProperty(buildingCode)) {
        image += imageMap[buildingCode];
    } else {
        image += buildingCode;
    }
    
    image += ".jpg";
    
    console.log("to " + image);
    console.log($('#chartContainer').css('background'));
    $('#chartContainer').css('background-image', 'url(' + image + ')');
    console.log($('#chartContainer').css('background'));
}

// Does what the function name says it does
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

// Fill the building title on the page based on the code, uses buildings.js for lookup
function fillBuildingTitle(buildingName, utilName) {
    // buildings should be in buildings.js, refactored to make gregs life easy
		$('#buildingName').text(buildingName + " - Utility: " + utilName);
}

// Given a building code ("OM"), get the JSON representation of waste, etc.
function getBuildingJSON(buildingCode, debug) {
    
    console.log("getBuildingJSON called with " + buildingCode);
    
    if (buildingCode == "" || buildingCode == null) return;

    //requestAddress = "http://" + window.location.host +  "/lookup?code=" + buildingCode;
    requestAddress = "http://" + '127.0.1.1' +  "/cgi-bin/excelparse.py?code=" + buildingCode;

    console.log(requestAddress);

   if (debug && window.location.host != '140.160.141.163') {
	var debugJSON = {
       "name":"ACADEMIC INSTRUCTION CTR",
       "code":"AI",
       "utility":"elec",
       "unit":"kWh",
       "data":"not Sure",

       //"currCo2":17639,
       //"prevCo2":44707,
       "months":[
          {
             "month":"jan",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"feb",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"mar",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"apr",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"may",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"jun",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"jul",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"aug",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"sep",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"oct",
             "pre":1653789,
             "post":1653182,
          },
          {
             "month":"nov",
             "pre":1653789,
             "post":1653182
          },
          {
             "month":"dec",
             "pre":1653789,
             "post":1653182
          }

       ],
       "prevYear":2013,
       "currYear":2014,
       "co2unit":"lbs"
    };
	data = transformJsonToGraphData(debugJSON);
	//normalizedData = normalizeGraphData(data);
	//makeGraph(normalizedData);
	makeGraph(data, debugJSON.unit);

	fillBuildingTitle(debugJSON.name, debugJSON.utility);
	//normalizedPiData = transformJsonToPieChartData(debugJSON);
	//makePieChart(normalizedPiData);
	return;
    }

    
    $.getJSON(requestAddress , function (response) { 
	console.log("AJAX respone recieved");
	jsonData = transformJsonToGraphData(response);
	jsonData = normalizeGraphData(jsonData);

	makeGraph(jsonData);     
        
        normalizedPiData = transformJsonToPieChartData(jsonData);
        makePieChart(normalizedPiData);
    });
}

// Normalize the graph data so that 2013 data shows 100% and 2014 is a percentage of
function normalizeGraphData(json) {
	for (i = 0; i < json.length; i += 2) {
		ratio =  json[i].Value / json[i + 1].Value;
		ratioRounded = Math.round(ratio * 100);
        
        // i plus one is 2013 value
        json[i + 1].Value = 100;
        json[i].Value = ratioRounded;

		console.log("ratio: " + ratio);
	}

	return json;
}
/*TODO maybe work on a pie chart
function transformJsonToPieChartData(json) {
    currentCo2 = json.currCo2;
    previousCo2 = json.prevCo2;
    currentYear = json.currYear;
    previousYear = json.prevYear;
    
    data = [
        {"label":previousYear.toString(), "value":previousCo2},
        {"label":currentYear.toString(), "value":currentCo2}
    ];
    
    return data;
}
*/
// Transform a json object to a graph data object
function transformJsonToGraphData(json) {
	numberOfMonths = json.months.length;
	currentYear = json.currYear;
	previousYear = json.prevYear;

	console.log("Number of utilities is: " + numberOfMonths);
	console.log("Current year is: " + currentYear);
	console.log("Prev year is: " + previousYear);
	
	data = [];
	
	for (i = 0; i < numberOfMonths; i++) {
		month = json.months[i];
		if (month.post == null) continue;
		console.log("Month: " + month.month + " Year: " + currentYear + " Value: " + month.post);
	   console.log("Month: " + month.month + " Year: " + previousYear + " Value: " + month.pre);
		data.push({ "Month":month.month, "Year":currentYear, "Value":month.post});
		data.push({ "Month":month.month, "Year":previousYear, "Value":month.pre});
	}
	
	console.log(data);
	
	return data;
}
/* TODO maybe work on a pie chart
function makePieChart(json) {
    var w = 200;
    var h = 200;
    var r = h/2;
    var color = d3.scale.category20c();

    var data = json;

    var vis = d3.select('#pieChart')
                .append("svg:svg")
                .data([data])
                .attr("width", w)
                .attr("height", h)
                .append("svg:g")
                .attr("transform", "translate(" + r + "," + r + ")");
    var arc = d3.svg.arc().outerRadius(r);
    var pie = d3.layout.pie().value(
        function(d){
            return d.value;
        });
    var arcs = vis.selectAll("g.slice")
                  .data(pie)
                  .enter()
                  .append("svg:g")
                  .attr("class", "slice");
    arcs.append("svg:path").attr("fill", 
        function(d, i){
            return color(i);
        })
        .attr("d", arc);
    arcs.append("svg:text").attr("transform", 
        function(d){
                d.innerRadius = 0;
                d.outerRadius = r;
                return "translate(" + arc.centroid(d) + ")";
        })
        .attr("text-anchor", "middle")
        .text( 
        function(d, i) {
            return data[i].label;}
        );
}
*/
// Make and show the graph
function makeGraph(json, unit) {
	// Change title of page to building name
	var buildingName = json.displayName;
	
	chart = new dimple.chart(svg, data);
	
    // TODO
    // We can change these commands to do mod arith on the year, if its even assign the one color, if its odd assign the other
    // I'm not sure where the dimple.chart.assignColor call is going...
	chart.assignColor("2013", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2014", "#005794", "#005794", .75);
	chart.assignColor("2015", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2016", "#005794", "#005794", .75);
	chart.assignColor("2017", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2018", "#005794", "#005794", .75);
	chart.assignColor("2019", "#6C6C6C", "#6C6C6C", .75);
	chart.assignColor("2020", "#005794", "#005794", .75);
	
	// Bind data to axes
	x = chart.addCategoryAxis("x", ["Month", "Year"]);
	x.addGroupOrderRule("Year");
	y = chart.addMeasureAxis("y", "Value");
    x.fontSize = GRAPH_LEGEND_FONT_SIZE;
    y.fontSize = GRAPH_LEGEND_FONT_SIZE;
	
	// Make bar chart 
	s = chart.addSeries("Year", dimple.plot.bar);
	
    containerWidth = $('#content').width();
    containerHeight = $('#chartContainer').height();
    titleHeight = $('#buildingName').height();
    
    width = containerWidth - 100;
    height = containerHeight - titleHeight - 150;
    
    console.log("container width is: " + containerWidth);
	// Width/height
	chart.width = width;
	chart.height = height;
    
	// Order alphebetically by Consumable
	x.addOrderRule("Year", true);
	
	// No x label because it's obvious
	x.title = null;
	y.title = unit;

	legend = chart.addLegend(500, 20, "100%", 400, "left", s);
	legend.fontSize = GRAPH_LEGEND_FONT_SIZE;
	
    console.log("drawing chart");
	chart.draw();
}

// Given a building code, draws a graph
function drawGraph(buildingCode, utilCode) {
    $('#content').empty();
    html = '<div id="chartContainer"><div id="pieChart"></div><div id="chart"><h1 id="buildingName" align="center" style="font-family: sans-serif"></h1></div></div>';
    $('#content').append(html);
   //display proper utility named based of utilcode
    //svg = dimple.newSvg("#chartContainer", 800, 550),
	svg = dimple.newSvg("#chart", "100%", "100%");	
	// Request JSON building data
	json = getBuildingJSON(buildingCode, utilCode, true);
   changeBackground(buildingCode);
}
