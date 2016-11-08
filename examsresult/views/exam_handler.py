from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QTableWidget, \
    QAbstractItemView, QTextEdit, QCalendarWidget, QInputDialog, QTableWidgetItem, \
    QMessageBox

from examsresult.configuration import current_config
from examsresult.tools import lng_list, HIDE_ID_COLUMN
from examsresult.views.core import CoreView


class Exam(CoreView):

    changed_mark_enabled = False
    exam_id = None
    students = None

    width = 500
    height = 500
    table_left = 50
    table_top = 110
    table_height = 320
    table_width = 400

    def __init__(self, dbhandler, parent, lng, exam_data, type='add', single_test=False):
        self.type = type
        if 'exam_id' in exam_data:
            self.exam_id = exam_data['exam_id']
        else:
            self.schoolyear = exam_data['schoolyear']
            self.schoolclass = exam_data['schoolclass']
            self.subject = exam_data['subject']
            self.examtype = exam_data['examtype']
            self.timeperiod = exam_data['timeperiod']
            self.students = exam_data['students']

        self.dbhandler = dbhandler
        self.lng = lng
        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        self.language_list = lng_list()
        config = current_config

        self.window = QDialog(parent=parent)
        self.window.setFixedHeight(self.height)
        self.window.setFixedWidth(self.width)
        self.window.setWindowTitle(self.lng['title_result'])
        self.window.closeEvent = self.closeEvent

        label_exam_description = QLabel(self.window)
        label_exam_description.setText(self.lng['exam_description'])
        label_exam_description.move(self.table_left, 50)
        self.text_exam_description = QTextEdit(self.window)
        self.text_exam_description.setGeometry(self.table_left + 100, 52, 300, 40)
        self.text_exam_description.textChanged.connect(self.description_changed)

        label_students = QLabel(self.window)
        label_students.setText(self.lng['students'])
        label_students.move(self.table_left, self.table_top - 20)

        self.my_table = QTableWidget(self.window)

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)

        if HIDE_ID_COLUMN:
            # hide Column 'id'
            self.my_table.setColumnHidden(0, True)

        if self.row_title:
            self.my_table.setVerticalHeaderLabels(self.row_title)

        if self.full_row_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        if self.full_column_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectColumns)

        if self.cell_editable:
            self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Fixme: on doubleclick-Edit Cell has blinking Cursor focus

        self.my_table.resizeColumnsToContents()
        self.my_table.setSortingEnabled(self.sorting)

        self.my_table.doubleClicked.connect(self.result_edit)

        # set button_save object, so set_change - Handler doesn't crash
        self.button_save = QPushButton(self.lng['save'], self.window)
        self.button_save.move(self.table_left + self.table_width - self.button_save.width(), self.table_top + self.table_height)
        self.button_save.clicked.connect(self.action_save)

        self.button_csv_export = QPushButton(self.lng['csv_export'], self.window)
        self.button_csv_export.move(self.table_left + self.table_width - self.button_save.width() - self.button_csv_export.width(), self.table_top + self.table_height)
        self.button_csv_export.clicked.connect(self.do_csv_export)

        button_cancel = QPushButton(self.lng['close'], self.window)
        button_cancel.move(370, 470)
        button_cancel.clicked.connect(self.window.close)

        self.cal = QCalendarWidget(self.window)
        self.cal.setGridVisible(True)
        self.cal.move(self.table_left + 100, 30)
        self.cal.clicked.connect(self.set_date)
        self.cal.setVisible(False)

        label_exam_date = QLabel(self.window)
        label_exam_date.setText(self.lng['exam_date'])
        label_exam_date.move(self.table_left, 30)

        date = self.cal.selectedDate()
        self.exam_date = QLabel(self.window)
        self.exam_date.setText(date.toString())
        self.exam_date.setGeometry(self.table_left + 100, 22, 120, self.exam_date.height())

        self.button_set_date = QPushButton(self.lng['set_date'], self.window)
        self.button_set_date.move(self.table_left + 240, 25)
        self.button_set_date.clicked.connect(self.set_date)

        if self.students:
            for student in self.students:
                self.action_add(data_import=True, with_id=True, data=student)

        self.window.show()

        if type == 'add':
            # run over all students to fill in results
            self.insert_result(add_defaults=single_test)
        else:
            self.load_data()

        self.set_changed(False)

        self.window.exec_()

    def _define_column_title(self):
        return [{'name': self.lng['lastname'], 'type': 'string', 'unique': False},
                {'name': self.lng['firstname'], 'type': 'string', 'unique': False},
                {'name': self.lng['result'], 'type': 'float', 'unique': False},
                {'name': self.lng['comment'], 'type': 'string', 'unique': False}
                ]

    def _action_load_content(self):
        if self.exam_id != None:
            data = self.dbhandler.get_exam_by_id(exam_id=self.exam_id)
            school_class = self.dbhandler.get_schoolclass_data(data.school_class_id)
            timeperiod = self.dbhandler.get_timeperiod_by_id(data.time_period)
            examtype = self.dbhandler.get_examtype_by_id(data.exam_type)
            self.exam_date.setText(data.date)
            self.schoolyear = school_class.schoolyear
            self.schoolclass = school_class.schoolclass
            self.subject = data.subject
            self.examtype = examtype.name
            self.timeperiod = timeperiod.name
            self.text_exam_description.setText(data.comment)
        else:
            school_class_id = self.dbhandler.get_schoolclass_id(self.schoolyear, self.schoolclass)
            data = self.dbhandler.get_exam(exam_date=self.exam_date.text(),
                                           school_class_id=school_class_id,
                                           subject=self.subject,
                                           examtype=self.examtype,
                                           timeperiod=self.timeperiod)
        student_results = self.dbhandler.get_exam_result(exam_id=data.id)

        student_result_list = []
        for s in student_results:
            student = self.dbhandler.get_student_data(s.student)
            student_result_list.append((student.id, student.lastname, student.firstname, s.result, s.comment))
        return student_result_list

    def exam_is_unique(self, msg=True):
        exam_date = self.exam_date.text()
        schoolyear = self.schoolyear
        schoolclass = self.schoolclass
        subject = self.subject
        examtype = self.examtype
        timeperiod = self.timeperiod
        ret = self.dbhandler.exam_is_unique(exam_date, schoolyear, schoolclass, subject, examtype, timeperiod)
        if ret:
            return True
        if msg:
            QMessageBox.warning(self.window, self.lng['title'], self.lng['msg_exam_not_unique'])
        return False

    def result_edit(self, cell):
        self.action_edit(cell, limit_column=[3, 4])

    def set_date(self):
        self.cal.setVisible(not self.cal.isVisible())
        self.button_set_date.setVisible(not self.button_set_date.isVisible())
        self.exam_date.setVisible(not self.exam_date.isVisible())
        date = self.cal.selectedDate()
        self.exam_date.setText(date.toString())

        if not self.exam_is_unique(msg=not self.exam_id):
            return

        self.set_changed(True)

    def description_changed(self):
        self.set_changed(True)

    def insert_result(self, add_defaults=False):
        lastname_column = 1
        firstname_column = 2
        result_column = 3
        dialog = QInputDialog(self.my_table)
        row = 0
        while row <= self.my_table.rowCount() - 1:
            lastname = self.my_table.item(row, lastname_column).text()
            firstname = self.my_table.item(row, firstname_column).text()
            input_text = "%s, %s" % (lastname, firstname)

            if add_defaults:
                result = 0.0
                ok = True
            else:
                result, ok = dialog.getDouble(self.my_table, self.lng['result'], input_text, decimals=self.float_precision)

            if not ok:
                return
            self.my_table.setItem(row, result_column, QTableWidgetItem(str(result)))
            self.set_changed(True)

            row += 1

    def _action_save_content(self, data):

        if not self.exam_id and not self.exam_is_unique():
            return False

        self.dbhandler.set_exam(id=self.exam_id,
                                exam_date=self.exam_date.text(),
                                schoolyear=self.schoolyear,
                                schoolclassname=self.schoolclass,
                                subject=self.subject,
                                examtype=self.examtype,
                                timeperiod=self.timeperiod,
                                results=data,
                                comment=self.text_exam_description.toPlainText())
        return True

    def closeEvent(self, event):
        if self.button_save.isEnabled():
            answer = QMessageBox.question(self.window, self.lng['title'], self.lng['msg_close_unsaved'])
            if answer == QMessageBox.No:
                event.ignore()
                return
        self.window.close()

    def do_csv_export(self):
        filename = "%s_%s_%s_%s_%s" % (self.exam_date.text(), self.schoolyear, self.schoolclass, self.subject, self.examtype)
        self.configure_csv_export(parent=self.window, default_filename=filename)
