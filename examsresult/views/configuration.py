from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, \
    QPushButton, QComboBox, QMessageBox, QToolButton, QMenu, QInputDialog

from examsresult.tools import HIDE_ID_COLUMN
from examsresult.views import CoreView
from examsresult.views.exam_handler import Exam
from examsresult.views.import_csv import CSVImport


class ViewConfigure(CoreView):

    table_left = 100
    table_top = 130
    table_height = 350
    table_width = 500

    schoolyear_listindex = 0
    schoolyear_change_enabled = True
    schoolclass_listindex = 0
    schoolclass_change_enabled = True

    def _change(self, change_enabled, change_listbox, change_index, index):
        if not change_enabled:
            change_enabled = True
            return
        if self.is_changed:
            answer = QMessageBox.question(self.tab_window, self.lng['title'], self.lng['msg_switch_unsaved'])
            if answer == QMessageBox.No:
                change_enabled = False
                change_listbox.setCurrentIndex(change_index)
                return
            self.set_changed(False)
        self.load_data()
        change_index = index

    def get_schoolclassnames(self):
        return [x[1] for x in self.dbh.get_schoolclassname()]

    def get_schoolyears(self):
        return [x[1] for x in self.dbh.get_schoolyear()]

    def get_subjectnames(self):
        return [x[1] for x in self.dbh.get_subject()]


