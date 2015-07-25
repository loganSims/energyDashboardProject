var GRAPH_LEGEND_FONT_SIZE = "14 px";

// Does what the function name says it does
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

// Fill the building title on the page based on the code, uses buildings.js for lookup
function fillBuildingTitle(buildingName, utilName, year) {
    // buildings should be in buildings.js, refactored to make gregs life easy
    preyear = year-1;
    $('#buildingName').text(buildingName + ": " + preyear  + "-" + year + " " + utilName);
}

/*Given a building code ("AOM") as wel as other parameters, gets the JSON representation of waste, etc.
INPUT
	building code	: three letter code that each building has been given to identify it
	utilCode		: the code used to identify the different utlities 
	svg1			: used for monthly graphs
	svg2			: used for yearly total graphs
	type			: can be either use or cost depending on which graph is being generated
	chart1			: chart for svg1
	chart2			: chart for svg2
	year			: the year that graphs are being generated for

*/
function getBuildingJSON(buildingCode, utilCode,  svg1, svg2, type, chart1, chart2, year) {

    console.log("getBuildingJSON called with " + buildingCode);

    if (buildingCode == "" || buildingCode == null) return;


    if (type == 'cost') {
        requestAddress = "https://" + window.location.host + "/cgi-bin/getCostData.py?code=" + buildingCode + "&util=" + utilCode + "&year=" + year;
    }
    if (type == 'use') {
        requestAddress = "https://" + window.location.host + "/cgi-bin/getUsageData.py?code=" + buildingCode + "&util=" + utilCode + "&year=" + year;
    }


    console.log(requestAddress);

    $.getJSON(requestAddress, function(response) {
        console.log("AJAX response recieved");

        //make monthly graph
        jsonData1 = transformJsonToGraphData(response);
        makeGraph(jsonData1, response.unit, svg1, chart1);

        //make total graph
        jsonData2 = transformJsonToGraphDataYear(response);
        makeGraph(jsonData2, response.unit, svg2, chart2);

	//make the usage pie chart.
        if (type == 'use') {
            normalizedPiData = transformJsonToPieChartData(response);
            makePieChart(normalizedPiData);
        }

    });
}

function getBuildingScreenShotJSON(buildingCode, utilCode, svg1, type, chart1, year) {

    console.log("getBuildingJSON called with " + buildingCode);

    if (buildingCode == "" || buildingCode == null) return;


    if (type == 'cost') {
        requestAddress = "https://" + window.location.host + "/cgi-bin/getCostData.py?code=" + buildingCode + "&util=" + utilCode + "&year=" + year;
    }
    if (type == 'use') {
        requestAddress = "https://" + window.location.host + "/cgi-bin/getUsageData.py?code=" + buildingCode + "&util=" + utilCode + "&year=" + year;
    }


    console.log(requestAddress);

    $.getJSON(requestAddress, function(response) {
        console.log("AJAX response recieved");

        //make monthly graph
        jsonData1 = transformJsonToGraphData(response);
        makeGraph(jsonData1, response.unit, svg1, chart1);

	//make the usage pie chart.
        if (type == 'use') {
            normalizedPiData = transformJsonToPieChartData(response);
            makePieChart(normalizedPiData);
        }

    });
}
/*
Transforms a json object to a graph data object for graphing year total values
Sets the current year and preious years values. 

INPUT:
	json	: json object

RETURN: graph data object for year totals


*/

function transformJsonToGraphDataYear(json) {
    //numberOfYears = json.years.length;
    numberOfYears = 1;
    currentYear = json.currYear;
    previousYear = json.prevYear;

    console.log("Number of utilities is: " + numberOfYears);
    console.log("Current year is: " + currentYear);
    console.log("Prev year is: " + previousYear);

    data = [];

    for (i = 0; i < numberOfYears; i++) {
        year = json;
        data.push({
            "Month": " ",
            "Year": currentYear,
            "Value": json.posttotal
        });
        data.push({
            "Month": " ",
            "Year": previousYear,
            "Value": json.pretotal
        });
    }

    console.log(data);

    return data;
}


/* 
Transform a json object to a graph data object for monthly totals
Sets the month total for the current years as well as previous year.

INPUT:
	json	: json object


RETURN: graph data object for year totals

Sets the current year and preious years values. 
*/

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
        if ((month.post != 0) && (month.pre != 0)) {
            console.log("Month: " + month.name + " Year: " + currentYear + " Value: " + month.post);
            console.log("Month: " + month.name + " Year: " + previousYear + " Value: " + month.pre);
            data.push({
                "Month": month.name,
                "Year": currentYear,
                "Value": month.post
            });
            data.push({
                "Month": month.name,
                "Year": previousYear,
                "Value": month.pre
            });
        }
    }

    console.log(data);

    return data;
}

/* 
Transform a json object to a graph data object that holds the total for the individual building
as well as the total for all the other buildings on campus excluding the building your viewing. 

INPUT:
	json	: json object
	
RETURN: graph data object for building total and all other buildings total.
*/

