from nose.tools import *
import worldgen
import worldgen.worldmaps as worldmaps
import worldgen.algorithm as algorithm
import worldgen.locations as locations

def worldmap_shape_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    if wm.shape != (5,5):
        assert False, "Worldmap shape failed."

def worldmap_arrays_test():
    #A worldmap should generate a array with each element being a dict
    #of values.
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    algorithm.process(wm)
    for x in range(shape[0]):
        for y in range(shape[1]):
            v = wm[x, y]
            if type(v) != locations.Location:
                assert False, "Each value in map.array not a Location"

def east_west_matching_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    algorithm.process(wm)
    for y in range(wm.shape[1]):
        east_v = wm.get((0, y), 'altitude')
        west_v = wm.get((wm.shape[0]-1, y), 'altitude')
        if east_v != west_v:
            print "Found value at (%r, %r): %r" % (0, y, east_v)
            print "And value at (%r, %r): %r" % (wm.shape[0]-1, y, west_v)
            assert False, "East and West values do not match"
            
def north_south_matching_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    algorithm.process(wm)
    v = wm.get((0, 0), 'altitude')
    v2 = wm.get((0, -1), 'altitude')
    for x in range(wm.shape[0]):
        if wm.get((x, 0), 'altitude') != v:
            assert False, "Horizontal lines not matching."
        if wm.get((x, -1), 'altitude') != v2:
            assert False, "Horizontal lines not matching."

def location_init_test():
    coords = (2,4)
    l = locations.Location(coords, test=1, quiz=2)
    if l['test'] == 1 and l['quiz'] == 2:
        return True
    else:
        assert False, "location_init_test failed"
