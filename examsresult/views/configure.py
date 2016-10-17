from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QMessageBox, QPushButton


class ViewConfigure(object):
    # Fixme: if tab added, and before Tabview was empty, first one has no buttons
    lng = {}
    column_title = ()
    row_title = ()

    table_left = 0
    table_top = 0
    table_height = 200
    table_width = 200

    sorting = True
    header_horizontal = True
    header_vertical = False

    def __init__(self, root_tab, lng):
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = ('id',) + self._define_column_title()

        # Todo: check after Change if Cell is empty, then Error !
        mytab = QWidget()
        table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        table.setColumnCount(len(self.column_title))

        table.verticalHeader().setVisible(self.header_vertical)
        table.horizontalHeader().setVisible(self.header_horizontal)
        table.setHorizontalHeaderLabels(self.column_title)

        # hide Column 'id'
#        table.setColumnHidden(0, True)

        if self.row_title:
            table.setVerticalHeaderLabels(self.row_title)

        table.resizeColumnsToContents()
        table.setSortingEnabled(self.sorting)

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(self.table_left + self.table_width + 10, self.table_top)
        button_add.clicked.connect(lambda: self.action_add(self.tab_window, table))

        button_save = QPushButton(lng['save'], mytab)
        button_save.move(self.table_left + self.table_width + 10, self.table_top + table.height())
        button_save.clicked.connect(lambda: self.action_save(self.tab_window))

    def _define_column_title(self):
        return ()

    def action_add(self, root_window, table):
        # TODO: Give me something to do
        table.insertRow(table.rowCount())
        # add id Column also to have a reference to database id
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(str(table.rowCount())))
        table.setItem(table.rowCount() - 1, 1, QTableWidgetItem("blubber" + str(table.rowCount())))
        table.setItem(table.rowCount() - 1, 2, QTableWidgetItem("bla" + str(table.rowCount())))

    def action_save(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")


class ViewSchoolYear(ViewConfigure):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'],)


class ViewSchoolClass(ViewConfigure):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'],)


class ViewSubject(ViewConfigure):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'],)


class ViewExamsType(ViewConfigure):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'], self.lng['weight'])


class ViewTimeperiod(ViewConfigure):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'], self.lng['weight'])