function transformJsonToPieChartData(json) {
    posttotal = json.posttotal;
    postGrandTotal = json.postGrandTotal;
    building = json.name;

    data = [{
        "label": building.toString(),
        "value": posttotal,
		  "color": "#003F87"
    }, {
        "label": "Other Buildings",
        "value": postGrandTotal,
		  "color": "#339cde"
    }];


    return data;
}


/* 

Creates the pie chart  assigning data , size, labels and colors ofthe graph.

INPUT:
	json: json object

*/


function makePieChart(json) {
    var pie = new d3pie("#pieChart", {
    data: {
        content: json
          },
    size: {
         canvasHeight: 400,
         canvasWidth: 400
  	 },
    labels: {
        outer: {
            pieDistance: 20
        },
        mainLabel: {
            fontSize: 13,
            font: "verdana"
        },
        percentage: {
            color: "#ffffff",
            decimalPlaces: 2, 
            fontSize: 20


        },
        value: {
            color: "#FFFFFF",
            fontSize: 18
        },
        lines: {
            enabled: true
        },
        truncation: {
            enabled: false
        }
    }
    });
}


/*
 Make and show the graph
 
 INPUT:	
 	json			: json object
 	unit			: unit response from AJAX call
 	svg				: used with creating graph
 	chartcontainer	: chart value
*/
function makeGraph(json, unit, svg, chartcontainer) {
    // Change title of page to building name
    var buildingName = json.displayName;

    chart = new dimple.chart(svg, data);

    var postyear = json[0].Year;
    var preyear = json[1].Year;

    //chart.assignColor(postyear, "#0083D6", "#0083D6", .75);
    //chart.assignColor(preyear, "#003F87", "#003F87", .75);
    chart.assignColor(postyear, "#0083d6", "#0083d6", 1);
    chart.assignColor(preyear, "#003f87", "#003f87", 1);

    // Bind data to axes
    x = chart.addCategoryAxis("x", ["Month", "Year"]);
    x.addGroupOrderRule("Year", false);
    y = chart.addMeasureAxis("y", "Value");
    x.fontSize = 20;
    y.fontSize = 20;

    // Make bar chart 
    s = chart.addSeries("Year", dimple.plot.bar);
    s.addOrderRule("Year", false);
    // Order alphebetically by Consumable
    x.addOrderRule(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]);

    // No x label because it's obvious
    x.title = null;
    y.title = unit;

    legend = chart.addLegend(200, 5, "100%", 40, "left", s);
    legend.fontSize = 15;

    chart.setBounds(90, 20, 300, 300);

    console.log("drawing chart");
    chart.draw();

}

/*
This function is called when a builfing is selected from
the main menu. 

It first gets the information needed about the selected building
and it's util. This information comes from a python script.

it then calls drawGraph to set up all the graphs.
*/

function makeDashboard(buildingCode, util, buildingName, year) {
 
    requestAddress = "https://" + window.location.host +
        "/cgi-bin/getBuildingDesc.py?code=" +
        buildingCode + "&util=" + util;

    $.getJSON(requestAddress, function(response) {
        console.log("building description recieved");
        drawGraph(buildingCode, util, buildingName, year, response);

    });

}
/*
takes in the current year the user is viewing on the dashboard.
buildingCode is passed for buildings that dont have backlog to 2011
like most buildings.
*/
function makeYearSelect(currentYear, buildingCode) {

    var date = new Date();
    var year = date.getFullYear();
    var select = [];
	var oldestYear = 2011
	
	if (buildingCode == "aFR"){
        oldestYear = 2013;
    }
	
    select.push('<u></u> <select id="yearSelect">');
    while (year - 1 >= oldestYear) {
        if (currentYear == year) {
            select.push('<option value="' + year + '" selected="selected">' + (year - 1) + '-' + year + '</option>');
        } else {
            select.push('<option value="' + year + '">' + (year - 1) + '-' + year + '</option>');
        }
        year--;
    }
    select.push('</select id="yearSelect">');
    console.log("select html " + select.join(""));
    return select.join("");

}

//constructs utility menu for each buildings dashboard
function makeUtilRadio(util, code) {
   
    var utils = new Array("electric", "steam");

    //TODO aCS (Campus Services) is the only building we track
    // that we dont have usage for

    // sFC (fairhaven commons) has it's elec usage in Fairhaven towers
    if (code == 'aCS' || code == "sFC"){
        utils = new Array("electric");
    }

    var radios = '<u></u> ';

    for (i = 0; i < utils.length; i++) {
        if (utils[i] == util) {
            radios = radios + '<input type="radio"  id="' + utils[i] + '"name="utilSelect" value="' + utils[i] + '" checked>';
        } else {
            radios = radios + '<input type="radio"  id="' + utils[i] + '"name="utilSelect" value="' + utils[i] + '">';
        }
        radios = radios + '<label for="' + utils[i] + '">' + utils[i] + '</label>';
    }
    return radios;
}

