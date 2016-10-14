from examsresult.tools import lng_load, center_pos, app_icon
from examsresult.dbhandler import DatabaseConnector
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, \
    QDialog, QPushButton, QLabel, QTabWidget, QWidget
from PyQt5.QtGui import QIcon, QPixmap


class View(QMainWindow):

    database_file = None
    db_loaded = False
    dbc = None

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
        menutext = self.lng['menu']
        self.schoolyear_action.setEnabled(db_state)
        self.schoolclass_action.setEnabled(db_state)
        self.subject_action.setEnabled(db_state)

    def action_app_close(self):
        self.close()

    def action_subject_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_subject_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_subject_remove(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolyear_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolyear_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolyear_remove(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolclass_add(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolclass_edit(self, root_window):
        # TODO: Give me something to do
        QMessageBox.information(root_window, "", "Give me something to do!")

    def action_schoolclass_remove(self, root_window):
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

    def window_schoolyear(self, root_window, width=400, height=150):
        lng = self.lng['window_schoolyear']
        tk_window = Toplevel(root_window)
        tk_window.transient(root_window)
        tk_window.title(string=lng['title'])
        tk_window.minsize(width=width, height=height)
        tk_window.maxsize(width=width, height=height)
        center_pos(window_object=tk_window, width=width, height=height)

        btn_add = Button(tk_window, text=self.lng['main']['add'], command=lambda: self.action_schoolyear_add(tk_window), width=10)
        btn_edit = Button(tk_window, text=self.lng['main']['edit'], command=lambda: self.action_schoolyear_edit(tk_window), width=10)
        btn_remove = Button(tk_window, text=self.lng['main']['remove'], command=lambda: self.action_schoolyear_remove(tk_window), width=10)
        btn_close = Button(tk_window, text=self.lng['main']['close'], command=tk_window.destroy, width=10)
        btn_add.focus()
        btn_add.pack()
        btn_edit.pack()
        btn_remove.pack()
        btn_close.pack()

    def window_schoolclass(self, root_window, width=400, height=150):
        lng = self.lng['window_schoolclass']
        tk_window = Toplevel(root_window)
        tk_window.transient(root_window)
        tk_window.title(string=lng['title'])
        tk_window.minsize(width=width, height=height)
        tk_window.maxsize(width=width, height=height)
        center_pos(window_object=tk_window, width=width, height=height)

        btn_add = Button(tk_window, text=self.lng['main']['add'], command=lambda: self.action_schoolclass_add(tk_window), width=10)
        btn_edit = Button(tk_window, text=self.lng['main']['edit'], command=lambda: self.action_schoolclass_edit(tk_window), width=10)
        btn_remove = Button(tk_window, text=self.lng['main']['remove'], command=lambda: self.action_schoolclass_remove(tk_window), width=10)
        btn_close = Button(tk_window, text=self.lng['main']['close'], command=tk_window.destroy, width=10)
        btn_add.focus()
        btn_add.pack()
        btn_edit.pack()
        btn_remove.pack()
        btn_close.pack()

    def window_subject(self, root_window, width=400, height=150):
        lng = self.lng['window_subject']
        tk_window = Toplevel(root_window)
        tk_window.transient(root_window)
        tk_window.title(string=lng['title'])
        tk_window.minsize(width=width, height=height)
        tk_window.maxsize(width=width, height=height)
        center_pos(window_object=tk_window, width=width, height=height)

        btn_add = Button(tk_window, text=self.lng['main']['add'], command=lambda: self.action_subject_add(tk_window), width=10)
        btn_edit = Button(tk_window, text=self.lng['main']['edit'], command=lambda: self.action_subject_edit(tk_window), width=10)
        btn_remove = Button(tk_window, text=self.lng['main']['remove'], command=lambda: self.action_subject_remove(tk_window), width=10)
        btn_close = Button(tk_window, text=self.lng['main']['close'], command=tk_window.destroy, width=10)
        btn_add.focus()
        btn_add.pack()
        btn_edit.pack()
        btn_remove.pack()
        btn_close.pack()

    def window_about(self, parent_window, width=400, height=100):
        lng = self.lng['window_about']

        window = QDialog(parent=parent_window)
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

    def main_menu(self):
        mainMenu = self.menuBar()
        menutext = self.lng['menu']

        # File menu
        self.new_action = QAction(menutext['newfile'], self)
        self.new_action.triggered.connect(self.window_newfile)
        self.open_action = QAction(menutext['openfile'], self)
        self.open_action.triggered.connect(self.window_openfile)
        self.exit_action = QAction(menutext['quit'], self)
        self.exit_action.triggered.connect(self.action_app_close)

        filemenu = mainMenu.addMenu(menutext['mainmenufile'])
        filemenu.addAction(self.new_action)
        filemenu.addAction(self.open_action)
        filemenu.addSeparator()
        filemenu.addAction(self.exit_action)

        # Edit menu
        self.schoolyear_action = QAction(menutext['schoolyear'], self)
        self.schoolyear_action.triggered.connect(self.window_schoolyear)
        self.schoolclass_action = QAction(menutext['schoolclass'], self)
        self.schoolclass_action.triggered.connect(self.window_schoolclass)
        self.subject_action = QAction(menutext['subject'], self)
        self.subject_action.triggered.connect(self.window_subject)

        editmenu = mainMenu.addMenu(menutext['mainmenuedit'])
        editmenu.addAction(self.schoolyear_action)
        editmenu.addAction(self.schoolclass_action)
        editmenu.addAction(self.subject_action)

        # Help menu
        self.about_action = QAction(menutext['about'], self)
        self.about_action.triggered.connect(lambda: self.window_about(self))

        helpmenu = mainMenu.addMenu(menutext['mainmenuhelp'])
        helpmenu.addAction(self.about_action)

    def main_window(self, width=800, height=600):

        def tab_close_handler(index):
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

        #         # # no File to open found, ask for ...
        #         # if not self.database_file:
        #         #     self.window_openfile()
        #
        tab_top = 25

        self.tab_window = QTabWidget(parent=self)
        self.tab_window.move(0, tab_top)
        self.tab_window.setFixedHeight(height - tab_top)
        self.tab_window.setFixedWidth(width)
        self.tab_window.setMovable(True)
        self.tab_window.setTabsClosable(True)
        self.tab_window.tabCloseRequested.connect(tab_close_handler)

        # Todo: Focus on last opened Tab
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab_window.addTab(self.tab1, "Tab 1")
        self.tab_window.addTab(self.tab2, "Tab 2")
        self.tab_window.addTab(self.tab3, "Tab 3")
        self.tab_window.addTab(self.tab1, "Tab 1")

        self.show()
