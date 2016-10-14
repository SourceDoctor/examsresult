import sys
from PyQt5.QtWidgets import QApplication

from examsresult.view import View


def run():
    qapp = QApplication(sys.argv)
    gui = View(qapp=qapp)
    gui.main_window()
    sys.exit(qapp.exec_())

if __name__ == '__main__':
    run()