/* Given a building code, draws a graph.
   Writes up html on the fly for the dashboard page
   passes its params on to getBuildingJSON for the
   JSON object
*/
function drawGraph(buildingCode, util, buildingName, year, info) {

    $('#content').empty();

    //if year null set to current year. That will happen when called from main menu
    if (year == null) {
        console.log("year null, setting to current -1 ");
        var date = new Date();
        year = date.getFullYear();
    }
    var yearSelect = makeYearSelect(year, buildingCode);
    var utilRadio = makeUtilRadio(util, buildingCode);

    html = '<div id="chartContainer">' +
        '<h1 id="buildingName" align="center" style="font-family: sans-serif"></h1><br>' +
        //function used in dashboard dynamic page for changing graphs. needed to pass years around.   
        '<script> function changeGraph() {' +
        '   var year = document.getElementById("yearSelect").value;' +
        '   var radios = document.getElementsByName("utilSelect");' +
        '   for (var i = 0; i < 4; i++){' +
        '     if (radios[i].checked){' +
        '       var util = radios[i].value;' +
        '       break;' +
        '     }' +
        '   }' +
        '   makeDashboard("' + buildingCode + '", util, "' + buildingName + '", year);' +
        '}  ' +
        '</script> ' +
        //menu
        '<div id="utilmenu">' +
        '<nav>' +
        utilRadio +
        yearSelect +
        '<br><br>' +
        '<button onclick="javascript:changeGraph()">Generate Dashboard</button>' +
        '</nav>' +
        '</div>' +
        '<br>' +
        //chart section  
        '<div id="chart">' +
        //add chart id for each new chart!
        '<div id="info">' +
        '<h3 align="left" > Building Information </h3>' +
        //get buidling info strings here.
        info.buildingInfo +
        '<h3 align="left" > About the units </h3>' +
        info.utilInfo +
        '</div id="info">' +
        '<div id="pieChart">' +
        '<h3 align="center" >Building\'s Usage vs. All Other Tracked Buildings For  '+ year +' </h3>' +
        '</div id="pieChart">' +
        '<div id="chart1">' +
        '<h3 align="center" >'+ buildingName +' Monthly Usage </h3>' +
        '</div id="chart1">' +
        '<div id="chart2">' +
        '<h3 align="center" >'+ buildingName +' Usage Totals </h3>' +
        '</div id="chart2">' +
        '<div id="chart3">' +
        '<h3 align="center" >'+ buildingName +' Monthly Cost </h3>' +
        '</div id="chart3">' +
        '<div id="chart4">' +
        '<h3 align="center" >'+ buildingName +' Cost Totals </h3>' +
        '</div id="chart4">' +
        '</div id="chart">' +
        '</div>';

    $('#content').append(html);
    fillBuildingTitle(buildingName, util, year);
    // svg for monthly and total year usage
    var svg1 = dimple.newSvg("#chart1", 450, 400);
    var svg2 = dimple.newSvg("#chart2", 450, 400);
    var svg3 = dimple.newSvg("#chart3", 450, 400);
    var svg4 = dimple.newSvg("#chart4", 450, 400);

    // Request JSON building data
    //must pass in the svg and chart container ID

    getBuildingJSON(buildingCode, util, svg1, svg2, 'use', '#chart1', '#chart2', year);
    getBuildingJSON(buildingCode, util, svg3, svg4, 'cost', '#chart3', '#chart4', year);

    //changeBackground(buildingCode);
}

// Given a building code, draws a graph
// writes up html for the building page
function drawScreenShotGraph(buildingCode, util, buildingName, year) {

        var date = new Date();
        year = date.getFullYear();

html = '<div id="chartContainer">' +


        '<h1 id="buildingName" align="center" style="font-family: sans-serif"> </h1><br>' +
        //chart section  
        '<br>' +
        '<div id="chart">' +
        '<div id="chart1">' +
        '<h3 align="center" > Monthly Usage </h3>' +
	'<h3 align="center" > How we\'re doing vs. last year </h3>' +
        '</div id="chart1">' +
        '<div id="pieChart">' +
        '<h3 align="left" >Building\'s Usage vs. Other Buildings</h3>' +
        '</div id="pieChart">' +
        '<div id="info">' +
	'<h3> Scan the QR code to go to the Energy Dashboard website! </h3>' +
        '</div id="info">' +
        '</div id="chart">' +
        '</div>';

    $('#content').append(html);


    fillBuildingTitle(buildingName, util, year);
    // svg for monthly and total year usage
    var svg1 = dimple.newSvg("#chart1", 400, 450);
    
    // Request JSON building data
    //must pass in the svg and chart container ID

    getBuildingScreenShotJSON(buildingCode, util, svg1, 'use', '#chart1',  year);

}

