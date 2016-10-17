from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, \
    QDialog, QPushButton, QLabel, QTabWidget
from examsresult.controls.dbhandler import DatabaseConnector
from examsresult.tools import lng_load, center_pos, app_icon
from .definition import ViewTimeperiod, ViewExamsType, ViewSchoolClass, ViewSchoolYear, ViewSubject


class BaseView(QMainWindow):

    database_file = None
    db_loaded = False
    dbc = None
    open_tabs = []

    def __init__(self, qapp, language='english'):
        super().__init__()
        self.qapp = qapp
        self.lng = lng_load(language=language)
        lng = self.lng['filetypes']

        filetype = []
        for desc in [(lng['filetype_exf'], '*.exf'), (lng['filetype_all'], '*')]:
            filetype.append("%s (%s)" % (desc[0], desc[1]))
        self.filetypes = ";;".join(filetype)

    def connect_db(self):
        if self.database_file:
            self.dbc = DatabaseConnector(self.database_file)

        if not self.dbc:
            self.db_loaded = False
            QMessageBox.warning(self, "", self.lng['window_openfile']['msg_open_err'] % self.database_file)
        else:
            self.db_loaded = True
            old_db_version, db_version = self.dbc.db_updater()
            if old_db_version and old_db_version < db_version:
                QMessageBox.information(self, "", self.lng['window_openfile']['msg_db_updated'])
            elif old_db_version > db_version:
                self.db_loaded = False
                QMessageBox.warning(self, "", self.lng['window_openfile']['msg_db_to_new'])

        if self.db_loaded:
            self.setWindowTitle("%s - %s" % (self.lng['main']['title'], self.database_file))
        else:
            self.setWindowTitle(self.lng['main']['title'])
            self.database_file = None

        self.toggle_menu(self.db_loaded)

    def toggle_menu(self, db_state):
        # Enable/Disable Menu Entries
        self.schoolyear_action.setEnabled(db_state)
        self.schoolclass_action.setEnabled(db_state)
        self.subject_action.setEnabled(db_state)
        self.examstype_action.setEnabled(db_state)
        self.timeperiod_action.setEnabled(db_state)

    def action_app_close(self):
        self.close()

    def _filedialog_handler(self, dialog_type):
        file_handler = QFileDialog()
        if dialog_type == 'new':
            lng = self.lng['window_newfile']
            # TODO: add per default File Extension
            file_tuple = file_handler.getSaveFileName(parent=self, caption=lng['title'], filter=self.filetypes)
        elif dialog_type == 'open':
            lng = self.lng['window_openfile']
            file_tuple = file_handler.getOpenFileName(parent=self, caption=lng['title'], filter=self.filetypes)
        else:
            print("CRITICAL, unknown filedialog type to handle")
            return

        database_file = file_tuple[0]

        if not database_file:
            return
        if database_file == self.database_file:
            return

        # close all opened tabs
        while self.open_tabs:
            self.close_tab_handler(0)

        self.database_file = database_file
        self.connect_db()

    def window_newfile(self):
        self._filedialog_handler('new')

    def window_openfile(self):
        self._filedialog_handler('open')

    def window_schoolyear(self, lng):
        ViewSchoolYear(self.tab_window, lng)

    def window_schoolclass(self, lng):
        ViewSchoolClass(self.tab_window, lng)

    def window_subject(self, lng):
        ViewSubject(self.tab_window, lng)

    def window_examstype(self, lng):
        ViewExamsType(self.tab_window, lng)

    def window_timeperiod(self, lng):
        ViewTimeperiod(self.tab_window, lng)

    def window_about(self, parent, width=400, height=100):
        lng = self.lng['window_about']

        window = QDialog(parent=parent)
        window.setFixedHeight(height)
        window.setFixedWidth(width)
        window.setWindowTitle(lng['title'])

        app_icon_label = QLabel(window)
        pixmap = QPixmap(app_icon)
        # Todo: Zoom Icon
