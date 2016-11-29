from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from ..tools import app_icon


class ViewAbout(object):

    def __init__(self, parent, lng, width=400, height=150):
        self.lng = lng
        local_lng = lng['window_about']

        window = QDialog(parent=parent)
        window.setFixedHeight(height)
        window.setFixedWidth(width)
        window.setWindowTitle(local_lng['title'])

        app_icon_label = QLabel(window)
        pixmap = QPixmap(app_icon)
        # Todo: Zoom Icon
#         pixmap.scaledToWidth(30)
#         pixmap.scaledToHeight(30)
        app_icon_label.setPixmap(pixmap)
        app_icon_label.move(10, 10)

        version = "%s %s" % (local_lng['version'], "1.0")

        title_label = QLabel(self.lng['main']['title'], window)
        title_label.move(50, 10)
        info_label = QLabel(version, window)
        info_label.move(50, 30)
        info_label = QLabel(local_lng['infotext'], window)
        info_label.move(50, 50)
        info_label = QLabel("created by Thomas Berberich", window)
        info_label.move(50, 70)
        button = QPushButton(self.lng['main']['ok'], window)
        button.move(300, 120)
        button.clicked.connect(window.close)

        window.exec_()
