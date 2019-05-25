from os.path import isfile

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, \
    QPushButton, QComboBox, QMessageBox, QToolButton, QMenu, QCheckBox, QFrame
from examsresult.extendedqinputdialog import ExtendedQInputDialog
from examsresult.models import DB_ID_INDEX, DB_SCHOOLCLASS_SCHOOLCLASS_INDEX
from examsresult.tools import HIDE_ID_COLUMN, sort
from examsresult.views import CoreView
from examsresult.views.exam_handler import Exam
from examsresult.views.import_csv import CSVImport


class ViewConfigure(CoreView):

    table_left = 100
    table_top = 130
    table_height = 350
    table_width = 500

    schoolyear_listindex = 0
    schoolclass_listindex = 0

    change_enabled = True

    def _change(self, change_listbox, change_index, index):
        if not self.change_enabled:
            self.change_enabled = True
            return change_index
        if self.is_changed:
            answer = QMessageBox.question(self.tab_window, self.lng['title'], self.lng['msg_switch_unsaved'])
            if answer == QMessageBox.No:
                self.change_enabled = False
                change_listbox.setCurrentIndex(change_index)
                return change_index
            self.set_changed(False)
        self.load_data()
        return index

    def get_schoolclassnames(self):
        return [x[1] for x in self.dbh.get_schoolclassname()]

    def get_schoolyears(self):
        return [x[1] for x in self.dbh.get_schoolyear()]

    def get_subjectnames(self):
        return [x[1] for x in self.dbh.get_subject()]


