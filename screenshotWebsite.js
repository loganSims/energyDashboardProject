$( document ).ready(function() {
	buildingName = getParameterByName("building");
	console.log("Building name in querystring is " + buildingName);

	drawGraph(buildingName);
});
