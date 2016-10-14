from configparser import RawConfigParser

app_icon = './lng/1476313854_report_pencil.png'


def lng_load(language='english', type='ini'):
    lng_cfg = {}

    if type == 'ini':
        cfg = RawConfigParser()
        cfg.read('./lng/%s.lng' % language)
        for section in cfg.sections():
            section_dict = {}
            section_list = cfg.items(section)
            for k, v in section_list:
                section_dict[k] = v
            lng_cfg[section] = section_dict

    return lng_cfg


def center_pos(window_object, width, height):
    display = window_object.desktop().screenGeometry()
    left = (display.width() - width) / 2
    top = (display.height() - height) / 2
    return left, top
