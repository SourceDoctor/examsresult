from PyQt5.QtWidgets import QWidget, QTableWidget

from examsresult.views import CoreView


class ViewReport(CoreView):

    table_left = 100
    table_top = 130
    table_height = 350
    table_width = 500


class ViewReportStudent(ViewReport):

    def __init__(self, dbhandler, root_tab, lng, data):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng

        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()

        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])

class ViewReportSchoolclass(ViewReport):

    def __init__(self, dbhandler, root_tab, lng, data):
        self.dbh = dbhandler
        self.tab_window = root_tab
        self.lng = lng

        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        mytab = QWidget()

        self.my_table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, self.lng['title'])