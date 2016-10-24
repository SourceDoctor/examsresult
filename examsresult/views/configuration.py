from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, QPushButton, QComboBox
from examsresult.views import CoreView


class ViewConfigure(CoreView):
    pass


class ViewSchoolClassConfigure(ViewConfigure):

    table_left = 100
    table_top = 120
    table_height = 350
    table_width = 300

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

        self.button_student_add = QPushButton(self.lng['add'], mytab)
        self.button_student_add.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_student_add.clicked.connect(self.student_add)
        
        self.button_student_remove = QPushButton(self.lng['remove'], mytab)
        self.button_student_remove.move(self.table_left + self.table_width + 10, self.table_top + self.button_student_add.height())
        self.button_student_remove.clicked.connect(self.student_remove)

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

        self.button_save = QPushButton(lng['save'], mytab)
        self.button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        self.button_save.clicked.connect(lambda: self.action_save(self.tab_window))

        self.listbox_schoolclass = QComboBox(mytab)
        self.listbox_schoolclass.move(self.table_left + 100,
                                      self.table_top - label_students.height() - self.listbox_schoolclass.height())

        label_schoolclass = QLabel(self.lng['schoolclass'], mytab)
        label_schoolclass.move(self.table_left, self.table_top - label_students.height() - self.listbox_schoolclass.height() + 5)

        self.listbox_schoolyear = QComboBox(mytab)
        self.listbox_schoolyear.move(self.table_left + 100,
                             self.table_top - label_students.height() - self.listbox_schoolyear.height() - self.listbox_schoolclass.height())

        label_schoolyear = QLabel(self.lng['schoolyear'], mytab)
        label_schoolyear.move(self.table_left, self.table_top - label_students.height() - self.listbox_schoolyear.height() - self.listbox_schoolclass.height() + 5)

        self.set_changed(False)

    def _define_column_title(self):
        return [{'name': self.lng['firstname'], 'type': 'string', 'unique': False},
                {'name': self.lng['lastname'], 'type': 'string', 'unique': False}
                ]

    def action_save(self, root_window):
        self.set_changed(False)

    def set_changed(self, status):
        if status:
            if not self.listbox_schoolyear.currentText():
                return
            if not self.listbox_schoolclass.currentText():
                return
        self.button_save.setEnabled(status)

    def student_add(self):
        self.set_changed(True)

    def student_edit(self, index):
        self.set_changed(True)

    def student_remove(self, index):
        self.set_changed(True)
