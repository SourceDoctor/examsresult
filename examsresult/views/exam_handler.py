from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QTableWidget, \
    QAbstractItemView, QTextEdit, QCalendarWidget, QGroupBox

from examsresult.configuration import current_config, save_config
from examsresult.tools import lng_list
from examsresult.views.core import CoreView


class Exam(CoreView):

    changed_mark_enabled = False

    width = 500
    height = 500
    table_left = 50
    table_top = 110
    table_height = 320
    table_width = 400

    examresult = []

    def __init__(self, dbhandler, parent, lng):
        self.dbhandler = dbhandler
        self.lng = lng
        self.column_title = []
        self.column_title.append({'name': 'id', 'type': 'int', 'unique': True, 'editable': False})
        self.column_title.extend(self._define_column_title())

        self.language_list = lng_list()
        config = current_config

        self.window = QDialog(parent=parent)
        self.window.setFixedHeight(self.height)
        self.window.setFixedWidth(self.width)
        self.window.setWindowTitle(self.lng['title_result'])

        label_exam_description = QLabel(self.window)
        label_exam_description.setText(self.lng['exam_description'])
        label_exam_description.move(self.table_left, 50)
        self.text_exam_description = QTextEdit(self.window)
        self.text_exam_description.setGeometry(self.table_left + 100, 52, 300, 40)

        label_students = QLabel(self.window)
        label_students.setText(self.lng['students'])
        label_students.move(self.table_left, self.table_top - 20)

        self.my_table = QTableWidget(self.window)

        self.my_table.setGeometry(self.table_left, self.table_top, self.table_width, self.table_height)

        self.my_table.setColumnCount(len(self.column_title))

        column_tuple = ()
        for col in self.column_title:
            column_tuple += (col['name'],)
        self.my_table.setHorizontalHeaderLabels(column_tuple)

        self.my_table.verticalHeader().setVisible(self.header_vertical)
        self.my_table.horizontalHeader().setVisible(self.header_horizontal)

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



        self.button_save = QPushButton(self.lng['save'], self.window)
        self.button_save.move(self.table_left + self.table_width - self.button_save.width(), self.table_top + self.table_height)
#        self.button_save.clicked.connect(self.save_settings)

        button_cancel = QPushButton(self.lng['close'], self.window)
        button_cancel.move(370, 470)
        button_cancel.clicked.connect(self.window.close)

        self.cal = QCalendarWidget(self.window)
        self.cal.setGridVisible(True)
        self.cal.move(self.table_left + 100, 30)
        self.cal.clicked.connect(self.set_date)
        self.cal.setVisible(False)

        label_exam_date = QLabel(self.window)
        label_exam_date.setText(self.lng['exam_date'])
        label_exam_date.move(self.table_left, 30)

#        cal.clicked[QDate].connect(cal.showDate)

        date = self.cal.selectedDate()
        self.exam_date = QLabel(self.window)
        self.exam_date.setText(date.toString())
#        self.exam_date.move(self.table_left + 100, 30)
        self.exam_date.setGeometry(self.table_left + 100, 22, 100, self.exam_date.height())

        self.button_set_date = QPushButton(self.lng['set_date'], self.window)
        self.button_set_date.move(self.table_left + 240, 25)
        self.button_set_date.clicked.connect(self.set_date)

        self.set_changed(False)
        self.window.exec_()

    def _define_column_title(self):
        return [{'name': self.lng['lastname'], 'type': 'string', 'unique': False},
                {'name': self.lng['firstname'], 'type': 'string', 'unique': False},
                {'name': self.lng['result'], 'type': 'float', 'unique': False},
                {'name': self.lng['comment'], 'type': 'string', 'unique': False}
                ]

    def set_date(self):
        self.cal.setVisible(not self.cal.isVisible())
        self.button_set_date.setVisible(not self.button_set_date.isVisible())
        self.exam_date.setVisible(not self.exam_date.isVisible())
        date = self.cal.selectedDate()
        self.exam_date.setText(date.toString())
