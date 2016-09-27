#from .dbhandler import DBHandler
from configparser import RawConfigParser


def lng_load(language='english', type='ini'):
    lng_cfg = {}

    if type == 'ini':
        cfg = RawConfigParser()
        cfg.read('./lng/%s.lng' % language)
        for section in cfg.sections():
            section_dict = {}
            section_list = cfg.items(section)
            for k,v in section_list:
                section_dict[k] = v
            lng_cfg[section] = section_dict

    return lng_cfg

def center_pos(window_object, width, height):
    window_object.update_idletasks()
    w = window_object.winfo_screenwidth()
    h = window_object.winfo_screenheight()
    size = tuple(int(_) for _ in window_object.geometry().split('+')[0].split('x'))
    x = w / 2 - width / 2
    y = h / 2 - height / 2
    window_object.geometry("%dx%d+%d+%d" % (size + (x, y)))

class Control(object):

    def __init__(self, db_name):
#        self.db = DBHandler(database=db_name)
        pass
