import json
from os import makedirs
from os.path import isfile, splitext

configfile = "examsresult.conf"

current_config = {}


def image_directory(absolute_filename):
    directory = splitext(absolute_filename)[0]
    makedirs(directory, exist_ok=True)
    return directory


def default_config():
    default_dict = {
        'language': 'english',
        'openbox_on_startup': False,
        'open_file_on_startup': '',
        'schoolyear_result_calculation_method': 'complete',
        'title_view': 'filename'
        }
    return default_dict


def init_config():
    my_config = load_config()
    config = default_config()

    config.update(**my_config)
    current_config.update(**config)

    return config


def save_config(config, conffile=configfile):
    with open(conffile, 'w') as f:
        f.write(json.dumps(config))


def load_config(conffile=configfile):
    if not isfile(conffile):
        return {}

    with open(conffile, 'r') as f:
        config = f.read()

    return json.loads(config)
