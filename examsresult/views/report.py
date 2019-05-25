from os.path import isfile

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QAbstractItemView, QMenu, \
    QToolButton, QPushButton, QMessageBox, QFrame

from examsresult import current_config
from examsresult.controls.calculation import Calculation
from examsresult.extendedqinputdialog import ExtendedQInputDialog
from examsresult.models import DB_ID_INDEX
from examsresult.tools import HIDE_ID_COLUMN
from examsresult.views import CoreView


class ViewReport(CoreView):

    table_left = 30
    table_top = 130
    table_height = 350
    table_width = 600

    y_pos = 10

    show_schoolyear = True
    show_schoolclass = True
    show_subject = True
    show_student = False

    sorting = False

    def __init__(self, dbhandler, root_tab, lng, data):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())
        self.config = current_config
        self.data = data
        self.calculation = Calculation(dbh=self.dbh, config=self.config, lng=self.lng, data=self.data)

        mytab = QWidget()

        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        self.image_window = QLabel(mytab)
        self.image_window.setFrameShape(QFrame.Panel)
        self.image_window.setFrameShadow(QFrame.Sunken)
        self.image_window.setLineWidth(3)
        image_window_top = self.table_top - 10 - self.student_image_height
        image_window_left = self.table_left + self.table_width + 10
        self.image_window.setGeometry(image_window_left,
                                      image_window_top,
                                      self.student_image_width,
                                      self.student_image_height)

        if self.show_schoolyear:
            self.schoolyear = data['schoolyear']
            label_schoolyear_description = QLabel(self.lng['schoolyear'], mytab)
            label_schoolyear_description.move(10, self.y_pos)
            label_schoolyear_description = QLabel(self.schoolyear, mytab)
            label_schoolyear_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_schoolclass:
            self.schoolclass = data['schoolclass']
            label_schoolclass_description = QLabel(self.lng['schoolclass'], mytab)
            label_schoolclass_description.move(10, self.y_pos)
            label_schoolclass_description = QLabel(self.schoolclass, mytab)
            label_schoolclass_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_subject:
            self.subject = data['subject']
            label_subject_description = QLabel(self.lng['subject'], mytab)
            label_subject_description.move(10, self.y_pos)
            label_subject_description = QLabel(self.subject, mytab)
            label_subject_description.move(100, self.y_pos)
            self.y_pos += 20

        if self.show_student:
            self.student_id = data['student_id']
            s = self.dbh.get_student_data(self.student_id)
            self.student = "%s, %s" % (s.lastname, s.firstname)
            self.student_image = s.image

            label_student_description = QLabel(self.lng['student'], mytab)
            label_student_description.move(10, self.y_pos)
            label_student_description = QLabel(self.student, mytab)
            label_student_description.move(100, self.y_pos)
            self.y_pos += 20

        self.y_pos += 20
        label_results = QLabel(self.lng['results'], mytab)
        label_results.move(self.table_left, self.y_pos)

        self.y_pos += 20
        self.table_top = self.y_pos
        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)
        self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
            if 'hide' in col.keys():
                self.my_table.setColumnHidden(self.column_title.index(col), col['hide'])
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        self.button_export = QToolButton(mytab)
        self.button_export.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_export.setText(self.lng['export'])
        self.button_export.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.lng['csv_export'], lambda: self.do_csv_export())
        menu.addAction(self.lng['pdf_export'], lambda: self.do_pdf_export(self.export_file_title))
        self.button_export.setMenu(menu)

        if self.show_student:
            self.button_simulate = QPushButton(self.lng['simulate'], mytab)
            self.button_simulate.move(self.table_left + self.table_width + 10, self.table_top + self.button_export.height())
            self.button_simulate.clicked.connect(self.simulate_action)
            
            self.button_simulation_clear = QPushButton(self.lng['simulation_clear'], mytab)
            self.button_simulation_clear.move(self.table_left + self.table_width + 10,
                                              self.table_top + self.button_export.height() + self.button_simulate.height()
                                              )
            self.button_simulation_clear.clicked.connect(self.simulate_clear)
            self.button_simulation_clear.setEnabled(False)

        # hide Column 'id'
        self.my_table.setColumnHidden(DB_ID_INDEX, HIDE_ID_COLUMN)

        if self.row_title:
            self.my_table.setVerticalHeaderLabels(self.row_title)

        if self.full_row_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        if self.full_column_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectColumns)

        if self.cell_editable:
            self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.load_data(1, 0)

        self.my_table.resizeColumnsToContents()
        self.my_table.setSortingEnabled(self.sorting)

    def load_image(self, filename):
        # TODO: does not work if placed in parent class
        pixmap = QPixmap(filename)
        if filename and isfile(filename):
            pixmap = pixmap.scaled(self.student_image_height,
                                   self.student_image_width,
                                   QtCore.Qt.KeepAspectRatio)
        self.image_window.setPixmap(pixmap)

    def show_results(self):
        return []

    def do_csv_export(self):
        self.configure_export_csv(parent=self.tab_window, default_filename=self.export_file_title)

    @property
    def export_file_title(self):
        return ""

    @property
    def pdf_head_text(self):
        return "Head"

    @property
    def pdf_foot_text(self):
        return "Foot"

    def simulate_action(self):
        pass

    def simulate_clear(self):
        pass

    def reload_data(self):
        self.clear_table()
        self.load_data()


