var GRAPH_LEGEND_FONT_SIZE = "14 px";

// Given a building code ("OM"), get the JSON representation of waste, etc.
function getSummaryJSON(ResUse, StudUse, AcaUse, ResCost, StudCost, AcaCost, year) {

    console.log("getSummaryJSON called with ");

    requestAddress = "https://" + window.location.host + "/cgi-bin/dataSummary.py?year=" + year

    console.log(requestAddress);

    $.getJSON(requestAddress, function(response) {
        console.log("AJAX response recieved");

	     //make the usage pie charts.
        normalizedPiData = JsonToPieChartData(response.ResSteamUse, response.ResElectricUse);
        makePie(normalizedPiData, ResUse, "Resident Use");

	     //make the usage pie charts.
        normalizedPiData = JsonToPieChartData(response.ResSteamCost, response.ResElectricCost);
        makePie(normalizedPiData, ResCost, "Resident Cost");

	     //make the usage pie charts.
        normalizedPiData = JsonToPieChartData(response.StuSteamUse, response.StuElectricUse);
        makePie(normalizedPiData, StudUse, "Student Building Use");

	     //make the usage pie charts.
        normalizedPiData = JsonToPieChartData(response.StuSteamCost, response.StuElectricCost);
        makePie(normalizedPiData, StudCost, "Student Building Cost");

	     //make the usage pie charts.
        normalizedPiData = JsonToPieChartData(response.AcaSteamUse, response.AcaElectricUse);
        makePie(normalizedPiData, AcaUse, "Academic Building Use");

	     //make the usage pie charts.
        normalizedPiData = JsonToPieChartData(response.AcaSteamCost, response.AcaElectricCost);
        makePie(normalizedPiData, AcaCost, "Academic Building Cost");


    });
}


function JsonToPieChartData(steam, elec) {

    data = [{
        "label": "Steam",
        "value": steam,
	"color": "#003F87"
    }, {
        "label": "Electric",
        "value": elec,
	"color": "#339cde"
    }];


    return data;
}
function makePie(json, divTag, title) { 

    var pie = new d3pie(divTag, {

    data: {
        content: json,
    },
    size: {
         canvasHeight: 300,
         canvasWidth: 300
  	 },
    header:{
        title: {
           text: title,
           fontSize: 17,
	   font: "verdana"
        }
    },
    "labels": {
        "outer": {
            "format": "none",
        },
        "inner": {
            "format": "label",
        },
        "mainLabel": {
            "fontSize": 15,
	    "font": "verdana",
            "color": "#ffffff"
        },
        "percentage": {
            "color": "#ffffff",
            "decimalPlaces": 2, 
            "fontSize": 20
        },
        "lines": {
            "enabled": true
        },
        "truncation": {
            "enabled": false
        }
    },
    tooltips: {
      enabled: true,
      type: "placeholder",
      string: "{percentage}%",
      styles: {
        color: "#000000",
        fadeInSpeed: 500,
	backgroundOpacty: 0.8,
	backgroundColor: "#cce6f7",
	font: "verdana",
	fontSize: 20,
	padding: 10
      }
    }

    });
}


/* Given a building code, draws a graph.
   Writes up html on the fly for the dashboard page
   passes its params on to getBuildingJSON for the
   JSON object
*/
function makeSummaryDash() {

    var date = new Date();
    year = date.getFullYear();

    getSummaryJSON("#homeResUsageChart", "#homeStudUsageChart", 
		  "#homeAckUsageChart", "#homeResCostChart",
		  "#homeStudCostChart", "#homeAckCostChart", year);


}
