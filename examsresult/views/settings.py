from PyQt5.QtWidgets import QDialog, QPushButton


class ViewSettings(object):

    def __init__(self, parent, lng, width=400, height=200):
        self.lng = lng
        local_lng = lng['window_settings']

        window = QDialog(parent=parent)
        window.setFixedHeight(height)
        window.setFixedWidth(width)
        window.setWindowTitle(local_lng['title'])

        button = QPushButton(self.lng['main']['ok'], window)
        button.move(300, 170)
        button.clicked.connect(window.close)

        window.exec_()
