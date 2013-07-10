from nose.tools import *
import worldgen
import worldgen.worldmaps as worldmaps
import worldgen.dsprocess as dsprocess
import worldgen.locations as locations
import numpy as np

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
    dsprocess.process(wm)
    for x in range(shape[0]):
        for y in range(shape[1]):
            v = wm[x, y]
            if type(v) != locations.Location:
                assert False, "Each value in map.array not a Location"

def east_west_matching_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    dsprocess.process(wm)
    for y in range(wm.shape[1]):
        east_v = wm[0, y]['elevation']
        west_v = wm[wm.shape[0]-1, y]['elevation']
        if east_v != west_v:
            print "Found value at (%r, %r): %r" % (0, y, east_v)
            print "And value at (%r, %r): %r" % (wm.shape[0]-1, y, west_v)
            assert False, "East and West values do not match"
            
def north_south_matching_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    dsprocess.process(wm)

    north_value = wm[0, 0]['elevation']
    south_value = wm[0, -1]['elevation']
    
    for x in range(wm.shape[0]):
        if wm[x, 0]['elevation'] != north_value:
            assert False, "Horizontal lines not matching."
        if wm[x, -1]['elevation'] != south_value:
            assert False, "Horizontal lines not matching."

def dsprocess_scale_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    dsprocess.process(wm)

    max_dict = {}
    min_dict = {}
    for key in wm.ds_generated:
        for (x, y), value in np.ndenumerate(wm):
            if key not in max_dict or wm[x, y][key] > max_dict[key]:
                max_dict[key] = wm[x, y][key]
            if key not in min_dict or wm[x, y][key] < min_dict[key]:
                min_dict[key] = wm[x, y][key]
    for value in max_dict.itervalues():
        assert value == 1, "Found non-one maximum."
    for value in min_dict.itervalues():
        assert value == 0.0, "Found non-zero maximum."

def location_init_test():
    coords = (2,4)
    l = locations.Location(coords, test=1, quiz=2)
    
    if l['test'] == 1 and l['quiz'] == 2:
        return True
    else:
        assert False, "location_init_test failed"

def variables_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    dsprocess.process(wm)
    for key in ['smoothness', 'elevation', 'volcanism',
                'solubility', 'precious_minerals', 
                'economic_minerals']:
        if key not in wm[0, 0]:
            assert False, "loc missing variable"

def local_max_test():
    shape = (5, 5)
    wm = worldmaps.Worldmap(shape)
    dsprocess.process(wm)
    coords, v = worldmaps.local_max(wm, 'elevation')
    if v != 1.0:
        assert False, "local max test failed"