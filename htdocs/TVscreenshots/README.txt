PhantomJS is required to make this screenshot thing work.

http://phantomjs.org/download.html

Inside buildingScipts are .sh files for each building and a util. 
When a new screenshot is needed simply run the script for the 
needed building. The image will be saved in buildingImages folder.

example:
>/buildingScripts/sh <buildingName>.sh

When adding new buildings make sure to follow format of other sh scripts!

Also if any directory name or file name is changed make sure to update NewScreenShot.js
with those changes!

*make sure url in NewScreenShot.js is correct once site has a home.
