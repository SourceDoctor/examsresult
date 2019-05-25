from PyQt5.QtWidgets import QTableWidget, QWidget, QPushButton, QAbstractItemView, QLabel

from examsresult.models import DB_ID_INDEX
from examsresult.tools import HIDE_ID_COLUMN
from . import CoreView


class ViewDefine(CoreView):

    table_left = 100
    table_top = 30
    table_height = 350
    table_width = 200

    def __init__(self, dbhandler, root_tab, lng):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng
        self.column_title = []
        self.column_title.append({'name': 'id',
                                  'type': 'int',
                                  'unique': True,
                                  'editable': False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()
        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)
        self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
            if 'hide' in col.keys():
                self.my_table.setColumnHidden(self.column_title.index(col), col['hide'])
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        # hide Column 'id'
        self.my_table.setColumnHidden(DB_ID_INDEX, HIDE_ID_COLUMN)

        if self.row_title:
            self.my_table.setVerticalHeaderLabels(self.row_title)

        if self.full_row_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        if self.full_column_select:
            self.my_table.setSelectionBehavior(QAbstractItemView.SelectColumns)

        if self.cell_editable:
            self.my_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.my_table.resizeColumnsToContents()
        self.my_table.setSortingEnabled(self.sorting)

        self.my_table.doubleClicked.connect(self.action_edit)

        self.button_add = QPushButton(lng['add'], mytab)
        self.button_add.move(self.table_left + self.table_width + 10, self.table_top)
        self.button_add.clicked.connect(self.action_add)

        self.button_edit = QPushButton(lng['edit'], mytab)
        self.button_edit.move(self.table_left + self.table_width + 10, self.table_top + self.button_add.height())
        self.button_edit.clicked.connect(self.action_edit)

        self.button_save = QPushButton(lng['save'], mytab)
        self.button_save.move(self.table_left + self.table_width + 10, self.table_top + self.my_table.height())
        self.button_save.clicked.connect(lambda: self.action_save(self.tab_window))

        # inject Newlines in Descriptiontext
        max_length = 40
        lbl_txt_list = []
        tmp_txt = ""
        for t in str(lng['description']).split(' '):
            if not tmp_txt:
                tmp_txt = t
                continue
            elif len(tmp_txt + ' ' + t) >= max_length:
                lbl_txt_list.append(tmp_txt)
                tmp_txt = t
                continue
            tmp_txt += ' ' + t
        lbl_txt_list.append(tmp_txt)

        lbl_description = QLabel('', mytab)
        lbl_description.setText('\n'.join(lbl_txt_list))
        lbl_description.setGeometry(450, self.table_top, 250, 100)

        # load Content from Database
        self.load_data(1, 0)

        self.set_changed(False)
        self.button_add.setFocus()


class ViewSchoolYear(ViewDefine):

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True}]

    def _action_save_content(self, data):
        self.dbh.set_schoolyear(data=data)
        return True

    def _action_load_content(self):
        return self.dbh.get_schoolyear()


class ViewSchoolClass(ViewDefine):

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True}]

    def _action_save_content(self, data):
        self.dbh.set_schoolclassname(data=data)
        return True

    def _action_load_content(self):
        return self.dbh.get_schoolclassname()


class ViewSubject(ViewDefine):

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True}]

    def _action_save_content(self, data):
        self.dbh.set_subject(data=data)
        return True

    def _action_load_content(self):
        return self.dbh.get_subject()


class ViewExamsType(ViewDefine):

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True},
                {'name': self.lng['weight'], 'type': 'float', 'unique': False}
                ]

    def _action_save_content(self, data):
        self.dbh.set_examtype(data=data)
        return True

    def _action_load_content(self):
        return self.dbh.get_examtype()


class ViewTimeperiod(ViewDefine):

    def _define_column_title(self):
        return [{'name': self.lng['name'], 'type': 'string', 'unique': True},
                {'name': self.lng['weight'], 'type': 'float', 'unique': False}
                ]

    def _action_save_content(self, data):
        self.dbh.set_timeperiod(data=data)
        return True

    def _action_load_content(self):
        return self.dbh.get_timeperiod()
