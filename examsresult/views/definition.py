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

    def __init__(self, root_tab, lng):
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

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(self.table_left + self.table_width + 10, self.table_top)
        button_add.clicked.connect(self.action_add)

        button_save = QPushButton(lng['save'], mytab)
        button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        button_save.clicked.connect(lambda: self.action_save(self.tab_window))

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

    def action_save(self, root_window):
        QMessageBox.information(root_window, self.lng['title'], "Give me something to do!")


class ViewSchoolYear(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', '')]


class ViewSchoolClass(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', '')]


class ViewSubject(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', '')]


class ViewExamsType(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', ''),
                (self.lng['weight'], 'float', '')]


class ViewTimeperiod(ViewDefine):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def _define_column_title(self):
        return [(self.lng['name'], 'string', ''),
                (self.lng['weight'], 'float', '')]
