from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QMessageBox, \
    QPushButton, QInputDialog, QAbstractItemView


class ViewDefine(object):
    # Fixme: if tab added, and before Tabview was empty, first one has no buttons

    lng = {}
    # (column_name, column_type, column_default_value, column_editable)
    column_title = []
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
    float_precision = 2

    def __init__(self, dbhandler, root_tab, lng):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = []
        self.column_title.append(('id', 'int', '', False))
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
            column_tuple += (col[0],)
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

        self.set_changed(False)
        self.button_add.setFocus()

    def _define_column_title(self):
        return []

    def _action_add_content(self, root_window, content=()):
        data = ()

        add_dialog = QInputDialog(parent=root_window)
        content_index = 0

        for col in self.column_title:
            try:
                if col[3] == False:
                    continue
            except IndexError:
                pass

            try:
                cell_content = content[content_index]
            except IndexError:
                if col[1] == 'int':
                    cell_content = 0
                elif col[1] == 'float':
                    cell_content = 0
                elif col[1] == 'string':
                    cell_content = ""
                elif col[1] == 'list':
                    cell_content = []
                else:
                    cell_content = None

            content_index += 1

            if col[1] == 'int':
                value, ok = add_dialog.getInt(root_window, self.lng['title'], col[0], value=int(cell_content))
            elif col[1] == 'float':
                value, ok = add_dialog.getDouble(root_window, self.lng['title'], col[0], decimals=self.float_precision, value=float(cell_content))
            elif col[1] == 'string':
                value, ok = add_dialog.getText(root_window, self.lng['title'], col[0], text=cell_content)
            elif col[1] == 'list':
                value, ok = add_dialog.getItem(root_window, self.lng['title'], col[0], Iterable=cell_content)
            else:
                print("unknown Type: %s" % col[1])
                return ()

            if not ok:
                return ()

            data += (value,)

        return data

    def _action_edit_content(self, root_window, content):
        return self._action_add_content(root_window, content)

    def _action_save_content(self, data):
        QMessageBox.information(self.tab_window, self.lng['title'], "Tell me how to save!")
        return 0

    def action_add(self):
        # fill Data into Cells
        data = self._action_add_content(self.my_table)
        if data:
            self.my_table.insertRow(self.my_table.rowCount())
            # add empty cell to id Column to have a reference to database
            self.my_table.setItem(self.my_table.rowCount() - 1, 0, QTableWidgetItem(''))

            column = 1
            while column <= len(self.column_title) - 1:
                self.my_table.setItem(self.my_table.rowCount() - 1, column, QTableWidgetItem(str(data[column - 1])))
                column += 1
            self.set_changed(True)

        self.button_add.setFocus()

    def action_edit(self, cell):
        row = cell.row()
        content = ()

        # get Cell Content
        column = 1
        while column <= len(self.column_title) - 1:
            content += (self.my_table.item(row, column).text(),)
            column += 1

        new_content = self._action_edit_content(self.my_table, content)
        if not new_content:
            self.my_table.selectRow(row)
            return

        # write new Cell Content
        column = 1
        while column <= len(self.column_title) - 1:
            new_value = new_content[column - 1]
            self.my_table.setItem(row, column, QTableWidgetItem(str(new_value)))
            column += 1

        self.my_table.selectRow(row)
        self.set_changed(True)

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
        self.set_changed(False)

    def set_changed(self, status):

        self.button_save.setEnabled(status)

        # (un)mark tab title
        changed_mark = "! "
        index = 0
        while index <= self.tab_window.count():
            title = self.tab_window.tabText(index)
            if status:
                search_title = "%s" % self.lng['title']
                new_title = "%s%s" % (changed_mark, title)
            else:
                search_title = "%s%s" % (changed_mark, self.lng['title'])
                new_title = title.replace(changed_mark, '')

            if title == search_title:
                break
            index += 1

        self.tab_window.setTabText(index, new_title)


class ViewSchoolYear(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', '')]

    def _action_save_content(self, data):
        ret = self.dbh.set_schoolyear(data=data)
        return ret

class ViewSchoolClass(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', '')]

    def _action_save_content(self, data):
        ret = self.dbh.set_schoolclassname(data=data)
        return ret

class ViewSubject(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', '')]

    def _action_save_content(self, data):
        ret = self.dbh.set_subject(data=data)
        return ret

class ViewExamsType(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', ''),
                (self.lng['weight'], 'float', '')]

    def _action_save_content(self, data):
        ret = self.dbh.set_examtype(data=data)
        return ret


class ViewTimeperiod(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', ''),
                (self.lng['weight'], 'float', '')]

    def _action_save_content(self, data):
        ret = self.dbh.set_timeperiod(data=data)
        return ret
