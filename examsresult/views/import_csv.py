from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QFileDialog, \
    QGroupBox, QRadioButton, QLineEdit, QMessageBox

from examsresult.views.core import CoreView
import csv


class CSVImport(CoreView):

    changed_mark_enabled = False
    students = []

    def __init__(self, parent, lng, width=400, height=420):
        self.lng = lng

        self.window = QDialog(parent=parent)
        self.window.setFixedHeight(height)
        self.window.setFixedWidth(width)
        self.window.setWindowTitle(self.lng['csv_import_title'])

        self.radio_csv_with_header = QRadioButton(self.window)
        self.radio_csv_with_header.setText(self.lng['csv_with_header'])
        self.radio_csv_with_header.move(10, 20)
        column_group = QGroupBox(self.window)
        column_group.setGeometry(20, 20, self.window.width() - 20 - 20, 100)

        label_lastname = QLabel(self.lng['lastname'], column_group)
        label_lastname.move(10, 30)
        self.text_lastname = QLineEdit(column_group)
        self.text_lastname.setGeometry(100, 27, 100, 20)
        self.text_lastname.setText("lastname")
        label_firstname = QLabel(self.lng['firstname'], column_group)
        label_firstname.move(10, 50)
        self.text_firstname = QLineEdit(column_group)
        self.text_firstname.setGeometry(100, 47, 100, 20)
        self.text_firstname.setText("firstname")
        label_comment = QLabel(self.lng['comment'], column_group)
        label_comment.move(10, 70)
        self.text_comment = QLineEdit(column_group)
        self.text_comment.setGeometry(100, 67, 100, 20)
        self.text_comment.setText("comment")

        self.radio_csv_simple = QRadioButton(self.window)
        self.radio_csv_simple.setText(self.lng['csv_simple'])
        self.radio_csv_simple.move(10, 130)
        simple_group = QGroupBox(self.window)
        simple_group.setGeometry(20, 130, self.window.width() - 20 - 20, 120)

        label_delimiter = QLabel(self.lng['delimiter'], simple_group)
        label_delimiter.move(10, 30)
        self.text_delimiter = QLineEdit(simple_group)
        self.text_delimiter.setGeometry(100, 27, 15, 20)
        self.text_delimiter.setMaxLength(1)
        self.text_delimiter.setText(";")
        label_lastname = QLabel(self.lng['column_lastname'], simple_group)
        label_lastname.move(10, 50)
        self.int_lastname = QLineEdit(simple_group)
        self.int_lastname.setGeometry(240, 47, 50, 20)
        self.int_lastname.setText("1")
        label_firstname = QLabel(self.lng['column_firstname'], simple_group)
        label_firstname.move(10, 70)
        self.int_firstname = QLineEdit(simple_group)
        self.int_firstname.setGeometry(240, 67, 50, 20)
        self.int_firstname.setText("2")
        label_comment = QLabel(self.lng['column_comment'], simple_group)
        label_comment.move(10, 90)
        self.int_comment = QLineEdit(simple_group)
        self.int_comment.setGeometry(240, 87, 50, 20)
        self.int_comment.setText("3")

        csv_file_group = QGroupBox(self.window)
        csv_file_group.setTitle("CSV File")
        csv_file_group.setGeometry(20, 300, self.window.width() - 20 - 20, 80)
        self.label_csv_file = QLabel("", csv_file_group)
        self.label_csv_file.setGeometry(10, 20, csv_file_group.width() - 10, self.label_csv_file.height())
        
        button_csv_file = QPushButton(self.lng['csv_file'], csv_file_group)
        button_csv_file.move(250, 50)
        button_csv_file.clicked.connect(self.csv_openfile)

        self.button_import = QPushButton(self.lng['import'], self.window)
        self.button_import.move(210, 390)
        self.button_import.clicked.connect(self.csv_import)

        button_cancel = QPushButton(self.lng['cancel'], self.window)
        button_cancel.move(300, 390)
        button_cancel.clicked.connect(self.window.close)

        self.radio_csv_with_header.setChecked(True)
        self.button_import.setEnabled(False)
        self.window.exec_()

    def csv_import(self):
        students = []
        column_list = [
            self.text_lastname.text(),
            self.text_firstname.text(),
            self.text_comment.text()
        ]
        csv_file = self.label_csv_file.text()

        if self.radio_csv_with_header.isChecked():
            with open(csv_file) as csvfile:
                reader = csv.DictReader(csvfile)
                try:
                    for row in reader:
                        d = ()
                        column = 0
                        while column <= len(column_list) - 1:
                            d += (row[column_list[column]],)
                            column += 1
                        students.append(d)
                except KeyError:
                    QMessageBox.critical(self.window, self.lng['title'], self.lng['msg_column_key_failure'])
                    return

        elif self.radio_csv_simple.isChecked():
            with open(csv_file, 'r') as csvfile:
                csv_content = csv.reader(csvfile, delimiter=self.text_delimiter.text())
                try:
                    for row in csv_content:
                        d = ()
                        d += (row[int(self.int_lastname.text()) - 1],)
                        d += (row[int(self.int_firstname.text()) - 1],)
                        d += (row[int(self.int_comment.text()) - 1],)
                        students.append(d)
                except IndexError:
                    QMessageBox.critical(self.window, self.lng['title'], self.lng['msg_column_number_failure'])
                    return
        else:
            print("unknown CSV Type to import")

        self.students = students
        self.window.close()

    def csv_openfile(self):
        lng = self.lng
        file_handler = QFileDialog()
        file_tuple = file_handler.getOpenFileName(parent=self.window, caption=lng['title'], filter="CSV (*.csv)")
        csv_file = file_tuple[0]

        if not csv_file:
            return
        self.label_csv_file.setText(csv_file)
        self.button_import.setEnabled(True)

