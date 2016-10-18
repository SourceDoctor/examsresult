from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QMessageBox, \
    QPushButton, QInputDialog, QAbstractItemView


class ViewDefine(object):
    # Fixme: if tab added, and before Tabview was empty, first one has no buttons

    lng = {}
    column_title = ()
    row_title = ()

    table_left = 0
    table_top = 0
    table_height = 200
    table_width = 200

    cell_editable = False
    full_row_select = True
    full_column_select = False

    sorting = True
    header_horizontal = True
    header_vertical = False

    def __init__(self, root_tab, lng):
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = ('id',) + self._define_column_title()

        mytab = QWidget()
        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)
        self.my_table.setHorizontalHeaderLabels(self.column_title)

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

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(self.table_left + self.table_width + 10, self.table_top)
        button_add.clicked.connect(self.action_add)

        button_save = QPushButton(lng['save'], mytab)
        button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        button_save.clicked.connect(lambda: self.action_save(self.tab_window))

    def _define_column_title(self):
        return ()

    def _action_add_content(self, table):
        # set Dummy Content
        data = ()
        column = 1
        while column <= len(self.column_title) - 1:
            cell_dummy_content = "%s_%s" % (self.column_title[column], str(self.my_table.rowCount()))
            data += (cell_dummy_content,)
            column += 1
        return data

    def _action_edit_content(self, table, content):
        data = ()
        return data

    def action_add(self):
        # fill Data into Cells
        data = self._action_add_content(self.my_table)
        if not data:
            return

        self.my_table.insertRow(self.my_table.rowCount())
        # add id Column also to have a reference to database id
        self.my_table.setItem(self.my_table.rowCount() - 1, 0, QTableWidgetItem(str(self.my_table.rowCount())))

        column = 1
        while column <= len(self.column_title) - 1:
            self.my_table.setItem(self.my_table.rowCount() - 1, column, QTableWidgetItem(str(data[column - 1])))
            column += 1

    def action_edit(self, cell):
        row = cell.row()
        content = ()

        column = 1
        while column <= len(self.column_title) - 1:
            content += (self.my_table.item(row, column).text(),)
            column += 1

        new_content = self._action_edit_content(self.my_table, content)
        if not new_content:
            self.my_table.selectRow(row)
            return

        column = 1
        while column <= len(self.column_title) - 1:
            new_value = new_content[column - 1]
            self.my_table.setItem(row, column, QTableWidgetItem(str(new_value)))
            column += 1

        self.my_table.selectRow(row)

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

    def _action_edit_content(self, table, content):
        data = ()

        edit_dialog = QInputDialog(parent=self.tab_window)

        name, ok = edit_dialog.getText(self.tab_window, self.lng['title'], self.lng['name'],text=content[0])
        if ok:
            weight, ok = edit_dialog.getDouble(self.tab_window, self.lng['title'], self.lng['weight'], decimals=2,value=float(content[1]))
        if ok:
            data += (name, weight)

        return data
