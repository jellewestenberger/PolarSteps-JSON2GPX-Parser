# PolarSteps-JSON2gpx-Parser
This script parses the GPS file from your exported Polarsteps data to a gpx 1.0 scheme.

This could be a helpful tool in many different scenarios, but I created it to be able to use the gps trackpoints from Polarsteps to automatically geotag my photos in Adobe Lightroom (which only accepts gpx tracklogs). <a href="https://helpx.adobe.com/lightroom/help/maps-module.html#timezone_offset_auto_tag" target="_blank">Read here how to use tracklogs to auto-tag your photos in Lightroom</a>
Note that the script assumes that the unix time stamps are in the GMT+0 time zone, therefore you may need to compensate for the time set in your camera. Lightroom has the option to do this.

The script may not contain the most elegant or robust code, but it was very useful to me, and may be useful to you too. 


