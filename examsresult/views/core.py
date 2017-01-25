from PyQt5.QtWidgets import QMessageBox, QInputDialog, QTableWidgetItem, QFileDialog

from examsresult.tools import export_csv, ExportPdf, cleanup_filename


class CoreView(object):

    changed_mark = "! "
    changed_mark_enabled = True
    is_changed = False

    lng = {}
    # {name, type, unique, editable}
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

    def set_filetypes(self, lng):
        filetype = []
        for desc in [(lng['filetype_exf'], '*.exf'), (lng['filetype_all'], '*')]:
            filetype.append("%s (%s)" % (desc[0], desc[1]))
        self.filetypes = ";;".join(filetype)

    def _define_column_title(self):
        return []

    def _set_changed(self, status):
        return True

    def set_changed(self, status):
        if not self._set_changed(status):
            return False

        # (un)mark tab title
        if self.changed_mark_enabled:
            index = 0
            while index <= self.tab_window.count():
                title = self.tab_window.tabText(index)
                if status:
                    search_title = "%s" % self.lng['title']
                    new_title = "%s%s" % (self.changed_mark, title)
                else:
                    search_title = "%s%s" % (self.changed_mark, self.lng['title'])
                    new_title = title.replace(self.changed_mark, '')

                if title == search_title:
                    break
                index += 1
            self.tab_window.setTabText(index, new_title)

        self.is_changed = status
        self.button_save.setEnabled(status)
        return True

    def unique_check(self, proof_data, edited_id=0):
        # search each Column which has to be unique if possible new_data is in it
        column = -1
        for col in self.column_title:
            column += 1
            if column == 0:
                # id Column will be ignored
                continue
            if not col['unique']:
                continue
            row = 0
            while row <= self.my_table.rowCount() - 1:
                if edited_id and \
                        self.my_table.item(row, 0).text() and \
                        (edited_id == int(self.my_table.item(row, 0).text())):
                    # don't check against myself (happens on editing Content)
                    pass
                elif proof_data[column - 1] == self.my_table.item(row, column).text():
                    return False
                row += 1
        return True

    def _action_add_content(self, root_window, content=(), limit_column=[]):
        data = ()

        add_dialog = QInputDialog(parent=root_window)
        content_index = 0

        for col in self.column_title:
            try:
                if col['editable'] == False:
                    continue
            except KeyError:
                pass

            try:
                cell_content = content[content_index]
            except IndexError:
                if col['type'] == 'int':
                    cell_content = 0
                elif col['type'] == 'float':
                    cell_content = 0
                elif col['type'] == 'string':
                    cell_content = ""
                elif col['type'] == 'list':
                    cell_content = []
                else:
                    cell_content = None

            content_index += 1
            if len(limit_column) and content_index not in limit_column:
                value = cell_content
            else:
                if col['type'] == 'int':
                    value, ok = add_dialog.getInt(root_window, self.lng['title'], col['name'], value=int(cell_content))
                elif col['type'] == 'float':
                    value, ok = add_dialog.getDouble(root_window, self.lng['title'], col['name'],
                                                     decimals=self.float_precision, value=float(cell_content))
                elif col['type'] == 'string':
                    value, ok = add_dialog.getText(root_window, self.lng['title'], col['name'], text=cell_content)
                elif col['type'] == 'list':
                    column_list = col['list']
                    column_list.sort()
                    if cell_content in column_list:
                        list_index = column_list.index(cell_content)
                    else:
                        list_index = 0
                    value, ok = add_dialog.getItem(root_window, self.lng['title'], col['name'], col['list'], list_index, False)
                else:
                    print("unknown Type: %s" % col[1])
                    return ()

                if not ok:
                    return ()

            data += (value,)

        return data

    def _action_edit_content(self, root_window, content, limit_column=[]):
        return self._action_add_content(root_window, content, limit_column)

    def _action_load_content(self):
        QMessageBox.information(self.tab_window, self.lng['title'], "Tell me how to load!")
        return []

    def _action_save_content(self, data):
        QMessageBox.information(self.tab_window, self.lng['title'], "Tell me how to save!")
        return False

    def action_add(self, data_import=False, with_id=False, data=()):
        # temporarly disable sorting
        sort_state = self.sorting
        self.sorting = False
        self.my_table.setSortingEnabled(False)

        # fill Data into Cells
        if not data_import:
            data = self._action_add_content(self.my_table)
        if data:
            if not self.unique_check(data):
                QMessageBox.warning(self.tab_window, self.lng['title'], self.lng['msg_double_error'])
            else:
                self.my_table.insertRow(self.my_table.rowCount())
                # add empty cell to id Column to have a reference to database
                self.my_table.setItem(self.my_table.rowCount() - 1, 0, QTableWidgetItem(''))

                column_title = []
                if with_id:
                    column = 0
                    column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
                else:
                    column = 1
                column_title.extend(self.column_title)
                data_row = 0
                while column <= len(column_title) - 1 and data_row <= len(data) - 1:
                    if with_id:
                        self.my_table.setItem(self.my_table.rowCount() - 1, column, QTableWidgetItem(str(data[column])))
                    else:
                        self.my_table.setItem(self.my_table.rowCount() - 1, column, QTableWidgetItem(str(data[column - 1])))
                    column += 1
                    data_row += 1
                self.set_changed(True)
        try:
            self.button_add.setFocus()
        except AttributeError:
            pass

        # restore sorting state
        self.sorting = sort_state
        self.my_table.setSortingEnabled(sort_state)

    def action_edit(self, cell=None, limit_column=[]):
        try:
            row = cell.row()
        except AttributeError:
            try:
                row = self.my_table.selectedIndexes()[0].row()
            except IndexError:
                row = 0

        content = ()

        # get Cell Content
        column = 1
        while column <= len(self.column_title) - 1:
            content += (self.my_table.item(row, column).text(),)
            column += 1

        new_content = self._action_edit_content(self.my_table, content, limit_column)
        if not new_content:
            self.my_table.selectRow(row)
            return

        if not self.unique_check(new_content, edited_id=row+1):
            QMessageBox.warning(self.tab_window, self.lng['title'], self.lng['msg_double_error'])
            return

        # write new Cell Content
        column = 1
        while column <= len(self.column_title) - 1:
            if not len(limit_column) or column in limit_column:
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

        if not self._action_save_content(data=data):
            return False

        self.load_data(1, 0)
        self.set_changed(False)

    def clear_table(self):
        while self.my_table.rowCount():
            self.my_table.removeRow(0)

    def load_data(self, sort_column=None, sort_order=0):
        # temporarly disable sorting
        sort_state = self.sorting
        self.sorting = False
        self.my_table.setSortingEnabled(False)

        # clear table
        self.clear_table()
        # load data from Database
        data_list = self._action_load_content()
        for data in data_list:
            self.my_table.insertRow(self.my_table.rowCount())
            column = 0
            while column <= len(self.column_title) - 1:
                self.my_table.setItem(self.my_table.rowCount() - 1, column, QTableWidgetItem(str(data[column])))
                column += 1

        # restore sorting state
        self.sorting = sort_state
        self.my_table.setSortingEnabled(sort_state)

        # sort Table
        if self.sorting and sort_column != None:
            self.my_table.sortItems(sort_column, sort_order)

    def file_save(self, parent, caption, default_filename, filetype=None):
        if filetype == 'csv':
            filetype = "CSV (*.csv)"
        elif filetype == 'pdf':
            filetype = "PDF (*.pdf)"
        else:
            filetype = ''

        default_filename = "%s_%s" % (self.lng['export_title'], default_filename)
        default_filename = cleanup_filename(default_filename)

        file_handler = QFileDialog()
        file_tuple = file_handler.getSaveFileName(parent, caption, default_filename, filetype)

        if not file_tuple[1]:
            return ''
        return file_tuple[0]

    def _collect_export_data(self, start_column=0):
        data = []
        rows = self.my_table.rowCount()
        columns = self.my_table.columnCount()
        r = 0
        while r <= rows - 1:
            c = start_column
            row = ()
            while c <= columns - 1:
                row += (self.my_table.item(r, c).text(),)
                c += 1
            r += 1
            data.append(row)
        return data

    def configure_export_csv(self, parent, default_filename):
        filename = self.file_save(parent=parent, caption=self.lng['title'], default_filename=default_filename, filetype='csv')
        if not filename:
            return

        data = self._collect_export_data(start_column=1)
        export_csv(target_file=filename, data=data)

    def do_pdf_export(self, default_filename, root=None):
        if not root:
            root = self.tab_window
        filename = self.file_save(root, self.lng['title'], default_filename=default_filename, filetype='pdf')
        if not filename:
            return

        data = self._collect_export_data(start_column=0)
        pdf = ExportPdf(target_file=filename, template=self.pdf_template, data=data, head_text=self.pdf_head_text, foot_text=self.pdf_foot_text)
        pdf.save()

    def pdf_template(self, obj, data):
        obj.drawString(100, 750, "Empty Template")

    @property
    def pdf_head_text(self):
        return "empty Head"

    @property
    def pdf_foot_text(self):
        return "empty Foot"
