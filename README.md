# HikingJournal
Blend text, notes, voice, gpx, and USGS quads to make an entry in the journal

## Ideal workflow[software] would be:
1. strip tracks/waypoints from GPS              [read.py][Import]
  1. change track labels
  2. add track descriptions
  3. change waypoint labels
  4. add waypoint descriptions

2. plot tracks/waypoints on PDF                 [plot.py][Metadata]
  1. change track labels
  2. change track descriptions
  3. change waypoint labels
  4. change waypoint descriptions

3. bind track data to photographs               [bind.py][Metatdata]
  1. change track labels
  2. change track descriptions
  3. change waypoint labels
  4. change waypoint descriptions
  5. add picture description (captions)

4. put diary account to all of the above        [note.py][Scribe Entry]
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
- [x] start tool for firing up the front-end
  - [x] invoke later (with delay) a browser connected to this front-end
  - [x] invoke cherrypy/flask to handle the web events for the front-end
- [x] ideal workflow step 1
  - [x] build a display to connect device to input
  - [x] manipulate tracks
    - [x] change labels
    - [x] add descriptions
  - [x] manipulate waypoints
    - [x] change labels
    - [x] add descriptions
  - [x] redirect back to cover of journal
- [x] database
  - [x] determine if it needs GIS database *no, but can hook one in later if need be just to do GIS relational junk*
  - [x] define storage structure
    - use Python shelve
    - use the md5 checksum as the keyword
    - value is the type of data contained in the md5 checksum
    - data is stored in **wdir** from the config file
- [ ] manage metadata
  - [x] ideal workflow step 2
    - [x] find Quad map(s) associated with a route, track, or waypoint
      - [x] search local db for map
      - [x] search usgs for map *can only do this manually*
    - [x] find waypoints that go along with track
      - [x] manually remove them
      - [x] manually add them
      * Note: because it takes so long to generate the map, it will not be updated when the waypoint list changes
    - [x] change descriptions and labels for all data involved (reuse import.js?)
  - [ ] be able to click on map and get to gps info rather than successor/previous
  - [ ] ideal workflow step 3
    - [ ] add pictures from file system : in-place reference?
    - [ ] correlate pictures with tracks via time
  - [x] bind all metadata annotations for scribing an entry
- [ ] ideal workflow step 4
  - [x] define: an entry is one or more annotated tracks that make up a journey.
  - [ ] define the language to scribe in
    - [ ] markdown? *markdown seems more popular than XML*
    - [x] yet another markdown? *hijack markdown with CSS*
    - [x] xml (with schema) and CSS? *Not recommended by W3*
    - [x] xml (with schema) and XSLT? *XML too verbose*
    - [x] xml (with schema) and JavaScript? *XML too verbose*
    - [ ] something else?