class ViewReportSchoolclass(ViewReport):

    sorting = True

    def __init__(self, dbhandler, root_tab, lng, data):
        super().__init__(dbhandler, root_tab, lng, data)
        self.my_table.clicked.connect(self.action_select)

    def _define_column_title(self):
        timeperiod_list = self.dbh.get_timeperiod()
        column_title = []

        column_title.append({'name': self.lng['student'], 'type': 'string', 'unique': False})
        for period in timeperiod_list:
            column_title.append({'name': period[1], 'type': 'string', 'unique': False})
        column_title.append({'name': self.lng['schoolyear'], 'type': 'string', 'unique': False})
        column_title.append({'name': 'image_filename', 'type': 'image', 'unique': False, 'hide': True})

        return column_title

    def action_select(self, cell=None, limit_column=[]):
        student_image_column = len(self.column_title)
        if student_image_column:
            student_image_column -= 1
        image_data_temp = self.my_table.item(cell.row(), student_image_column).text()
        self.load_image(image_data_temp)

    @property
    def export_file_title(self):
        return "%s_%s_%s" % (self.schoolyear, self.schoolclass, self.subject)

    def _action_load_content(self):
        return self.show_results()

    def show_results(self):
        return self.calculation.show_results_schoolclass(schoolyear=self.schoolyear,
                                                         schoolclass=self.schoolclass,
                                                         subject=self.subject)

    def pdf_template(self, obj, data):
        y = obj.body_max_y
        x = obj.body_min_x

        font_width = round(obj.font_size * 3/5, 0)

        title_list = []
        string_len = []
        # get maximal length
        first_element = True
        for t in self.column_title:
            if first_element:
                first_element = False
                continue
            title_list.append(t['name'])
            string_len.append(len(t['name']))

        for row in data:
            i = 1
            while i < len(string_len):
                if len(str(row[i])) > string_len[i - 1]:
                    string_len[i - 1] = len(str(row[i]))
                i += 1

        string_width = []
        i = 0
        while i < len(string_len):
            string_width.append(font_width * string_len[i])
            i += 1

        # print title
        offset = 0
        i = 0
        for title in title_list:
            obj.drawString(x + offset, y, str(title))
            offset += string_width[i]
            i += 1

        # print seperator Line
        y -= 4
        obj.line(x, y, x + offset, y)
        # print period results
        for row in data:
            offset = 0
            y -= obj.font_size
            i = -1
            first_element = True
            while i < len(row) - 1:
                i += 1
                if first_element:
                    first_element = False
                    continue
                obj.drawString(x + offset, y, str(row[i]))
                offset += string_width[i - 1]

    @property
    def pdf_head_text(self):
        return "%s: %s %s %s" % (self.lng['title'], self.schoolyear, self.schoolclass, self.subject)

    @property
    def pdf_foot_text(self):
        return ""


