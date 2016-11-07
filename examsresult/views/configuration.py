from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, \
    QPushButton, QComboBox, QMessageBox, QToolButton, QMenu, QInputDialog
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
        ret = []
        for i in self.dbh.get_schoolclassname():
            ret.append(i[1])
        return ret

    def get_schoolyears(self):
        ret = []
        for i in self.dbh.get_schoolyear():
            ret.append(i[1])
        return ret

    def get_subjectnames(self):
        ret = []
        for i in self.dbh.get_subject():
            ret.append(i[1])
        return ret

    def get_examtypenames(self):
        ret = []
        for i in self.dbh.get_examtype():
            ret.append(i[1])
        return ret

    def get_timeperiodnames(self):
        ret = []
        for i in self.dbh.get_timeperiod():
            ret.append(i[1])
        return ret


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

        self.button_import = QToolButton(mytab)
        self.button_import.move(self.table_left + self.table_width + self.button_add.width(), self.table_top)
        self.button_import.setText(self.lng['import'])
        self.button_import.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.lng['import_csv'], self.student_import_csv)
        menu.addAction(self.lng['import_other_schoolclass'], self.student_import_other_class)
        self.button_import.setMenu(menu)

        # hide Column 'id'
        #        table.setColumnHidden(0, True)

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
        self.load_data()

        self.set_changed(False)
        self.button_add.setFocus()

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

        # hide Column 'id'
        #        table.setColumnHidden(0, True)

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

        self.set_changed(False)
        self.button_add.setFocus()

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
        examtype_list = self.get_examtypenames()
        timeperiod_list = self.get_timeperiodnames()

        if not examtype_list:
            QMessageBox.critical(self.tab_window, self.lng['title'], self.lng['msg_no_examtype'])
            return
        if not timeperiod_list:
            QMessageBox.critical(self.tab_window, self.lng['title'], self.lng['msg_no_timeperiod'])
            return

        dialog = QInputDialog()
        examtype, ok = dialog.getItem(self.tab_window, self.lng['title'], self.lng['examtype'], examtype_list, 0, False)
        if not ok:
            return
        timeperiod, ok = dialog.getItem(self.tab_window, self.lng['title'], self.lng['timeperiod'], timeperiod_list, 0, False)
        if not ok:
            return
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
            'examtype': examtype,
            'timeperiod': timeperiod,
            'students': student_list
        }

        Exam(self.dbh, self.tab_window, self.lng, type='add', single_test=single_test, exam_data=exam_data)
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