class ViewSchoolClassConfigure(ViewConfigure):

    schoolclass_combined = False
    schoolclass_name = ""

    def __init__(self, dbhandler, root_tab, lng):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng

        self.define_column_title()

        mytab = QWidget()

        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        label_students = QLabel(self.lng['students'], mytab)
        label_students.move(self.table_left, self.table_top - 20)

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

        self.button_add = QPushButton(self.lng['add'], mytab)
        self.button_add.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_add.clicked.connect(self.action_add)

        self.button_edit = QPushButton(lng['edit'], mytab)
        self.button_edit.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height())
        self.button_edit.clicked.connect(self.action_edit)

        self.button_remove = QPushButton(self.lng['remove'], mytab)
        self.button_remove.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height() + self.button_edit.height())
        self.button_remove.clicked.connect(self.student_remove)

        self.button_export = QToolButton(mytab)
        self.button_export.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height() + self.button_edit.height() + self.button_remove.height())
        self.button_export.setText(self.lng['export'])
        self.button_export.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.lng['csv_export'], lambda: self.do_csv_export())
        menu.addAction(self.lng['pdf_export'], lambda: self.do_pdf_export(self.export_file_title))
        self.button_export.setMenu(menu)

        self.button_import = QToolButton(mytab)
        self.button_import.move(self.table_left + self.table_width + self.button_add.width(), self.table_top)
        self.button_import.setText(self.lng['import'])
        self.button_import.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.lng['import_csv'], self.student_import_csv)
        menu.addAction(self.lng['import_other_schoolclass'], self.student_import_other_class)
        self.button_import.setMenu(menu)

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

        self.my_table.setSortingEnabled(self.sorting)

        self.my_table.clicked.connect(self.action_select)
        self.my_table.doubleClicked.connect(self.action_edit)

        self.button_save = QPushButton(lng['save'], mytab)
        self.button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        self.button_save.clicked.connect(lambda: self.action_save(self.tab_window))

        self.combined_schoolclass = QCheckBox(self.lng['combined_schoolclass'], mytab)
        top_pos = self.table_top - label_students.height() - self.combined_schoolclass.height() + 5
        self.combined_schoolclass.move(self.table_left, top_pos + 5)
        self.combined_schoolclass.clicked.connect(self.schoolclass_combined_change)

        self.listbox_schoolclass = QComboBox(mytab)
        list_schoolclass = self.get_schoolclassnames()
        list_schoolclass = sort(list_schoolclass)
        for i in list_schoolclass:
            self.listbox_schoolclass.addItem(i)
        top_pos -= self.listbox_schoolclass.height()
        self.listbox_schoolclass.move(self.table_left + 100, top_pos)
        self.listbox_schoolclass.currentIndexChanged.connect(self.schoolclass_change)

        label_schoolclass = QLabel(self.lng['schoolclass'], mytab)
        label_schoolclass.move(self.table_left, top_pos + 5)

        self.listbox_schoolyear = QComboBox(mytab)
        list_schoolyear = self.get_schoolyears()
        list_schoolyear = sort(list_schoolyear, reverse=True)
        for i in list_schoolyear:
            self.listbox_schoolyear.addItem(i)
        top_pos -= self.listbox_schoolyear.height()
        self.listbox_schoolyear.move(self.table_left + 100, top_pos)
        self.listbox_schoolyear.currentIndexChanged.connect(self.schoolyear_change)

        label_schoolyear = QLabel(self.lng['schoolyear'], mytab)
        label_schoolyear.move(self.table_left, top_pos + 5)

        # load Content from Database
        self.load_data(1, 0)
        self.my_table.resizeColumnsToContents()

        self.set_changed(False)
        self.button_add.setFocus()

        if not self.listbox_schoolyear or not self.listbox_schoolclass:
            QMessageBox.critical(self.tab_window, self.lng['title'], self.lng['msg_missing_parameter'])
            self.button_add.setEnabled(False)
            self.button_remove.setEnabled(False)

    def load_image(self, filename):
        # TODO: does not work if placed in parent class
        pixmap = QPixmap(filename)
        if filename and isfile(filename):
            pixmap = pixmap.scaled(self.student_image_height,
                                   self.student_image_width,
                                   QtCore.Qt.KeepAspectRatio)
        self.image_window.setPixmap(pixmap)

    def action_select(self, cell=None, limit_column=[]):
        student_image_column = 5
        image_data_temp = self.my_table.item(cell.row(), student_image_column).text()
        self.load_image(image_data_temp)

    def define_column_title(self):
        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

    @property
    def export_file_title(self):
        schoolyear = self.listbox_schoolyear.currentText()
        schoolclass = self.listbox_schoolclass.currentText()
        return "%s_%s" % (schoolyear, schoolclass)

    def _define_column_title(self):
        return [{'name': self.lng['lastname'], 'type': 'string', 'unique': False},
                {'name': self.lng['firstname'], 'type': 'string', 'unique': False},
                {'name': self.lng['real_schoolclass'],
                 'type': 'list',
                 'unique': False,
                 'list': self.get_schoolclassnames(),
                 'handle': self.schoolclass_combined,
                 'default': self.schoolclass_name},
                {'name': self.lng['comment'], 'type': 'string', 'unique': False},
                {'name': 'image_filename', 'type': 'image', 'unique': False, 'hide': True}
                ]

    def schoolclass_combined_change(self):
        school_class_combined_column_nr = 3
        self.schoolclass_combined = self.combined_schoolclass.isChecked()
        self.my_table.setColumnHidden(school_class_combined_column_nr, not self.schoolclass_combined)
        self.set_changed(True)
        self.define_column_title()

    def schoolclass_change(self, index):
        self.schoolclass_name = self.listbox_schoolclass.currentText()
        self.schoolclass_listindex = self._change(self.listbox_schoolclass, self.schoolclass_listindex, index)
        self.define_column_title()

    def schoolyear_change(self, index):
        self.schoolyear_listindex = self._change(self.listbox_schoolyear, self.schoolyear_listindex, index)

    def _action_load_content(self):
        is_combined_school_class = self.dbh.get_schoolclass_combine(schoolyear=self.listbox_schoolyear.currentText(),
                                                                    schoolclassname=self.listbox_schoolclass.currentText()
                                                                    )
        self.combined_schoolclass.setChecked(is_combined_school_class)
        self.schoolclass_combined_change()
        self.set_changed(False)

        return self.dbh.get_students(schoolyear=self.listbox_schoolyear.currentText(),
                                     schoolclass=self.listbox_schoolclass.currentText()
                                     )

    def _action_save_content(self, data):
        self.dbh.set_schoolclass_combine(schoolyear=self.listbox_schoolyear.currentText(),
                                         schoolclassname=self.listbox_schoolclass.currentText(),
                                         combined_schoolclass=self.combined_schoolclass.isChecked()
                                         )
        self.dbh.set_students(schoolyear=self.listbox_schoolyear.currentText(),
                              schoolclass=self.listbox_schoolclass.currentText(),
                              students=data
                              )
        self.set_changed(False)
        return True

    def _set_changed(self, status):
        if status:
            if not self.listbox_schoolyear.currentText():
                return False
            if not self.listbox_schoolclass.currentText():
                return False
        return True

    def student_edit(self, cell):
        self.action_edit(cell)
        self.set_changed(True)

    def student_remove(self):
        selection = self.my_table.currentRow()
        if selection < 0:
            return
        self.my_table.removeRow(selection)
        self.set_changed(True)

    def student_import_csv(self):
        data = CSVImport(self.tab_window, lng=self.lng)
        for student in data.students:
            # incoming Tuple
            # Lastname, Firstname, Comment
            student = list(student[1:len(student)])
            student.append(student[len(student) - 1])
            student[DB_SCHOOLCLASS_SCHOOLCLASS_INDEX] = self.listbox_schoolclass.currentText()
            # modified to
            # Lastname, Firstname, Schoolclass, Comment
            student = tuple(student)
            self.action_add(data_import=True, data=student)

    def student_import_other_class(self):
        schoolyear_list = []
        schoolclass_list = []

        for y in self.dbh.get_schoolyear():
            schoolyear_list.append(y[1])
        for c in self.dbh.get_schoolclassname():
            schoolclass_list.append(c[1])

        schoolyear_list = sort(schoolyear_list, reverse=True)
        if not schoolyear_list:
            QMessageBox.information(self.tab_window, self.lng['title'], self.lng['msg_no_schoolyear'])
            return
        schoolclass_list = sort(schoolclass_list)
        if not schoolclass_list:
            QMessageBox.information(self.tab_window, self.lng['title'], self.lng['msg_no_schoolclass'])
            return

        import_dialog = ExtendedQInputDialog(parent=self.tab_window)
        schoolyear, ok = import_dialog.getItem(self.tab_window, self.lng['title'], self.lng['schoolyear'], schoolyear_list, 0, False)
        if not ok:
            return
        schoolclass, ok = import_dialog.getItem(self.tab_window, self.lng['title'], self.lng['schoolclass'], schoolclass_list, 0, False)
        if not ok:
            return

        student_list = self.dbh.get_students(schoolyear=schoolyear, schoolclass=schoolclass)
        for student in student_list:
            # remove first element of tuple (id Field)
            student = list(student[1:len(student)])
            student[DB_SCHOOLCLASS_SCHOOLCLASS_INDEX] = self.listbox_schoolclass.currentText()
            student = tuple(student)
            self.action_add(data_import=True, data=student)

    def do_csv_export(self):
        schoolyear = self.listbox_schoolyear.currentText()
        schoolclass = self.listbox_schoolclass.currentText()
        filename = "%s_%s" % (schoolyear, schoolclass)
        self.configure_export_csv(parent=self.tab_window, default_filename=filename)

    def pdf_template(self, obj, data):
        y = obj.body_max_y
        x = obj.body_min_x

        font_width = round(obj.font_size * 3/5, 0)

        lastname_max_len = len(self.lng['lastname'])
        firstname_max_len = len(self.lng['firstname'])

        for row in data:
            if len(row[1]) > lastname_max_len:
                lastname_max_len = len(row[1])
            if len(row[2]) > firstname_max_len:
                firstname_max_len = len(row[2])

        lastname_width = font_width * lastname_max_len
        firstname_width = font_width * firstname_max_len

        offset = 0
        obj.drawString(x, y, self.lng['lastname'])
        offset += lastname_width
        obj.drawString(x + offset, y, self.lng['firstname'])
        offset += firstname_width
        obj.drawString(x + offset, y, self.lng['comment'])
        offset += 100
        y -= 4
        obj.line(x, y, x + offset, y)

        for row in data:
            y -= obj.font_size
            offset = 0
            obj.drawString(x, y, row[1])
            offset += lastname_width
            obj.drawString(x + offset, y, row[2])
            offset += firstname_width
            obj.drawString(x + offset, y, row[3])

    @property
    def pdf_head_text(self):
        return "%s: %s %s" % (self.lng['schoolclass'], self.listbox_schoolyear.currentText(), self.listbox_schoolclass.currentText())

    @property
    def pdf_foot_text(self):
        return ""