#         pixmap.scaledToWidth(30)
#         pixmap.scaledToHeight(30)
        app_icon_label.setPixmap(pixmap)
        app_icon_label.move(10, 10)

        title_label = QLabel(self.lng['main']['title'], window)
        title_label.move(50, 10)
        info_label = QLabel(lng['infotext'], window)
        info_label.move(50, 30)
        button = QPushButton(self.lng['main']['ok'], window)
        button.move(300, 70)
        button.clicked.connect(window.close)

        window.exec_()

    def closeEvent(self, event):
        self.action_app_close()

    def close_tab_handler(self, index):
        title = self.tab_window.tabText(index)
        self.open_tabs.remove(title)
        self.tab_window.removeTab(index)

    def add_tab_event(self, tab_window_to_open, lng):
        # add Tab only if not still open
        if lng['title'] not in self.open_tabs:
            tab_window_to_open(lng)
            self.open_tabs.append(lng['title'])

        # set focus to requested Tab
        index = 0
        while index <= len(self.open_tabs) - 1:
            title = self.tab_window.tabText(index)
            if title == lng['title']:
                break
            index += 1
        self.tab_window.setCurrentIndex(index)

    def main_menu(self):
        mainMenu = self.menuBar()
        menutext = self.lng['menu']

        # File menu actions
        self.new_action = QAction(menutext['newfile'], self)
        self.new_action.triggered.connect(self.window_newfile)
        self.open_action = QAction(menutext['openfile'], self)
        self.open_action.triggered.connect(self.window_openfile)
        self.exit_action = QAction(menutext['quit'], self)
        self.exit_action.triggered.connect(self.action_app_close)
        # configure menu actions
        self.schoolyear_action = QAction(menutext['schoolyear'], self)
        self.schoolyear_action.triggered.connect(lambda: self.add_tab_event(self.window_schoolyear, self.lng['window_schoolyear']))
        self.schoolclass_action = QAction(menutext['schoolclass'], self)
        self.schoolclass_action.triggered.connect(lambda: self.add_tab_event(self.window_schoolclass, self.lng['window_schoolclass']))
        self.subject_action = QAction(menutext['subject'], self)
        self.subject_action.triggered.connect(lambda: self.add_tab_event(self.window_subject, self.lng['window_subject']))
        self.examstype_action = QAction(menutext['examstype'], self)
        self.examstype_action.triggered.connect(lambda: self.add_tab_event(self.window_examstype, self.lng['window_examstype']))
        self.timeperiod_action = QAction(menutext['timeperiod'], self)
        self.timeperiod_action.triggered.connect(lambda: self.add_tab_event(self.window_timeperiod, self.lng['window_timeperiod']))
        # Help menu actions
        self.about_action = QAction(menutext['about'], self)
        self.about_action.triggered.connect(lambda: self.window_about(self))

        # construct menu
        filemenu = mainMenu.addMenu(menutext['mainmenufile'])
        filemenu.addAction(self.new_action)
        filemenu.addAction(self.open_action)
        filemenu.addSeparator()
        filemenu.addAction(self.exit_action)

        definitionmenu = mainMenu.addMenu(menutext['mainmenudefinition'])
        definitionmenu.addAction(self.schoolyear_action)
        definitionmenu.addAction(self.schoolclass_action)
        definitionmenu.addAction(self.subject_action)
        definitionmenu.addAction(self.examstype_action)
        definitionmenu.addAction(self.timeperiod_action)

        helpmenu = mainMenu.addMenu(menutext['mainmenuhelp'])
        helpmenu.addAction(self.about_action)

    def main_window(self, width=800, height=600):

        self.setWindowTitle(self.lng['main']['title'])
        self.setWindowIcon(QIcon(app_icon))
        left, top = center_pos(window_object=self.qapp, width=width, height=height)
        self.setGeometry(left, top, width, height)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

        self.main_menu()

        self.toggle_menu(self.db_loaded)

        tab_top = 25

        self.tab_window = QTabWidget(parent=self)
        self.tab_window.move(0, tab_top)
        self.tab_window.setFixedHeight(height - tab_top)
        self.tab_window.setFixedWidth(width)
        self.tab_window.setMovable(True)
        self.tab_window.setTabsClosable(True)
        self.tab_window.tabCloseRequested.connect(self.close_tab_handler)

        self.show()

        # no File to open found, ask for ...
        if not self.database_file:
            self.window_openfile()
