import sys
from PyQt5.QtWidgets import QApplication

from examsresult.configuration import init_config
from examsresult.views import BaseView


def run():

    config = init_config()

    qapp = QApplication(sys.argv)
    gui = BaseView(qapp=qapp, config=config)
    gui.main_window()
    sys.exit(qapp.exec_())

if __name__ == '__main__':
    run()