class ViewExamConfigure(ViewConfigure):

    subject_listindex = 0

    def __init__(self, dbhandler, root_tab, lng):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()

        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        label_students = QLabel(self.lng['exams'], mytab)
        label_students.move(self.table_left, self.table_top - 20)

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)
        self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        self.button_add = QPushButton(self.lng['add'], mytab)
        self.button_add.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_add.clicked.connect(self.action_add)

        self.button_edit = QPushButton(lng['edit'], mytab)
        self.button_edit.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height())
        self.button_edit.clicked.connect(self.change_result)

        self.button_remove = QPushButton(self.lng['remove'], mytab)
        self.button_remove.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height() + self.button_edit.height())
        self.button_remove.clicked.connect(self.action_remove)

        self.button_export = QToolButton(mytab)
        self.button_export.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height() + self.button_edit.height() + self.button_remove.height())
        self.button_export.setText(self.lng['export'])
        self.button_export.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.lng['csv_export'], lambda: self.do_csv_export())
        menu.addAction(self.lng['pdf_export'], lambda: self.do_pdf_export(self.export_file_title))
        self.button_export.setMenu(menu)

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

        self.my_table.setSortingEnabled(self.sorting)

        self.my_table.doubleClicked.connect(self.change_result)

        # dummy Button
        self.button_save = QPushButton(lng['save'], mytab)
        self.button_save.setVisible(False)
        self.button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        self.button_save.clicked.connect(lambda: self.action_save(self.tab_window))

        self.listbox_subject = QComboBox(mytab)
        list_subject = self.get_subjectnames()
        list_subject = sort(list_subject)
        for i in list_subject:
            self.listbox_subject.addItem(i)
        top_pos = self.table_top - label_students.height() - self.listbox_subject.height() + 5
        self.listbox_subject.move(self.table_left + 100, top_pos)
        self.listbox_subject.currentIndexChanged.connect(self.subject_change)
        
        label_subject = QLabel(self.lng['subject'], mytab)
        label_subject.move(self.table_left, top_pos + 5)

        self.listbox_schoolclass = QComboBox(mytab)
        list_schoolclass = self.get_schoolclassnames()
        list_schoolclass = sort(list_schoolclass)
        for i in list_schoolclass:
            self.listbox_schoolclass.addItem(i)
        top_pos -= self.listbox_schoolclass.height()
        self.listbox_schoolclass.move(self.table_left + 100, top_pos)
        self.listbox_schoolclass.currentIndexChanged.connect(self.schoolclass_change)

        label_schoolclass = QLabel(self.lng['schoolclass'], mytab)
        label_schoolclass.move(self.table_left, top_pos + 5)

        self.listbox_schoolyear = QComboBox(mytab)
        list_schoolyear = self.get_schoolyears()
        list_schoolyear = sort(list_schoolyear, reverse=True)
        for i in list_schoolyear:
            self.listbox_schoolyear.addItem(i)
        top_pos -= self.listbox_schoolyear.height()
        self.listbox_schoolyear.move(self.table_left + 100, top_pos)
        self.listbox_schoolyear.currentIndexChanged.connect(self.schoolyear_change)

        label_schoolyear = QLabel(self.lng['schoolyear'], mytab)
        label_schoolyear.move(self.table_left, top_pos + 5)

        # load Content from Database
        self.load_data()
        self.my_table.resizeColumnsToContents()

        self.set_changed(False)
        self.button_add.setFocus()

        if not self.listbox_schoolyear or not self.listbox_schoolclass or not self.listbox_subject:
            QMessageBox.critical(self.tab_window, self.lng['title'], self.lng['msg_missing_parameter'])
            self.button_add.setEnabled(False)
            self.button_remove.setEnabled(False)

    @property
    def export_file_title(self):
        schoolyear = self.listbox_schoolyear.currentText()
        schoolclass = self.listbox_schoolclass.currentText()
        subject = self.listbox_subject.currentText()
        return "%s_%s_%s" % (schoolyear, schoolclass, subject)

    def _define_column_title(self):
        return [{'name': self.lng['date'], 'type': 'string', 'unique': False},
                {'name': self.lng['examtype'], 'type': 'string', 'unique': False},
                {'name': self.lng['timeperiod'], 'type': 'string', 'unique': False},
                {'name': self.lng['count'], 'type': 'float', 'unique': False},
                {'name': self.lng['average'], 'type': 'float', 'unique': False},
                {'name': self.lng['exam_description'], 'type': 'string', 'unique': False},
                ]

    def schoolclass_change(self, index):
        self.schoolclass_listindex = self._change(self.listbox_schoolclass, self.schoolclass_listindex, index)
    
    def schoolyear_change(self, index):
        self.schoolyear_listindex = self._change(self.listbox_schoolyear, self.schoolyear_listindex, index)

    def subject_change(self, index):
        self.subject_listindex = self._change(self.listbox_subject, self.subject_listindex, index)

    def action_add(self, data_import=False, data=()):
        answer = QMessageBox.question(self.tab_window, self.lng['title'], self.lng['msg_is_singletest'])
        if answer == QMessageBox.Yes:
            single_test = True
        else:
            single_test = False

        students = self.dbh.get_students(schoolyear=self.listbox_schoolyear.currentText(),
                                         schoolclass=self.listbox_schoolclass.currentText()
                                         )
        student_list = []
        for s in students:
            student_list.append((s[0], s[1], s[2], "", ""))

        exam_data = {
            'schoolyear': self.listbox_schoolyear.currentText(),
            'schoolclass': self.listbox_schoolclass.currentText(),
            'subject': self.listbox_subject.currentText(),
            'students': student_list
        }

        Exam(self.dbh, self.tab_window, self.lng, type='add', single_test=single_test, exam_data=exam_data)
        self.load_data()

    def action_remove(self, cell):
        column = 0
        try:
            row = self.my_table.currentItem().row()
        except AttributeError:
            return
        answer = QMessageBox.question(self.tab_window, self.lng['title'], self.lng['msg_remove_exam'])
        if answer == QMessageBox.No:
            return
        exam_id = self.my_table.item(row, column).text()
        self.dbh.remove_exam(exam_id=exam_id)
        self.load_data()

    def change_result(self, cell=None):
        try:
            row = cell.row()
        except AttributeError:
            try:
                row = self.my_table.selectedIndexes()[0].row()
            except IndexError:
                row = 0
        column = 0
        exam_id = self.my_table.item(row, column).text()

        exam_data = {
            'exam_id': exam_id,
        }
        Exam(self.dbh, self.tab_window, self.lng, type='edit', exam_data=exam_data)
        self.load_data()

    def _set_changed(self, status):
        if status:
            if not self.listbox_schoolyear.currentText():
                return False
            if not self.listbox_schoolclass.currentText():
                return False
            if not self.listbox_subject.currentText():
                return False
        return True

    def _action_load_content(self):
        schoolyear = self.listbox_schoolyear.currentText()
        schoolclassname = self.listbox_schoolclass.currentText()
        subject = self.listbox_subject.currentText()
        return self.dbh.get_exams(schoolyear, schoolclassname, subject)

    def do_csv_export(self):
        schoolyear = self.listbox_schoolyear.currentText()
        schoolclass = self.listbox_schoolclass.currentText()
        subject = self.listbox_subject.currentText()
        filename = "%s_%s_%s" % (schoolyear, schoolclass, subject)
        self.configure_export_csv(parent=self.tab_window, default_filename=filename)

    def pdf_template(self, obj, data):
        y = obj.body_max_y
        x = obj.body_min_x

        font_width = round(obj.font_size * 3/5, 0)

        date_max_len = len(self.lng['date'])
        examtype_max_len = len(self.lng['examtype'])
        timeperiod_max_len = len(self.lng['timeperiod'])
        count_max_len = len(self.lng['count'])
        average_max_len = len(self.lng['average'])

        for row in data:
            if len(row[1]) > date_max_len:
                date_max_len = len(row[1])
            if len(row[2]) > examtype_max_len:
                examtype_max_len = len(row[2])
            if len(row[3]) > timeperiod_max_len:
                timeperiod_max_len= len(row[3])
            if len(row[4]) > count_max_len:
                count_max_len = len(row[4])
            if len(str(row[5])) > average_max_len:
                average_max_len = len(str(row[5]))

        date_width = font_width * date_max_len
        exam_type_width = font_width * examtype_max_len
        timeperiod_width = font_width * timeperiod_max_len
        count_width = font_width * count_max_len
        average_width = font_width * average_max_len

        offset = 0
        obj.drawString(x, y, self.lng['date'])
        offset += date_width
        obj.drawString(x + offset, y, self.lng['examtype'])
        offset += exam_type_width
        obj.drawString(x + offset, y, self.lng['timeperiod'])
        offset += timeperiod_width
        obj.drawString(x + offset, y, self.lng['count'])
        offset += count_width
        obj.drawString(x + offset, y, self.lng['average'])
        offset += average_width
        obj.drawString(x + offset, y, self.lng['comment'])
        y -= 4
        obj.line(x, y, x + offset + 100, y)

        for row in data:
            y -= obj.font_size
            offset = 0
            obj.drawString(x, y, row[1])
            offset += date_width
            obj.drawString(x + offset, y, row[2])
            offset += exam_type_width
            obj.drawString(x + offset, y, row[3])
            offset += timeperiod_width
            obj.drawString(x + offset, y, row[4])
            offset += count_width
            obj.drawString(x + offset, y, str(row[5]))
            offset += average_width
            obj.drawString(x + offset, y, row[6])

    @property
    def pdf_head_text(self):
        return "%s: %s %s %s" % (self.lng['exams'], self.listbox_schoolyear.currentText(), self.listbox_schoolclass.currentText(), self.listbox_subject.currentText())

    @property
    def pdf_foot_text(self):
        return ""
