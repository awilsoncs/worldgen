import ConfigParser


def _generate_default_file(path):
    """
    Build the default config file.
    @param path: path to save the config file
    @return: none
    """
    print "Generating config.ini..."
    with open(path, 'w') as config_file:
        config = ConfigParser.SafeConfigParser()
        config.add_section('Parameters')
        config.set('Parameters', 'size_x', '257')
        config.set('Parameters', 'size_y', '129')
        config.set('Parameters', 'depth', '0.6')
        config.add_section('Climate')
        config.set('Climate', 'moisture_pickup', '1.0')
        config.set('Climate', 'moisture_drop', '0.5')
        config.set('Climate', 'winds', '50')
        config.add_section('Controls')
        config.set('Controls', 'scroll', '5')
        config.set('Controls', 'change_ocean', '0.005')
        config.write(config_file)


def get_config(config_file='config.ini'):
    config = ConfigParser.SafeConfigParser()
    if not config.read(config_file):
        _generate_default_file(config_file)
        config.read(config_file)
    return config

verbose = False