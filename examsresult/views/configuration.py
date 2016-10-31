from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, \
    QPushButton, QComboBox, QMessageBox, QTableWidgetItem
from examsresult.views import CoreView


class ViewConfigure(CoreView):
    pass


class ViewSchoolClassConfigure(ViewConfigure):

    table_left = 100
    table_top = 120
    table_height = 350
    table_width = 500

    schoolyear_listindex = 0
    schoolyear_change_enabled = True
    schoolclass_listindex = 0
    schoolclass_change_enabled = True

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
        self.button_add.clicked.connect(self.student_add)
        
        self.button_remove = QPushButton(self.lng['remove'], mytab)
        self.button_remove.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height())
        self.button_remove.clicked.connect(self.student_remove)

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

        self.set_changed(False)
        self.button_add.setFocus()

    def _define_column_title(self):
        return [{'name': self.lng['firstname'], 'type': 'string', 'unique': False},
                {'name': self.lng['lastname'], 'type': 'string', 'unique': False},
                {'name': self.lng['comment'], 'type': 'string', 'unique': False}
                ]

    def schoolclass_change(self, index):
        if not self.schoolclass_change_enabled:
            self.schoolclass_change_enabled = True
            return
        if self.is_changed:
            answer = QMessageBox.question(self.tab_window, self.lng['title'], self.lng['msg_switch_unsaved'])
            if answer == QMessageBox.No:
                self.schoolclass_change_enabled = False
                self.listbox_schoolclass.setCurrentIndex(self.schoolclass_listindex)
                return
            self.set_changed(False)
        self.students_load(schoolyear=self.listbox_schoolyear.currentText(),
                           schoolclass=self.listbox_schoolclass.currentText())
        self.schoolclass_listindex = index

    def schoolyear_change(self, index):
        if not self.schoolyear_change_enabled:
            self.schoolyear_change_enabled = True
            return
        if self.is_changed:
            answer = QMessageBox.question(self.tab_window, self.lng['title'], self.lng['msg_switch_unsaved'])
            if answer == QMessageBox.No:
                self.schoolyear_change_enabled = False
                self.listbox_schoolyear.setCurrentIndex(self.schoolyear_listindex)
                return
        self.set_changed(False)
        self.students_load(schoolyear=self.listbox_schoolyear.currentText(),
                           schoolclass=self.listbox_schoolclass.currentText())
        self.schoolyear_listindex = index

    def _action_load_content(self):
        return self.dbh.get_students(schoolyear=self.listbox_schoolyear.currentText(),
                                     schoolclass=self.listbox_schoolclass.currentText()
                                     )

    def _action_save_content(self, data):
        self.dbh.set_students(schoolyear=self.listbox_schoolyear.currentText(),
                              schoolclass=self.listbox_schoolclass.currentText(),
                              students=data)
        self.set_changed(False)

    def load_data(self):
        # clear table
        while self.my_table.rowCount():
            self.my_table.removeRow(0)
        # load data from Database
        data_list = self._action_load_content()
        for data in data_list:
            self.my_table.insertRow(self.my_table.rowCount())
            column = 0
            while column <= len(self.column_title) - 1:
                self.my_table.setItem(self.my_table.rowCount() - 1, column, QTableWidgetItem(str(data[column])))
                column += 1

    def action_save(self, root_window):
        data = []
        row = 0
        while row <= self.my_table.rowCount() - 1:
            row_content = ()
            column = 0
            while column <= self.my_table.columnCount() - 1:
                cell = self.my_table.item(row, column).text()
                row_content += (cell,)
                column += 1
            data.append(row_content)
            row += 1

        self._action_save_content(data=data)
        self.load_data()
        self.set_changed(False)

    def _set_changed(self, status):
        if status:
            if not self.listbox_schoolyear.currentText():
                return False
            if not self.listbox_schoolclass.currentText():
                return False
        return True

    def student_add(self):
        self.action_add()
        self.set_changed(True)

    def student_edit(self, cell):
        self.action_edit(cell)
        self.set_changed(True)

    def student_remove(self):
        selection = self.my_table.currentRow()
        if not selection:
            return
        self.my_table.removeRow(selection)
        self.set_changed(True)

    def students_load(self, schoolyear, schoolclass):
        self.load_data()

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
