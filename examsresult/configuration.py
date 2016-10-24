import json
from os.path import isfile


def default_config():
    default_dict = {
        'language': 'english',
        'openbox_on_startup': False,
        'open_file_on_startup': '',
        }
    return default_dict

current_config = {}

configfile = "examsresult.conf"


def init_config():
    my_config = load_config()
    config = default_config()

    config.update(**my_config)
    current_config.update(**config)

    return config

def save_config(config, configfile=configfile):
    with open(configfile, 'w') as f:
        f.write(json.dumps(config))

def load_config(configfile=configfile):
    if not isfile(configfile):
        return {}

    with open(configfile, 'r') as f:
        config = f.read()

    return json.loads(config)
