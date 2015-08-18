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

## System dependencies
1. python3
2. twisted
3. gdal

## To-Do List
- [ ] start tool for firing up the front-end
  - [ ] invoke later (with delay) a browser connected to this front-end
  - [ ] invoke twisted to handle the web events for the front-end
- [ ] ideal workflow step 1
  - [x] build a display to connect device to input
  - [ ] manipulate tracks
    - [ ] change labels
    - [ ] add descriptions
  - [ ] manipulate waypoints
    - [ ] change labels
    - [ ] add descriptions
