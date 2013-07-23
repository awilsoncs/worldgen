import numpy as np

def build_climate(worldmap):
    set_oceans(worldmap, 0.6)
    draw_north_easterlies(worldmap)
    draw_south_easterlies(worldmap)
    draw_north_tradewinds(worldmap)
    draw_south_tradewinds(worldmap)

def set_oceans(worldmap, depth):
    print "Filling oceans..."
    for (x, y), location in np.ndenumerate(worldmap):
        if location['elevation'] <= depth:
            location['ocean'] = 1.0
        else:
            location['ocean'] = 0.0

def draw_south_easterlies(worldmap):
    pass
def draw_north_easterlies(worldmap):
    pass
def draw_south_tradewinds(worldmap):
    # Get the equator
    start_at = int(worldmap.shape[1] * 2.0/3.0)
    stop_at = worldmap.shape[1]/2 - 2
    print "start at: ", start_at
    print "stop at: ", stop_at
    moisture_array = np.zeros((worldmap.shape[0],1))
    # Step from the 30th n northward to the equator.
    for y in range(start_at, stop_at + 1, -1):
        for (x, y2), cell in np.ndenumerate(moisture_array):
            if worldmap[x, y]['ocean']:
                moisture_array[x, y2] += 1.0
                worldmap[x, y]['precipitation'] = moisture_array[x, y2]
            else:
                elevation = worldmap[x, y]['elevation']
                precipitation = moisture_array[x, y2] * elevation / 4.0
                moisture_array[x, y2] -= precipitation
                worldmap[x, y]['precipitation'] = precipitation
        np.roll(moisture_array, -2)

def draw_north_tradewinds(worldmap):
    # Get the equator
    start_at = int(worldmap.shape[1] * 1.0/3.0)
    stop_at = worldmap.shape[1]/2 + 2
    print "start at: ", start_at
    print "stop at: ", stop_at
    moisture_array = np.zeros((worldmap.shape[0],1))
    # Step from the 30th n southward to the equator.
    for y in range(start_at, stop_at, 1):
        for (x, y2), cell in np.ndenumerate(moisture_array):
            if worldmap[x, y]['ocean']:
                moisture_array[x, y2] += 1.0
                worldmap[x, y]['precipitation'] = moisture_array[x, y2]
            else:
                elevation = worldmap[x, y]['elevation']
                precipitation = moisture_array[x, y2] * elevation / 4.0
                moisture_array[x, y2] -= precipitation
                worldmap[x, y]['precipitation'] = precipitation
        np.roll(moisture_array, -2)