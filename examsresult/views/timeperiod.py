from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QMessageBox, QPushButton


class ViewTimeperiod(object):

    def __init__(self, root_tab, lng):
        self.tab_window = root_tab
        # Todo: check after Change if Cell is empty, then Error !
        mytab = QWidget()
        table = QTableWidget(mytab)
        self.tab_window.addTab(mytab, lng['title'])

        table_left = 100
        table_top = 70

        table.move(table_left, table_top)

        table.setRowCount(4)
        table.setColumnCount(2)

        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels((lng['description'], lng['weight']))

        table.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        table.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
        table.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
        table.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
        table.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
        table.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
        table.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
        table.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))

        table.resizeColumnsToContents()
        table.setSortingEnabled(True)

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(500, table_top)
        button_add.clicked.connect(lambda: self.action_add(self.tab_window, table))

        button_save = QPushButton(lng['save'], mytab)
        button_save.move(500, table_top + table.height())
        button_save.clicked.connect(lambda: self.action_save(self.tab_window))

    def action_add(self, root_window, table):
        # TODO: Give me something to do
        table.insertRow(table.rowCount())
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem("blubber" + str(table.rowCount())))
        table.setItem(table.rowCount() - 1, 1, QTableWidgetItem("bla" + str(table.rowCount())))

    def action_save(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")
