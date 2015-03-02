# HikingJournal
Blend text, notes, voice, gpx, and USGS quads to make an entry in the journal

## Ideal workflow[software] would be:
1. strip tracks/waypoints from GPS              [read.py]
  1. change track labels
  2. add track descriptions
  3. change waypoint labels
  4. add waypoint descriptions

2. plot tracks/waypoints on PDF                 [plot.py]
  1. change track labels
  2. change track descriptions
  3. change waypoint labels
  4. change waypoint descriptions

3. bind track data to photographs               [bind.py]
  1. change track labels
  2. change track descriptions
  3. change waypoint labels
  4. change waypoint descriptions
  5. add picture description (captions)

4. put diary account to all of the above        [note.py]
  1. change track labels
  2. change track descriptions
  3. change waypoint labels
  4. change waypoint descriptions
  5. change picture description (captions)
  6. add/edit the story


## Packages
- hj.device
> Modules to make various GPS devices behave as a file system. Simple to do when they already are a file system, but not so obvious when they connect via serial port.
- hj.fe
- hj.tool
- hj..util

## System dependencies
1. python3
2. twisted
3. gdal
