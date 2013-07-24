import numpy as np

def build_climate(worldmap):
    set_oceans(worldmap, 0.6)
    
    # Southern westerlies
    start_at = int(worldmap.shape[1] * 2.0/3.0)
    stop_at = worldmap.shape[1]
    draw_wind (worldmap, start_at, stop_at, 2)

    # Northern westerlies
    start_at = int(worldmap.shape[1] * 1.0/3.0)
    stop_at = -1
    draw_wind (worldmap, start_at, stop_at, 2)

    # Southern trades
    start_at = int(worldmap.shape[1] * 2.0/3.0)
    stop_at = worldmap.shape[1]/2 - 1
    draw_wind (worldmap, start_at, stop_at, -2)

    # Northern trades
    start_at = int(worldmap.shape[1] * 1.0/3.0)
    stop_at = worldmap.shape[1]/2 + 2
    draw_wind (worldmap, start_at, stop_at, -2)

def set_oceans(worldmap, depth):
    print "Filling oceans..."
    for (x, y), location in np.ndenumerate(worldmap):
        if location['elevation'] <= depth:
            location['ocean'] = 1.0
        else:
            location['ocean'] = 0.0

def draw_wind(worldmap, start_at, stop_at, direction):
    step = 1
    if start_at > stop_at:
        step = -1
    moisture_array = np.zeros((worldmap.shape[0],1))
    # Step from the 30th n northward to the equator.
    for y in range(start_at, stop_at, step):
        for (x, y2), cell in np.ndenumerate(moisture_array):
            if worldmap[x, y]['ocean']:
                moisture_array[x, y2] += 1.0
                worldmap[x, y]['precipitation'] = 0.0
            else:
                elevation = worldmap[x, y]['elevation']
                precipitation = moisture_array[x, y2] * (elevation - 0.5)
                moisture_array[x, y2] -= precipitation
                worldmap[x, y]['precipitation'] = precipitation
        moisture_array = np.roll(moisture_array, direction)