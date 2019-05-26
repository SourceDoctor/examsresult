from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from examsresult.tools import app_icon, repository_version


class ViewAbout(object):

    def __init__(self, dbhandler, parent, lng, width=400, height=150):
        self.dbh = dbhandler

        self.lng = lng
        local_lng = lng['window_about']

        window = QDialog(parent=parent)
        window.setFixedHeight(height)
        window.setFixedWidth(width)
        window.setWindowTitle(local_lng['title'])

        app_icon_label = QLabel(window)
        pixmap = QPixmap(app_icon)
        pixmap = pixmap.scaled(60, 60)
        app_icon_label.setPixmap(pixmap)
        app_icon_label.move(7, 7)

        system_version = self.dbh.system_version
        version = "%s %s" % (local_lng['version'], system_version.replace('v', ''))

        title_label = QLabel(self.lng['main']['title'], window)
        title_label.move(80, 10)
        info_label = QLabel(version, window)
        info_label.move(80, 30)
        info_label = QLabel(local_lng['infotext'], window)
        info_label.move(80, 50)
        info_label = QLabel("created by Thomas Berberich", window)
        info_label.move(80, 70)
        supportmail = "program.examsresult@gmail.com"
        info_label = QLabel("E-Mail: <a href=\"mailto:" + supportmail + "?Subject=Support\" target=\"_top\">" + supportmail + "</a>", window)
        info_label.setOpenExternalLinks(True)
        info_label.move(80, 90)
        version_information_label = QLabel(self.version_information, window)
        version_information_label.move(10, 120)
        button = QPushButton(self.lng['main']['ok'], window)
        button.move(300, 120)
        button.clicked.connect(window.close)

        window.exec_()

    @property
    def version_information(self):
        local_lng = self.lng['window_about']

        running_version = self.dbh.system_version
        repo_version = repository_version()

        if not repo_version:
            ret = local_lng['remote_check_failed']
        elif running_version < repo_version:
            ret = local_lng['system_update_available']
        elif running_version == repo_version:
            ret = local_lng['system_uptodate']
        elif running_version > repo_version:
            ret = local_lng['system_newer_than_repository']
        else:
            ret = local_lng['unknown_version_check_error']

        return ret
