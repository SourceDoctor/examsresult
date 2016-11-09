from configparser import RawConfigParser
from glob import glob
import csv

language_extension = 'lng'
language_path = '/lng'
app_icon = '.%s/1476313854_report_pencil.png' % language_path
HIDE_ID_COLUMN = False


def lng_load(language='english', type='ini'):
    lng_cfg = {}

    if type == 'ini':
        cfg = RawConfigParser()
        cfg.read('.%s/%s.%s' % (language_path, language, language_extension))
        for section in cfg.sections():
            section_dict = {}
            section_list = cfg.items(section)
            for k, v in section_list:
                section_dict[k] = v
            lng_cfg[section] = section_dict
    else:
        print("unknown Language File Type %s" % type)

    return lng_cfg


def lng_list(type='ini'):
    language_list = []

    lang_file_list = glob('.%s/*.%s' % (language_path, language_extension))

    for lang_file in lang_file_list:
        if type == 'ini':
            cfg = RawConfigParser()
            cfg.read('%s' % lang_file)
            lang_name = cfg.get('main', 'language')
            lang_file_name = lang_file.replace('.%s/' % language_path, '').replace('.%s' % language_extension, '')
            language_list.append((lang_name, lang_file_name))
        else:
            print("unknown Language File Type %s" % type)

    return language_list


def center_pos(window_object, width, height):
    display = window_object.desktop().screenGeometry()
    left = (display.width() - width) / 2
    top = (display.height() - height) / 2
    return left, top


def csv_export(target_file, data, quotechar=" ", delimiter=";"):
    with open(target_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)
