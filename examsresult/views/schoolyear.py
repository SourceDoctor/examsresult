from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QMessageBox, QPushButton


class ViewSchoolYear(object):

    def __init__(self, root_tab, lng):
        self.tab_window = root_tab
        mytab = QWidget()

        self.tab_window.addTab(mytab, lng['title'])

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(50, 70)
        button_add.clicked.connect(lambda: self.action_add(self.tab_window))
        button_edit = QPushButton(lng['edit'], mytab)
        button_edit.move(50, 90)
        button_edit.clicked.connect(lambda: self.action_edit(self.tab_window))


    def action_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")


    def action_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")
