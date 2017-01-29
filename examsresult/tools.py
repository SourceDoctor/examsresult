from configparser import RawConfigParser
from glob import glob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

language_extension = 'lng'
language_path = '/lng'
app_icon = '.%s/1476313854_report_pencil.png' % language_path

HIDE_ID_COLUMN = True


def lng_load(language='english', type='ini'):
    lng_cfg = {}

    if type == 'ini':
        cfg = RawConfigParser()
        configfile = '.%s/%s.%s' % (language_path, language, language_extension)

        cfg.read(configfile)
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
            lang_file_name = lang_file.replace('.%s\\' % language_path, '')
            lang_file_name = lang_file_name.replace('.%s/' % language_path, '')
            lang_file_name = lang_file_name.replace('.%s' % language_extension, '')

            language_list.append((lang_name, lang_file_name))
        else:
            print("unknown Language File Type %s" % type)

    return language_list


def cleanup_filename(filename):
    # remove's forbidden character from Filename
    forbidden_chars = '<>"|?*\\:/'

    for char in forbidden_chars:
        if char in filename:
            filename = filename.replace(char, '')
    return filename


def center_pos(window_object, width, height):
    display = window_object.desktop().screenGeometry()
    left = (display.width() - width) / 2
    top = (display.height() - height) / 2
    return left, top


def export_csv(target_file, data, quotechar=" ", delimiter=";"):
    if not target_file.endswith(".csv"):
        target_file += ".csv"
    with open(target_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)


def sort(unsorted_list, reverse=False):
    return sorted(unsorted_list, key=str.lower, reverse=reverse)


class ExportPdf(object):

    min_x = 2
    max_x = 610
    min_y = 2
    max_y = 780
    body_min_x = min_x + 50
    body_max_x = max_x - 50
    body_min_y = min_y + 50 + 10
    body_max_y = max_y - 50 - 10
    line_distance_x = 10
    line_distance_y = 30

    font_normal = 'Helvetica'
    font_size = 12

    head_text = "Head"
    foot_text = "Foot"

    def __init__(self, target_file, template, head_text="Head", foot_text="Foot", data=None):
        if not target_file.endswith(".pdf"):
            target_file += ".pdf"

        self.pdf_export = canvas.Canvas(target_file, pagesize=letter)
        self.pdf_export.setLineWidth(.3)
        self.pdf_export.setFont(self.font_normal, self.font_size)
        self.pdf_export.font_size = self.font_size
        self.pdf_export.body_min_x = self.body_min_x
        self.pdf_export.body_max_x = self.body_max_x
        self.pdf_export.body_min_y = self.body_min_y
        self.pdf_export.body_max_y = self.body_max_y
        self.template = template
        self.head_text = head_text
        self.foot_text = foot_text
        self.data = data

    def template(self, data):
        self.pdf_export.drawString(100, 750, "no content")

    def save(self):
        self.template_head()
        self.template(self.pdf_export, self.data)
        self.template_foot()
        self.pdf_export.save()

    def template_head(self):
        self.pdf_export.setFont(self.font_normal, self.font_size + 2)
        self.pdf_export.line(self.min_x + self.line_distance_x,
                             self.max_y - self.line_distance_y,
                             self.max_x - self.line_distance_x,
                             self.max_y - self.line_distance_y
                             )
        self.pdf_export.drawString(self.min_x + 10, self.max_y - 20, self.head_text)
        self.pdf_export.setFont(self.font_normal, self.font_size)

    def template_foot(self):
        project_name_offset = self.font_size
        project_name = "created by Examsresult"
        self.pdf_export.line(self.min_x + self.line_distance_x,
                             self.min_y + self.line_distance_y + project_name_offset,
                             self.max_x - self.line_distance_x,
                             self.min_y + self.line_distance_y + project_name_offset
                             )
        self.pdf_export.drawString(50,
                                   self.min_y + self.line_distance_y,
                                   self.foot_text
                                   )
        self.pdf_export.setFont(self.font_normal, self.font_size - 2)
        self.pdf_export.drawString(self.max_x - 8 * len(project_name),
                                   self.min_y + 10,
                                   project_name
                                   )
        self.pdf_export.setFont(self.font_normal, self.font_size)
