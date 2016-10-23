
default_config = {'language': 'english',
                  'openbox_on_startup': False,
                  'open_file_on_startup': '',
                  }


def init_config():

    config = {'language': 'english',
              'openbox_on_startup': False,
              'open_file_on_startup': 'testdb.exf',
              }

    current_config = default_config
    current_config.update(**config)

    return current_config
