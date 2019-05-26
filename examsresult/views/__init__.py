from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QTabWidget, QWidget
from examsresult.controls.dbhandler import DBHandler
from examsresult.extendedqinputdialog import ExtendedQInputDialog
from examsresult.tools import lng_load, center_pos, app_icon, sort
from examsresult.views.core import CoreView
from examsresult.views.report import ViewReportStudent, ViewReportSchoolclass
from examsresult.views.settings import ViewSettings
from examsresult.views.configuration import ViewSchoolClassConfigure, ViewExamConfigure
from examsresult.views.definition import ViewTimeperiod, ViewExamsType, ViewSchoolClass, ViewSchoolYear, ViewSubject
from examsresult.views.about import ViewAbout
from os.path import isfile, basename


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
        self.set_filetypes(self.lng['filetypes'])

    def connect_db(self):
        if self.database_file:
            self.dbh = DBHandler(self.database_file)

        if not self.dbh:
            self.db_loaded = False
            QMessageBox.warning(self, "", self.lng['window_openfile']['msg_open_err'] % self.database_file)
        else:
            self.db_loaded = True
            db_versions_difference = self.dbh.dbc.db_version_difference

            if db_versions_difference > 0:
                answer = QMessageBox.question(self, "", self.lng['window_openfile']['msg_db_has_to_be_updated'] % self.database_file)
                if answer == QMessageBox.Yes:
                    if self.dbh.dbc.db_updater():
                        QMessageBox.information(self, "", self.lng['window_openfile']['msg_db_updated'] % self.database_file)
                    else:
                        QMessageBox.warning(self, "", self.lng['window_openfile']['msg_db_update_failure'] % self.database_file)
                        self.db_loaded = False
                else:
                    self.db_loaded = False

            elif db_versions_difference < 0:
                self.db_loaded = False
                QMessageBox.warning(self, "", self.lng['window_openfile']['msg_db_to_new'] % self.database_file)

            else:
                # Version is on newest state
                pass

        if self.db_loaded:
            if self.config['title_view'] == 'fullpath':
                self.setWindowTitle("%s - %s" % (self.lng['main']['title'], self.database_file))
            elif self.config['title_view'] == 'filename':
                self.setWindowTitle("%s - %s" % (self.lng['main']['title'], basename(self.database_file)))
            else:
                print("critical unknown Key '%s' in settings" % self.config['title_view'])
                self.setWindowTitle("%s - %s" % (self.lng['main']['title'], basename(self.database_file)))
        else:
            self.setWindowTitle(self.lng['main']['title'])
            self.database_file = None

        self.toggle_menu(self.db_loaded)

    def toggle_menu(self, db_state):
        # Enable/Disable Menu Entries
        self.report_schoolclass_action.setEnabled(db_state)
        self.report_student_action.setEnabled(db_state)
        self.schoolclass_configure_action.setEnabled(db_state)
        self.exam_configure_action.setEnabled(db_state)
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
                file_tuple = file_handler.getSaveFileName(parent=self, caption=lng['title'], filter=self.filetypes)
                database_file = file_tuple[0]
                if not database_file.endswith('.exf'):
                    database_file += '.exf'
            elif dialog_type == 'open':
                lng = self.lng['window_openfile']
                file_tuple = file_handler.getOpenFileName(parent=self, caption=lng['title'], filter=self.filetypes)
                database_file = file_tuple[0]
            else:
                print("CRITICAL, unknown filedialog type to handle")
                return

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

    def window_settings(self, parent):
        ViewSettings(parent=parent, lng=self.lng)

    def window_report_schoolclass(self, lng):
        report_dialog = ExtendedQInputDialog(parent=self.tab_window)

        schoolyear_list = [y[1] for y in self.dbh.get_schoolyear()]
        schoolyear_list = sort(schoolyear_list, reverse=True)
        schoolyear, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['schoolyear'], schoolyear_list, 0, False)
        if not ok:
            return False

        schoolclass_list = [c[1] for c in self.dbh.get_schoolclass(schoolyear=schoolyear)]
        schoolclass_list = sort(schoolclass_list)
        schoolclass, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['schoolclass'], schoolclass_list, 0, False)
        if not ok:
            return False

        subject_list = [s[1] for s in self.dbh.get_subject()]
        subject_list = sort(subject_list)
        subject, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['subject'], subject_list, 0, False)
        if not ok:
            return False

        is_combined = self.dbh.get_schoolclass_combine(schoolyear=schoolyear, schoolclassname=schoolclass)
        if is_combined:
            _combined_class_list = self.dbh.get_combined_classes(schoolyear=schoolyear, schoolclassname=schoolclass)
            _combined_class_list.sort()
            combined_class_list = [self.lng['main']['all']]
            combined_class_list.extend(_combined_class_list)
            combined_class, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['real_schoolclass'], combined_class_list, 0, False)
            if not ok:
                return False
            if combined_class == self.lng['main']['all']:
                combined_class = None
        else:
            combined_class = None

        data = {
            'schoolyear': schoolyear,
            'schoolclass': schoolclass,
            'combined_class': combined_class,
            'subject': subject,
        }

        ViewReportSchoolclass(self.dbh, self.tab_window, lng, data)
        return True

    def window_report_student(self, lng):
        student_list = []
        student_id_dict = {}

        report_dialog = ExtendedQInputDialog(parent=self.tab_window)

        schoolyear_list = [y[1] for y in self.dbh.get_schoolyear()]
        schoolyear_list = sort(schoolyear_list, reverse=True)
        schoolyear, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['schoolyear'], schoolyear_list, 0, False)
        if not ok:
            return False

        schoolclass_list = [c[1] for c in self.dbh.get_schoolclass(schoolyear=schoolyear)]
        schoolclass_list = sort(schoolclass_list)
        schoolclass, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['schoolclass'], schoolclass_list, 0, False)
        if not ok:
            return False

        subject_list = [s[1] for s in self.dbh.get_subject()]
        subject_list = sort(subject_list)
        subject, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['subject'], subject_list, 0, False)
        if not ok:
            return False

        for c in self.dbh.get_schoolclassstudents(schoolyear=schoolyear, schoolclass=schoolclass):
            name = "%s, %s" % (c[1], c[2])
            student_list.append(name)
            student_id_dict[name] = c[0]
        student_list = sort(student_list)
        student, ok = report_dialog.getItem(self.tab_window, self.lng['menu']['mainmenureport'], self.lng['menu']['student'], student_list, 0, False)
        if not ok:
            return False
        student_id = student_id_dict[student]

        data = {
            'schoolyear': schoolyear,
            'schoolclass': schoolclass,
            'subject': subject,
            'student_id': student_id
        }

        ViewReportStudent(self.dbh, self.tab_window, lng, data)
        return True

    def window_configure_schoolclass(self, lng):
        ViewSchoolClassConfigure(self.dbh, self.tab_window, lng)
        return True

    def window_configure_exam(self, lng):
        ViewExamConfigure(self.dbh, self.tab_window, lng)
        return True

    def window_define_schoolyear(self, lng):
        ViewSchoolYear(self.dbh, self.tab_window, lng)
        return True

    def window_define_schoolclass(self, lng):
        ViewSchoolClass(self.dbh, self.tab_window, lng)
        return True

    def window_define_subject(self, lng):
        ViewSubject(self.dbh, self.tab_window, lng)
        return True

    def window_define_examstype(self, lng):
        ViewExamsType(self.dbh, self.tab_window, lng)
        return True

    def window_define_timeperiod(self, lng):
        ViewTimeperiod(self.dbh, self.tab_window, lng)
        return True

    def window_about(self, parent):
        ViewAbout(dbhandler=self.dbh, parent=parent, lng=self.lng)
        return True

    def closeEvent(self, event):
        index = -1
        while index <= self.tab_window.count() - 1:
            index += 1
            title = self.tab_window.tabText(index)
            if not title.startswith(self.changed_mark):
                continue
            answer = QMessageBox.question(self, self.lng['main']['title'], self.lng['main']['msg_close_unsaved'])
            if answer == QMessageBox.No:
                event.ignore()
                return
            break
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
        # add dummy Tab (prevent incomplete view of first Tab)
        if not self.tab_window.count():
            self.tab_window.addTab(QWidget(), "")
            dummy_tab_present = True
        else:
            dummy_tab_present = False

        # add Tab only if not still open
        if lng['title'] not in self.open_tabs:
            self.open_tabs.append(lng['title'])
            if not tab_window_to_open(lng):
                self.open_tabs.remove(lng['title'])

        # remove dummy Tab
        if dummy_tab_present:
            self.tab_window.removeTab(0)

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
        self.settings_action.triggered.connect(lambda: self.window_settings(self))
        self.exit_action = QAction(menutext['quit'], self)
        self.exit_action.triggered.connect(self.action_app_close)
        # Report menu actions
        self.report_schoolclass_action = QAction(menutext['schoolclass'], self)
        self.report_schoolclass_action.triggered.connect(lambda: self.add_tab_event(self.window_report_schoolclass, self.lng['window_report_schoolclass']))
        self.report_student_action = QAction(menutext['student'], self)
        self.report_student_action.triggered.connect(lambda: self.add_tab_event(self.window_report_student, self.lng['window_report_student']))
        # configure menu actions
        self.schoolclass_configure_action = QAction(menutext['schoolclass'], self)
        self.schoolclass_configure_action.triggered.connect(lambda: self.add_tab_event(self.window_configure_schoolclass, self.lng['window_configure_schoolclass']))
        self.exam_configure_action = QAction(menutext['exam'], self)
        self.exam_configure_action.triggered.connect(lambda: self.add_tab_event(self.window_configure_exam, self.lng['window_configure_exam']))
        # Definition menu actions
        self.schoolyear_action = QAction(menutext['schoolyear'], self)
        self.schoolyear_action.triggered.connect(lambda: self.add_tab_event(self.window_define_schoolyear, self.lng['window_define_schoolyear']))
        self.schoolclass_action = QAction(menutext['schoolclass'], self)
        self.schoolclass_action.triggered.connect(lambda: self.add_tab_event(self.window_define_schoolclass, self.lng['window_define_schoolclass']))
        self.subject_action = QAction(menutext['subject'], self)
        self.subject_action.triggered.connect(lambda: self.add_tab_event(self.window_define_subject, self.lng['window_define_subject']))
        self.examstype_action = QAction(menutext['examstype'], self)
        self.examstype_action.triggered.connect(lambda: self.add_tab_event(self.window_define_examstype, self.lng['window_define_examstype']))
        self.timeperiod_action = QAction(menutext['timeperiod'], self)
        self.timeperiod_action.triggered.connect(lambda: self.add_tab_event(self.window_define_timeperiod, self.lng['window_define_timeperiod']))
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

        reportmenu = mainMenu.addMenu(menutext['mainmenureport'])
        reportmenu.addAction(self.report_schoolclass_action)
        reportmenu.addAction(self.report_student_action)

        configurationmenu = mainMenu.addMenu(menutext['mainmenuconfigure'])
        configurationmenu.addAction(self.schoolclass_configure_action)
        configurationmenu.addAction(self.exam_configure_action)

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

        tab_left = 0
        tab_top = 25

        self.tab_window = QTabWidget(parent=self)
        self.tab_window.move(tab_left, tab_top)
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
