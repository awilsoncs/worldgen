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

def draw_north_easterlies(worldmap):
    pass
def draw_south_easterlies(worldmap):
    pass
def draw_north_tradewinds(worldmap):
    # Get the equator
    stop_at = worldmap.shape[1] / 2
    start_at = int(worldmap.shape[1] * 2.0/3.0)
    moisture_array = np.zeros((1, worldmap.shape[1]))
    # Step from the 30th n southward to the equator.
    for y in range(start_at, stop_at + 1, -1):
        for (x, y2), cell in np.ndenumerate(moisture_array):
            if worldmap[x, y]['ocean']:
                moisture_array[x, y2] += 1.0
                worldmap[x, y]['precipitation'] = moisture_array[x, y2]
            else:
                elevation = worldmap[x, y]['elevation'] - 0.1
                precipitation = moisture_array[x, y2] * elevation
                worldmap[x, y]['precipitation'] = precipitation
        np.roll(moisture_array, 1)

def draw_south_tradewinds(worldmap):
    pass