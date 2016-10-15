from examsresult.tools import lng_load, center_pos, app_icon
from examsresult.dbhandler import DatabaseConnector
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, \
    QDialog, QPushButton, QLabel, QTabWidget, QWidget
from PyQt5.QtGui import QIcon, QPixmap


class View(QMainWindow):

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

    def action_schoolyear_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolyear_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolclass_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolclass_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_subject_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_subject_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_examstype_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_examstype_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_timeperiod_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_timeperiod_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def window_newfile(self):
        lng = self.lng['window_newfile']
        # TODO: add per default File Extension
        file_tuple = QFileDialog.getSaveFileName(parent=self, caption=lng['title'], filter=self.filetypes)
        database_file = file_tuple[0]
        if database_file:
            self.database_file = database_file
            self.connect_db()

    def window_openfile(self):
        lng = self.lng['window_openfile']
        file_tuple = QFileDialog.getOpenFileName(parent=self, caption=lng['title'], filter=self.filetypes)
        database_file = file_tuple[0]
        if database_file:
            self.database_file = database_file
            self.connect_db()

    def window_schoolyear(self, lng):
        mytab = QWidget()
        self.tab_window.addTab(mytab, lng['title'])

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(50, 70)
        button_add.clicked.connect(lambda: self.action_schoolyear_add(self))
        button_edit = QPushButton(lng['edit'], mytab)
        button_edit.move(50, 90)
        button_edit.clicked.connect(lambda: self.action_schoolyear_edit(self))

    def window_schoolclass(self, lng):
        mytab = QWidget()
        self.tab_window.addTab(mytab, lng['title'])

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(40, 70)
        button_add.clicked.connect(lambda: self.action_schoolclass_add(self))
        button_edit = QPushButton(lng['edit'], mytab)
        button_edit.move(40, 90)
        button_edit.clicked.connect(lambda: self.action_schoolclass_edit(self))

    def window_subject(self, lng):
        mytab = QWidget()
        self.tab_window.addTab(mytab, lng['title'])

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(30, 70)
        button_add.clicked.connect(lambda: self.action_subject_add(self))
        button_edit = QPushButton(lng['edit'], mytab)
        button_edit.move(30, 90)
        button_edit.clicked.connect(lambda: self.action_subject_edit(self))

    def window_examstype(self, lng):
        mytab = QWidget()
        self.tab_window.addTab(mytab, lng['title'])

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(20, 70)
        button_add.clicked.connect(lambda: self.action_examstype_add(self))
        button_edit = QPushButton(lng['edit'], mytab)
        button_edit.move(20, 90)
        button_edit.clicked.connect(lambda: self.action_examstype_edit(self))

    def window_timeperiod(self, lng):
        mytab = QWidget()
        self.tab_window.addTab(mytab, lng['title'])

        button_add = QPushButton(lng['add'], mytab)
        button_add.move(10, 70)
        button_add.clicked.connect(lambda: self.action_timeperiod_add(self))
        button_edit = QPushButton(lng['edit'], mytab)
        button_edit.move(10, 90)
        button_edit.clicked.connect(lambda: self.action_timeperiod_edit(self))

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

    def add_tab_event(self, tab_window_to_open, lng):
        # Fixme: if tab added, and before Tabview was empty, first one has no content
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

        configuremenu = mainMenu.addMenu(menutext['mainmenuconfigure'])
        configuremenu.addAction(self.schoolyear_action)
        configuremenu.addAction(self.schoolclass_action)
        configuremenu.addAction(self.subject_action)
        configuremenu.addAction(self.examstype_action)
        configuremenu.addAction(self.timeperiod_action)

        helpmenu = mainMenu.addMenu(menutext['mainmenuhelp'])
        helpmenu.addAction(self.about_action)

    def main_window(self, width=800, height=600):

        def tab_close_handler(index):
            title = self.tab_window.tabText(index)
            self.open_tabs.remove(title)
            self.tab_window.removeTab(index)

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
        self.tab_window.tabCloseRequested.connect(tab_close_handler)

        self.show()

        # no File to open found, ask for ...
        if not self.database_file:
            self.window_openfile()
