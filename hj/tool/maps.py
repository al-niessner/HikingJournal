#! /usr/bin/env python3

if __name__ == '__main__':
    import hj.config
    import hj.usgs.historical

    hj.config.wdir = '/home/niessner/Hiking/Journal'
    quad = hj.usgs.historical.Quad('/home/niessner/Hiking/Quads/Rockies/MT_Silver Run Peak_266706_1996_24000_geo.pdf')
    hj.usgs.historical.scan ('/home/niessner/Hiking/Quads', True)
    pass