class ViewSchoolClassConfigure(ViewConfigure):

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

        label_students = QLabel(self.lng['students'], mytab)
        label_students.move(self.table_left, self.table_top - 20)

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        self.button_add = QPushButton(self.lng['add'], mytab)
        self.button_add.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_add.clicked.connect(self.action_add)
        
        self.button_remove = QPushButton(self.lng['remove'], mytab)
        self.button_remove.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height())
        self.button_remove.clicked.connect(self.student_remove)

        self.button_export = QToolButton(mytab)
        self.button_export.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height() + self.button_remove.height())
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

        # hide Column 'id'
        self.my_table.setColumnHidden(0, HIDE_ID_COLUMN)

        if self.row_title:
            self.my_table.setVerticalHeaderLabels(self.row_title)

        if self.full_row_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        if self.full_column_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectColumns)

        if self.cell_editable:
            self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Fixme: on doubleclick-Edit Cell has blinking Cursor focus

        self.my_table.setSortingEnabled(self.sorting)

        self.my_table.doubleClicked.connect(self.action_edit)

        self.button_save = QPushButton(lng['save'], mytab)
        self.button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        self.button_save.clicked.connect(lambda: self.action_save(self.tab_window))

        self.listbox_schoolclass = QComboBox(mytab)
        for i in self.get_schoolclassnames():
            self.listbox_schoolclass.addItem(i)
        self.listbox_schoolclass.move(self.table_left + 100,
                                      self.table_top - label_students.height() - self.listbox_schoolclass.height())
        self.listbox_schoolclass.currentIndexChanged.connect(self.schoolclass_change)

        label_schoolclass = QLabel(self.lng['schoolclass'], mytab)
        label_schoolclass.move(self.table_left, self.table_top - label_students.height() - self.listbox_schoolclass.height() + 5)

        self.listbox_schoolyear = QComboBox(mytab)
        for i in self.get_schoolyears():
            self.listbox_schoolyear.addItem(i)
        self.listbox_schoolyear.move(self.table_left + 100,
                             self.table_top - label_students.height() - self.listbox_schoolyear.height() - self.listbox_schoolclass.height())
        self.listbox_schoolyear.currentIndexChanged.connect(self.schoolyear_change)

        label_schoolyear = QLabel(self.lng['schoolyear'], mytab)
        label_schoolyear.move(self.table_left, self.table_top - label_students.height() - self.listbox_schoolyear.height() - self.listbox_schoolclass.height() + 5)

        # load Content from Database
        self.load_data(1, 0)
        self.my_table.resizeColumnsToContents()

        self.set_changed(False)
        self.button_add.setFocus()

        if not self.listbox_schoolyear or not self.listbox_schoolclass:
            QMessageBox.critical(self.tab_window, self.lng['title'], self.lng['msg_missing_parameter'])
            self.button_add.setEnabled(False)
            self.button_remove.setEnabled(False)

    @property
    def export_file_title(self):
        schoolyear = self.listbox_schoolyear.currentText()
        schoolclass = self.listbox_schoolclass.currentText()
        return "%s_%s" % (schoolyear, schoolclass)

    def _define_column_title(self):
        return [{'name': self.lng['lastname'], 'type': 'string', 'unique': False},
                {'name': self.lng['firstname'], 'type': 'string', 'unique': False},
                {'name': self.lng['comment'], 'type': 'string', 'unique': False}
                ]

    def schoolclass_change(self, index):
        self._change(self.schoolclass_change_enabled, self.listbox_schoolclass, self.schoolclass_listindex, index)

    def schoolyear_change(self, index):
        self._change(self.schoolyear_change_enabled, self.listbox_schoolyear, self.schoolyear_listindex, index)

    def _action_load_content(self):
        return self.dbh.get_students(schoolyear=self.listbox_schoolyear.currentText(),
                                     schoolclass=self.listbox_schoolclass.currentText()
                                     )

    def _action_save_content(self, data):
        self.dbh.set_students(schoolyear=self.listbox_schoolyear.currentText(),
                              schoolclass=self.listbox_schoolclass.currentText(),
                              students=data)
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
            self.action_add(data_import=True, data=student)

    def student_import_other_class(self):
        schoolyear_list = []
        schoolclass_list = []

        for y in self.dbh.get_schoolyear():
            schoolyear_list.append(y[1])
        for c in self.dbh.get_schoolclassname():
            schoolclass_list.append(c[1])

        if not schoolyear_list:
            QMessageBox.information(self.tab_window, self.lng['title'], self.lng['msg_no_schoolyear'])
            return
        if not schoolclass_list:
            QMessageBox.information(self.tab_window, self.lng['title'], self.lng['msg_no_schoolclass'])
            return

        import_dialog = QInputDialog(parent=self.tab_window)
        schoolyear, ok = import_dialog.getItem(self.tab_window, self.lng['title'], self.lng['schoolyear'], schoolyear_list, 0, False)
        if not ok:
            return
        schoolclass, ok = import_dialog.getItem(self.tab_window, self.lng['title'], self.lng['schoolclass'], schoolclass_list, 0, False)
        if not ok:
            return

        student_list = self.dbh.get_students(schoolyear=schoolyear, schoolclass=schoolclass)
        for student in student_list:
            # remove first element of tuple (id Field)
            student = student[1:len(student)]
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
    subject_change_enabled = True

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

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        self.button_add = QPushButton(self.lng['add'], mytab)
        self.button_add.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_add.clicked.connect(self.action_add)

        self.button_remove = QPushButton(self.lng['remove'], mytab)
        self.button_remove.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height())
        self.button_remove.clicked.connect(self.action_remove)

        self.button_export = QToolButton(mytab)
        self.button_export.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height() + self.button_remove.height())
        self.button_export.setText(self.lng['export'])
        self.button_export.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.lng['csv_export'], lambda: self.do_csv_export())
        menu.addAction(self.lng['pdf_export'], lambda: self.do_pdf_export(self.export_file_title))
        self.button_export.setMenu(menu)

        # hide Column 'id'
        self.my_table.setColumnHidden(0, HIDE_ID_COLUMN)

        if self.row_title:
            self.my_table.setVerticalHeaderLabels(self.row_title)

        if self.full_row_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        if self.full_column_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectColumns)

        if self.cell_editable:
            self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Fixme: on doubleclick-Edit Cell has blinking Cursor focus

        self.my_table.setSortingEnabled(self.sorting)

        self.my_table.doubleClicked.connect(self.change_result)

        # dummy Button
        self.button_save = QPushButton(lng['save'], mytab)
        self.button_save.setVisible(False)
        self.button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        self.button_save.clicked.connect(lambda: self.action_save(self.tab_window))

        self.listbox_subject = QComboBox(mytab)
        for i in self.get_subjectnames():
            self.listbox_subject.addItem(i)
        self.listbox_subject.move(self.table_left + 100, 80)
        self.listbox_subject.currentIndexChanged.connect(self.subject_change)
        
        label_subject = QLabel(self.lng['subject'], mytab)
        label_subject.move(self.table_left, 80)

        self.listbox_schoolclass = QComboBox(mytab)
        for i in self.get_schoolclassnames():
            self.listbox_schoolclass.addItem(i)
        self.listbox_schoolclass.move(self.table_left + 100, 50)
        self.listbox_schoolclass.currentIndexChanged.connect(self.schoolclass_change)

        label_schoolclass = QLabel(self.lng['schoolclass'], mytab)
        label_schoolclass.move(self.table_left, 50)

        self.listbox_schoolyear = QComboBox(mytab)
        for i in self.get_schoolyears():
            self.listbox_schoolyear.addItem(i)
        self.listbox_schoolyear.move(self.table_left + 100, 20)
        self.listbox_schoolyear.currentIndexChanged.connect(self.schoolyear_change)

        label_schoolyear = QLabel(self.lng['schoolyear'], mytab)
        label_schoolyear.move(self.table_left, 20)

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
        self._change(self.schoolclass_change_enabled, self.listbox_schoolclass, self.schoolclass_listindex, index)
    
    def schoolyear_change(self, index):
        self._change(self.schoolyear_change_enabled, self.listbox_schoolyear, self.schoolyear_listindex, index)

    def subject_change(self, index):
        self._change(self.subject_change_enabled, self.listbox_subject, self.subject_listindex, index)

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

    def change_result(self, cell):
        row = cell.row()
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
