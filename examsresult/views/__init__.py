from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QTabWidget
from examsresult.controls.dbhandler import DBHandler
from examsresult.tools import lng_load, center_pos, app_icon
from examsresult.views.about import ViewAbout
from .definition import ViewTimeperiod, ViewExamsType, ViewSchoolClass, ViewSchoolYear, ViewSubject
from .core import CoreView
from os.path import isfile


class BaseView(QMainWindow, CoreView):

    database_file = None
    db_loaded = False
    dbh = None
    open_tabs = []

    def __init__(self, qapp, config):
        super().__init__()
        self.config = config
        self.qapp = qapp
        self.lng = lng_load(language=config['language'])
        lng = self.lng['filetypes']

        filetype = []
        for desc in [(lng['filetype_exf'], '*.exf'), (lng['filetype_all'], '*')]:
            filetype.append("%s (%s)" % (desc[0], desc[1]))
        self.filetypes = ";;".join(filetype)

    def connect_db(self):
        if self.database_file:
            self.dbh = DBHandler(self.database_file)

        if not self.dbh:
            self.db_loaded = False
            QMessageBox.warning(self, "", self.lng['window_openfile']['msg_open_err'] % self.database_file)
        else:
            self.db_loaded = True
            old_db_version, db_version = self.dbh.dbc.db_updater()
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

    def filedialog_handler(self, dialog_type, database_file=None):
        if database_file and not isfile(database_file):
            message = "%s\n%s" % (self.lng['main']['msg_file_not_found'], database_file)
            QMessageBox.warning(self, self.lng['main']['title'], message)
            database_file = None

        if not database_file:
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
        self.filedialog_handler('new')

    def window_openfile(self):
        self.filedialog_handler('open')

    def window_settings(self, lng):
        QMessageBox.information(self.tab_window, '', "Give me something to do")

    def window_schoolyear(self, lng):
        ViewSchoolYear(self.dbh, self.tab_window, lng)

    def window_schoolclass(self, lng):
        ViewSchoolClass(self.dbh, self.tab_window, lng)

    def window_subject(self, lng):
        ViewSubject(self.dbh, self.tab_window, lng)

    def window_examstype(self, lng):
        ViewExamsType(self.dbh, self.tab_window, lng)

    def window_timeperiod(self, lng):
        ViewTimeperiod(self.dbh, self.tab_window, lng)

    def window_about(self, parent, width=400, height=100):
        ViewAbout(parent=parent, lng=self.lng, width=width, height=height)

    def closeEvent(self, event):
        self.action_app_close()

    def close_tab_handler(self, index):
        title = self.tab_window.tabText(index)
        if title.startswith(self.changed_mark):
            answer = QMessageBox.question(self, self.lng['main']['title'], self.lng['main']['msg_close_unsaved'])
            if answer == QMessageBox.No:
                return
            title = title.replace(self.changed_mark, '')
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
        self.settings_action = QAction(menutext['settings'], self)
        self.settings_action.triggered.connect(self.window_settings)
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
        filemenu.addAction(self.settings_action)
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

        # open File on startup
        if self.config['open_file_on_startup']:
            self.filedialog_handler('open', database_file=self.config['open_file_on_startup'])

        # no File to open found, ask for ...
        if self.config['openbox_on_startup'] and not self.database_file:
            self.window_openfile()
