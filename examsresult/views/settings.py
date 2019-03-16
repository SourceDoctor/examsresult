from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QComboBox, QLabel,\
    QFileDialog, QRadioButton, QGroupBox, QVBoxLayout, QHBoxLayout

from examsresult.configuration import current_config, save_config
from examsresult.tools import lng_list
from examsresult.views.core import CoreView


class ViewSettings(CoreView):

    changed_mark_enabled = False

    def __init__(self, parent, lng, width=650, height=400):
        self.lng = lng
        local_lng = self.lng['window_settings']

        self.language_list = lng_list()
        config = current_config

        self.set_filetypes(self.lng['filetypes'])

        self.window = QDialog(parent=parent)
        self.window.setFixedHeight(height)
        self.window.setFixedWidth(width)
        self.window.setWindowTitle(local_lng['title'])

        # Calculation Methods for Results
        self.radio_complete = QRadioButton()
        self.radio_complete.setText(self.lng['calculation_method']['complete'])
        self.radio_complete.clicked.connect(self.calculation_method_change)

        self.radio_timeperiod = QRadioButton()
        self.radio_timeperiod.setText(self.lng['calculation_method']['timeperiod'])
        self.radio_timeperiod.clicked.connect(self.calculation_method_change)

        calc_box_layout = QGroupBox(self.lng['calculation_method']['title'], self.window)
        _calc_box_layout = QVBoxLayout()
        _calc_box_layout.addWidget(self.radio_complete)
        _calc_box_layout.addWidget(self.radio_timeperiod)
        _calc_box_layout.setSpacing(0)
        calc_box_layout.setLayout(_calc_box_layout)

        # show filename fullpath or filename only in title
        self.radio_title_filename = QRadioButton()
        self.radio_title_filename.setText(self.lng['window_settings']['show_file_name'])
        self.radio_title_filename.clicked.connect(self.calculation_method_change)

        self.radio_title_fullpath = QRadioButton()
        self.radio_title_fullpath.setText(self.lng['window_settings']['show_full_path'])
        self.radio_title_fullpath.clicked.connect(self.calculation_method_change)

        title_view_layout = QGroupBox(self.lng['window_settings']['title_view'], self.window)
        _title_view_layout = QVBoxLayout()
        _title_view_layout.addWidget(self.radio_title_filename)
        _title_view_layout.addWidget(self.radio_title_fullpath)
        _title_view_layout.setSpacing(0)
        title_view_layout.setLayout(_title_view_layout)

        # File Openbox on startup ------------------------------------------
        self.checkbox_openbox_on_startup = QCheckBox(local_lng['openbox_on_startup'], self.window)
        self.checkbox_openbox_on_startup.stateChanged.connect(self.openbox_on_startup_change)

        # language ------------------------------------------
        self.listbox_language = QComboBox(self.window)
        self.listbox_language.currentIndexChanged.connect(self.language_change)

        label_language = QLabel(local_lng['listbox_language'], self.window)

        # File to open on startup ------------------------------------------
        label_openfile = QLabel(local_lng['open_file_on_startup_label'], self.window)

        self.button_select = QPushButton(local_lng['open_file_on_startup_select'], self.window)
        self.button_select.clicked.connect(self.openfile_on_startup_select)

        self.button_clear = QPushButton(local_lng['open_file_on_startup_clear'], self.window)
        self.button_clear.clicked.connect(self.openfile_on_startup_clear)

        self.label_file_to_open = QLabel(config['open_file_on_startup'], self.window)

        # site layout
        y = 10
        calc_box_layout.move(20, y)
        y += 100
        title_view_layout.move(20, y)
        y += 100
        label_language.move(20, y)
        self.listbox_language.move(10 + label_language.width(), y)
        y += 35
        self.checkbox_openbox_on_startup.move(20, y)
        y += 40
        label_openfile.move(20, y)
        self.button_select.move(205, y - 5)
        self.button_clear.move(290, y - 5)
        y += 20
        self.label_file_to_open.setGeometry(40, y, 500, self.label_file_to_open.height())
        y += 40

        button_cancel = QPushButton(local_lng['close'], self.window)
        button_cancel.move(self.window.width() - button_cancel.width() - 10, y)
        button_cancel.clicked.connect(self.window.close)

        self.button_save = QPushButton(local_lng['save'], self.window)
        self.button_save.move(self.window.width() - button_cancel.width() - self.button_save.width() - 10 - 10, y)
        self.button_save.clicked.connect(self.save_settings)

        self.listbox_language.currentIndexChanged.connect(self.language_change)

        # load Settings to view
        if config['schoolyear_result_calculation_method'] == 'complete':
            self.radio_complete.setChecked(True)
        elif config['schoolyear_result_calculation_method'] == 'timeperiod':
            self.radio_timeperiod.setChecked(True)
        else:
            self.radio_complete.setChecked(True)

        if config['title_view'] == 'filename':
            self.radio_title_filename.setChecked(True)
        elif config['title_view'] == 'fullpath':
            self.radio_title_fullpath.setChecked(True)
        else:
            self.radio_title_filename.setChecked(True)

        self.checkbox_openbox_on_startup.setChecked(config['openbox_on_startup'])

        tmp_list = [x[0] for x in self.language_list]
        tmp_list.sort()
        for t in tmp_list:
            self.listbox_language.addItem(t)
        for l in self.language_list:
            if l[1] == config['language']:
                self.listbox_language.setCurrentIndex(self.listbox_language.findText(l[0]))
                break

        self.set_changed(False)
        self.window.exec_()

    def calculation_method_change(self):
        self.set_changed(True)

    def language_change(self, index):
        self.set_changed(True)

    def openbox_on_startup_change(self):
        self.set_changed(True)

    def openfile_on_startup_select(self):
        lng = self.lng['window_openfile']
        file_handler = QFileDialog()
        file_tuple = file_handler.getOpenFileName(parent=self.window, caption=lng['title'], filter=self.filetypes)
        database_file = file_tuple[0]

        if not database_file:
            return
        self.label_file_to_open.setText(database_file)
        self.set_changed(True)

    def openfile_on_startup_clear(self):
        self.label_file_to_open.setText("")
        self.set_changed(True)

    def save_settings(self):
        config = current_config

        for l in self.language_list:
            if l[0] == self.listbox_language.currentText():
                language = l[1]
                config['language'] = language
                break

        if self.radio_complete.isChecked():
            calculation_method = 'complete'
        elif self.radio_timeperiod.isChecked():
            calculation_method = 'timeperiod'
        else:
            calculation_method = 'complete'

        if self.radio_title_filename.isChecked():
            title_view = 'filename'
        elif self.radio_title_fullpath.isChecked():
            title_view = 'fullpath'
        else:
            title_view = 'filename'

        config['schoolyear_result_calculation_method'] = calculation_method
        config['title_view'] = title_view
        config['openbox_on_startup'] = self.checkbox_openbox_on_startup.isChecked()
        config['open_file_on_startup'] = self.label_file_to_open.text()

        save_config(config)

        self.set_changed(False)
