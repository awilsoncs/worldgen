from nose.tools import *
import worldgen
import worldgen.Worldmaps as Worldmaps



def worldmap_shape_test():
    shape = (5, 5)
    wm = Worldmaps.Worldmap(shape)
    if wm.shape != (5,5):
        assert False, "Worldmap shape failed."

def worldmap_arrays_test():
    #A worldmap should generate a array with each element being a dict
    #of values.
    

