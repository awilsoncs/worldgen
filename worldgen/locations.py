class Location(dict):

    """Location is a simple extension of the dict class"""
    
    def __init__(self, (x, y), **kwargs):
        dict.__init__(self, kwargs)
        self.x = x
        self.y = y
        #If a location is locked, nothing can modify it.
        self.locked = False