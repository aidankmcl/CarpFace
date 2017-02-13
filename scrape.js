/*
To use, install casperjs (npm install -g casperjs) and run:
casperjs scrape.js
*/

var casper = require('casper').create();
casper.start('https://lists.olin.edu/mailman/private/carpediem/');

casper.then(function() {
	console.log(this.getPageContent());
    console.log("just clicked");
	document.querySelector('input[name="username"]').setAttribute('value', "aidan.mclaughlin@students.olin.edu");
	document.querySelector('input[name="password"]').setAttribute('value', "Kyle5953");
    this.click('[name="submit"]');
});

casper.then(function() {
	console.log("made it");
	console.log(this.getCurrentUrl());
});

casper.run();