from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QMessageBox, QPushButton, QInputDialog


class ViewDefine(object):
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

    def _action_add_content(self, table):
        # set Dummy Content
        data = ()
        column = 1
        while column <= len(self.column_title) - 1:
            cell_dummy_content = "%s_%s" % (self.column_title[column], str(table.rowCount()))
            data += (cell_dummy_content,)
            column += 1
        return data

    def action_add(self, root_window, table):

        data = self._action_add_content(table)
        if not data:
            return

        table.insertRow(table.rowCount())
        # add id Column also to have a reference to database id
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(str(table.rowCount())))

        column = 1
        while column <= len(self.column_title) - 1:
            table.setItem(table.rowCount() - 1, column, QTableWidgetItem(str(data[column - 1])))
            column += 1

    def action_save(self, root_window):
        QMessageBox.information(root_window, self.lng['title'], "Give me something to do!")


class ViewSchoolYear(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'],)

    def _action_add_content(self, table):
        data = ()

        add_dialog = QInputDialog(parent=self.tab_window)

        name, ok = add_dialog.getText(self.tab_window, self.lng['title'], self.lng['name'])
        if not ok:
            return data

        data += (name,)

        return data


class ViewSchoolClass(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'],)

    def _action_add_content(self, table):
        data = ()

        add_dialog = QInputDialog(parent=self.tab_window)

        name, ok = add_dialog.getText(self.tab_window, self.lng['title'], self.lng['name'])
        if not ok:
            return data

        data += (name,)

        return data


class ViewSubject(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'],)

    def _action_add_content(self, table):
        data = ()

        add_dialog = QInputDialog(parent=self.tab_window)

        name, ok = add_dialog.getText(self.tab_window, self.lng['title'], self.lng['name'])
        if not ok:
            return data

        data += (name,)

        return data


class ViewExamsType(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'], self.lng['weight'])

    def _action_add_content(self, table):
        data = ()

        add_dialog = QInputDialog(parent=self.tab_window)

        name, ok = add_dialog.getText(self.tab_window, self.lng['title'], self.lng['name'])
        if ok:
            weight, ok = add_dialog.getDouble(self.tab_window, self.lng['title'], self.lng['weight'], decimals=2)
        if not ok:
            return data

        data += (name, weight)

        return data


class ViewTimeperiod(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return (self.lng['name'], self.lng['weight'])

    def _action_add_content(self, table):
        data = ()

        add_dialog = QInputDialog(parent=self.tab_window)

        name, ok = add_dialog.getText(self.tab_window, self.lng['title'], self.lng['name'])
        if ok:
            weight, ok = add_dialog.getDouble(self.tab_window, self.lng['title'], self.lng['weight'], decimals=2)
        if not ok:
            return data

        data += (name, weight)

        return data
