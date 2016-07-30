import configparser


def generate_default_file(path):
    """
    Build the default config file.
    @param path: path to save the config file
    @return: none
    """
    print("Generating config.ini...")
    with open(path, 'w') as config_file:
        config_parser = configparser.ConfigParser()
        config_parser.add_section('Parameters')
        config_parser.set('Parameters', 'size_x', '500')
        config_parser.set('Parameters', 'size_y', '500')
        config_parser.set('Parameters', 'scale', '9')
        config_parser.set('Parameters', 'depth', '0.5517')
        config_parser.set('Parameters', 'variance', '1.5')
        config_parser.add_section('Climate')
        config_parser.set('Climate', 'moisture_pickup', '1.0')
        config_parser.set('Climate', 'moisture_drop', '0.5')
        config_parser.set('Climate', 'average_temperature', '80')
        config_parser.set('Climate', 'winds', '50')
        config_parser.write(config_file)


def get_config(config_file='config.ini'):
    """

    @rtype : ConfigParser
    """
    config_parser = configparser.ConfigParser()
    if not config_parser.read(config_file):
        generate_default_file(config_file)
        config_parser.read(config_file)
    return config_parser

config = get_config()
