# PolarSteps/InfluxDB to gpx Parser
This script parses the GPS file from your exported Polarsteps or InfluxDB data to a gpx 1.0 scheme.

This could be a helpful tool in many different scenarios, but I created it to be able to use the gps trackpoints from Polarsteps to automatically geotag my photos in Adobe Lightroom (which only accepts gpx tracklogs). <a href="https://helpx.adobe.com/lightroom/help/maps-module.html#timezone_offset_auto_tag" target="_blank">Read here how to use tracklogs to auto-tag your photos in Lightroom</a>
Note that the script assumes that the unix time stamps are in the GMT+0 time zone, therefore you may need to compensate for the time set in your camera. Lightroom has the option to do this.

The script may not contain the most elegant or robust code, but it was very useful to me, and may be useful to you too. 

## InfluxDB
Since I also log my phone's coordinates to InfluxDB (via HomeAssistant), I also added the functionality to convert this gps data to the gpx scheme. 

It assumes that the csv files are influxdb exports and that the gpx data is formatted like:

    "time","state.mean_latitude","state.mean_longitude"
    "2022-07-19T17:29:00.000+02:00","54.2820671","9.7710714"
    "2022-07-19T17:30:00.000+02:00","54.2963866","9.759142266666666"
    "2022-07-19T17:31:00.000+02:00","54.3107061","9.747213133333334"
The header is skipped, so the specific format doesn't matter there.
