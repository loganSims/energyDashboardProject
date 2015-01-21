var system = require('system');
if (system.args.length === 1) {
    console.log('Try to pass some args when invoking this script!');
} 

var buildingName = system.args[1];

console.log("loading the GEF website!");
var page = require('webpage').create();


var url = 'http://140.160.141.163/website/ScreenShot.html?building=' + buildingName;
page.viewportSize = { width: 1366, height: 786 };
page.open(url, function (status) {
    if (status !== 'success') {
        console.log('Unable to access the network!');   
		 phantom.exit();
    } else {
		window.setTimeout(function () {
			page.render('GEF.png');
			console.log("done!");
			phantom.exit();
		}, 5000);
    }
});
