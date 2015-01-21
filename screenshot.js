var page = require('webpage').create();
page.viewportSize = { width: 2000, height: 2000 };
page.open('http://140.160.141.163/website/?building=AI', function (status) {
    if (status !== 'success') {
        console.log('Unable to access the network!');
    } else {
        page.evaluate(function () {
            var body = document.body;
            body.style.backgroundColor = '#fff';
            body.querySelector('div#title-block').style.display = 'none';
            body.querySelector('form#edition-picker-form').parentElement.parentElement.style.display = 'none';
        });
        page.render('technews.png');
    }
    phantom.exit();
});
