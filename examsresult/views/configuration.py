from PyQt5.QtWidgets import QWidget, QTableWidget
from examsresult.views import CoreView


class ViewSchoolClassConfigure(CoreView):

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

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

    def _define_column_title(self):
        return []
