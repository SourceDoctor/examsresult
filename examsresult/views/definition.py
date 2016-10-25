from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QMessageBox, \
    QPushButton, QInputDialog, QAbstractItemView
from .core import CoreView


class ViewDefine(CoreView):
    # Fixme: if tab added, and before Tabview was empty, first one has no buttons

    def __init__(self, dbhandler, root_tab, lng):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = []
        self.column_title.append({'name':'id', 'type':'int', 'unique':True, 'editable':False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()
        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
        self.my_table.setHorizontalHeaderLabels(column_tuple)

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

        self.button_add = QPushButton(lng['add'], mytab)
        self.button_add.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_add.clicked.connect(self.action_add)

        self.button_save = QPushButton(lng['save'], mytab)
        self.button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        self.button_save.clicked.connect(lambda: self.action_save(self.tab_window))

        # load Content from Database
        self.load_data()

        self.set_changed(False)
        self.button_add.setFocus()

    def _action_load_content(self):
        QMessageBox.information(self.tab_window, self.lng['title'], "Tell me how to load!")
        return []

    def _action_save_content(self, data):
        QMessageBox.information(self.tab_window, self.lng['title'], "Tell me how to save!")
        return 0

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


class ViewSchoolYear(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True}]

    def _action_save_content(self, data):
        ret = self.dbh.set_schoolyear(data=data)
        return ret

    def _action_load_content(self):
        return self.dbh.get_schoolyear()


class ViewSchoolClass(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True}]

    def _action_save_content(self, data):
        ret = self.dbh.set_schoolclassname(data=data)
        return ret

    def _action_load_content(self):
        return self.dbh.get_schoolclassname()


class ViewSubject(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True}]

    def _action_save_content(self, data):
        ret = self.dbh.set_subject(data=data)
        return ret

    def _action_load_content(self):
        return self.dbh.get_subject()


class ViewExamsType(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True},
                {'name': self.lng['weight'], 'type': 'float', 'unique': False}
                ]

    def _action_save_content(self, data):
        ret = self.dbh.set_examtype(data=data)
        return ret

    def _action_load_content(self):
        return self.dbh.get_examtype()


class ViewTimeperiod(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True},
                {'name': self.lng['weight'], 'type': 'float', 'unique': False}
                ]

    def _action_save_content(self, data):
        ret = self.dbh.set_timeperiod(data=data)
        return ret

    def _action_load_content(self):
        return self.dbh.get_timeperiod()
