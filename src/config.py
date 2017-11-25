import configparser
import sys

def read_config(configfile="config.ini"):
    """reads the given config file and returns a ConfigParser object.
    This does some simple checks and adds default values"""
    config = configparser.ConfigParser(allow_no_value=True)
    defaults = {'network'   : {'ip' : None},
            'rate'      : {'sleeptime' : 0.0001}}
    config.read_dict(defaults)
    config.read('example.ini')

    ips_found = (len(config.options("ips")) + len(config.options("networks"))) > 0
    if not ips_found:
        print("Config Error: Either [ips] or [networks] need keys")
        sys.exit(1)

    for section in ['ips','networks']:
        try:
            config.add_section('ips')
        except configparser.DuplicateSectionError:
            pass

    return config