class ViewReportStudent(ViewReport):

    show_student = True
    simulation_data = []

    student_image = None

    def __init__(self, dbhandler, root_tab, lng, data):
        super().__init__(dbhandler, root_tab, lng, data)
        self.load_image(self.student_image)

    def _define_column_title(self):
        return [{'name': self.lng['date'], 'type': 'string', 'unique': False},
                {'name': self.lng['timeperiod'], 'type': 'string', 'unique': False},
                {'name': self.lng['examtype'], 'type': 'string', 'unique': False},
                {'name': self.lng['result'], 'type': 'string', 'unique': False},
                {'name': self.lng['periodresult'], 'type': 'string', 'unique': False},
                {'name': self.lng['comment'], 'type': 'string', 'unique': False},
                ]

    def _action_load_content(self):
        return self.show_results(simulate_data=self.simulation_data)

    @property
    def export_file_title(self):
        return "%s_%s_%s_%s" % (self.schoolyear, self.schoolclass, self.subject, self.student)

    def show_results(self, simulate_data=[]):
        return self.calculation.show_results_student(student_id=self.student_id,
                                                     subject=self.subject,
                                                     simulate_data=simulate_data)

    def pdf_template(self, obj, data):
        y = obj.body_max_y
        x = obj.body_min_x

        font_width = round(obj.font_size * 3/5, 0)

        date_max_len = len(self.lng['date'])
        timeperiod_max_len = len(self.lng['timeperiod'])
        examtype_max_len = len(self.lng['examtype'])
        result_max_len = len(self.lng['result'])
        periodresult_max_len = len(self.lng['periodresult'])

        for row in data:
            if len(row[1]) > date_max_len:
                date_max_len = len(row[1])
            if len(row[2]) > timeperiod_max_len:
                timeperiod_max_len = len(row[2])
            if len(row[3]) > examtype_max_len:
                examtype_max_len = len(row[3])
            if len(str(row[4])) > result_max_len:
                result_max_len = len(str(row[4]))
            if len(str(row[5])) > periodresult_max_len:
                periodresult_max_len = len(str(row[5]))

        date_max_width = font_width * date_max_len
        timeperiod_max_width = font_width * timeperiod_max_len
        examtype_max_width = font_width * examtype_max_len
        result_max_width = font_width * result_max_len
        periodresult_max_width = font_width * periodresult_max_len

        y -= obj.font_size
        offset = 0
        obj.drawString(x, y, self.lng['date'])
        offset += date_max_width
        obj.drawString(x + offset, y, self.lng['timeperiod'])
        offset += timeperiod_max_width
        obj.drawString(x + offset, y, self.lng['examtype'])
        offset += examtype_max_width
        obj.drawString(x + offset, y, self.lng['result'])
        offset += result_max_width
        obj.drawString(x + offset, y, self.lng['periodresult'])
        offset += periodresult_max_width
        obj.drawString(x + offset, y, self.lng['comment'])

        y -= 4
        obj.line(x, y, x + offset + 100, y)

        for row in data:
            if not row[1]:
                # Period end
                y -= 4
                obj.line(x, y, x + offset + 100, y)

            y -= obj.font_size
            offset = 0
            obj.drawString(x, y, row[1])
            offset += date_max_width
            obj.drawString(x + offset, y, row[2])
            offset += timeperiod_max_width
            obj.drawString(x + offset, y, str(row[3]))
            offset += examtype_max_width
            obj.drawString(x + offset, y, str(row[4]))
            offset += result_max_width
            obj.drawString(x + offset, y, str(row[5]))
            offset += periodresult_max_width
            obj.drawString(x + offset, y, row[6])
            if not row[1]:
                y -= obj.font_size

    @property
    def pdf_head_text(self):
        return "%s: %s %s %s %s" % (self.lng['title'], self.schoolyear, self.schoolclass, self.subject, self.student)

    @property
    def pdf_foot_text(self):
        return ""

    def simulate_clear(self):
        self.simulation_data = []
        self.button_simulation_clear.setEnabled(False)
        self.reload_data()

    def simulate_action(self):
        self.simulation_data = self.simulate_student_result()
        if self.simulation_data:
            self.button_simulation_clear.setEnabled(True)
        else:
            self.button_simulation_clear.setEnabled(False)

        self.load_data()

    def simulate_student_result(self):
        simulation_data = []

        timeperiod_list = [t[1] for t in self.dbh.get_timeperiod()]
        examtype_list = [x[1] for x in self.dbh.get_examtype()]

        simulate_dialog = ExtendedQInputDialog(parent=self.tab_window)
        add_results = True
        while add_results:
            timeperiod, ok = simulate_dialog.getItem(self.tab_window, self.lng['simulate'], self.lng['timeperiod'], timeperiod_list, 0, False)
            if not ok:
                break
            examtype, ok = simulate_dialog.getItem(self.tab_window, self.lng['simulate'], self.lng['examtype'], examtype_list, 0, False)
            if not ok:
                break
            result, ok = simulate_dialog.getDouble(self.tab_window, self.lng['simulate'], self.lng['result'], value=0)
            if not ok:
                break

            exam_id = self.dbh.get_examtype_id(examtype)
            timeperiod_id = self.dbh.get_timeperiod_id(timeperiod)

            simulation_data.append((self.lng['simulate'], timeperiod_id, exam_id, result))

            answer = QMessageBox.question(self.tab_window, self.lng['simulate'], self.lng['msg_another_simulation_result'])
            if answer == QMessageBox.No:
                add_results = False

        return simulation_data
