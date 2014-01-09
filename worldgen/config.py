class Config(dict):
    def __init__(self, config_file, **kwargs):
        """
        @param config_file: filename of the config file
        @param kwargs: additional config parameters
        """
        super(Config, self).__init__(**kwargs)
        try:
            self.get_configs(config_file)
        except IOError:
            print "Generating config file..."
            with open(config_file, 'w') as f:
                output = ""
                for line in DEFAULTS:
                    output += line
                f.write(output)
            self.get_configs(config_file)

    def get_configs(self, config_file):
        with open(config_file, 'r') as f:
            for line in f:
                line = line.split('=')
                if len(line) > 1:
                    key = line[0]
                    value = line[1]
                    self[key] = value

verbose = False

DEFAULTS = ['======Parameters=====\n',
            'size_x=513\n',
            'size_y=257\n',
            'depth=0.6\n',
            '\n',
            '=======Climate=======\n',
            'moisture_pickup=1.0\n',
            'moisture_drop=0.5\n',
            'winds=50\n',
            '\n',
            '=======Controls======\n',
            'scroll=5\n',
            'change_ocean=0.005\n',
            ]