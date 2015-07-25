var system = require('system');
if (system.args.length === 1) {
    console.log('Try to pass some args when invoking this script!');
} 

var buildingName = system.args[1];
var buildingCode = system.args[2];
var util = system.args[3];
var date = new Date();
var year = date.getFullYear();
var month = date.getMonth();

console.log("loading the Energy DashBoard website!");
var page = require('webpage').create();

var url = 'http://sw.cs.wwu.edu/~simsl/ScreenShot.html?name='+
           buildingName + '&code=' + buildingCode + '&util=' +
           util;

page.viewportSize = { width: 1366, height: 768 };
page.open(url, function (status) {
    if (status !== 'success') {
        console.log('Unable to access the network!');   
		 phantom.exit();
    } else {
		window.setTimeout(function () {
			page.render('../buildingImages/' + 
                                     buildingName.replace("%20", " ") +'_'+ 
                                     util+'_'+ month + '-' + date.getFullYear()  + '.png');
			console.log("done!");
			phantom.exit();
		}, 5000);
    }
});
