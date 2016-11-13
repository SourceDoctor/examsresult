from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QComboBox, QLabel, QFileDialog, QRadioButton

from examsresult.configuration import current_config, save_config
from examsresult.tools import lng_list
from examsresult.views.core import CoreView


class ViewSettings(CoreView):

    changed_mark_enabled = False

    def __init__(self, parent, lng, width=700, height=260):
        self.lng = lng
        local_lng = self.lng['window_settings']

        self.language_list = lng_list()
        config = current_config

        self.set_filetypes(self.lng['filetypes'])

        self.window = QDialog(parent=parent)
        self.window.setFixedHeight(height)
        self.window.setFixedWidth(width)
        self.window.setWindowTitle(local_lng['title'])

        y = 10
        # Calculation Methods for Results
        label_openfile = QLabel(self.lng['calculation_method']['title'], self.window)
        label_openfile.move(40, y)
        y += 15
        self.radio_complete = QRadioButton(self.window)
        self.radio_complete.move(40, y)
        self.radio_complete.setText(self.lng['calculation_method']['complete'])
        self.radio_complete.clicked.connect(self.calculation_method_change)
        self.radio_timeperiod = QRadioButton(self.window)
        y += 20
        self.radio_timeperiod.move(40, y)
        self.radio_timeperiod.setText(self.lng['calculation_method']['timeperiod'])
        self.radio_timeperiod.clicked.connect(self.calculation_method_change)

        if config['schoolyear_result_calculation_method'] == 'complete':
            self.radio_complete.setChecked(True)
        elif config['schoolyear_result_calculation_method'] == 'timeperiod':
            self.radio_timeperiod.setChecked(True)
        else:
            self.radio_complete.setChecked(True)

        y += 35
        # File Openbox on startup ------------------------------------------
        self.checkbox_openbox_on_startup = QCheckBox(local_lng['openbox_on_startup'], self.window)
        self.checkbox_openbox_on_startup.move(40, y)
        self.checkbox_openbox_on_startup.setChecked(config['openbox_on_startup'])
        self.checkbox_openbox_on_startup.stateChanged.connect(self.openbox_on_startup_change)

        # language ------------------------------------------
        y += 30
        self.listbox_language = QComboBox(self.window)
        self.listbox_language.move(40, y)
        tmp_list = []
        for l in self.language_list:
            tmp_list.append(l[0])
        tmp_list.sort()
        for t in tmp_list:
            self.listbox_language.addItem(t)
        for l in self.language_list:
            if l[1] == config['language']:
                self.listbox_language.setCurrentIndex(self.listbox_language.findText(l[0]))
                break
        self.listbox_language.currentIndexChanged.connect(self.language_change)

        label_language = QLabel(local_lng['listbox_language'], self.window)
        label_language.move(130, y + 4)

        # File to open on startup ------------------------------------------
        y += 40
        label_openfile = QLabel(local_lng['open_file_on_startup_label'], self.window)
        label_openfile.move(40, y)

        self.button_select = QPushButton(local_lng['open_file_on_startup_select'], self.window)
        self.button_select.move(215, y - 5)
        self.button_select.clicked.connect(self.openfile_on_startup_select)
        
        self.button_clear = QPushButton(local_lng['open_file_on_startup_clear'], self.window)
        self.button_clear.move(300, y - 5)
        self.button_clear.clicked.connect(self.openfile_on_startup_clear)

        y += 20
        self.label_file_to_open = QLabel(config['open_file_on_startup'], self.window)
        self.label_file_to_open.setGeometry(40, y, 300, self.label_file_to_open.height())

        y += 40
        button_cancel = QPushButton(local_lng['close'], self.window)
        button_cancel.move(self.window.width() - button_cancel.width() - 10, y)
        button_cancel.clicked.connect(self.window.close)

        self.button_save = QPushButton(local_lng['save'], self.window)
        self.button_save.move(self.window.width() - button_cancel.width() - self.button_save.width() - 10 - 10, y)
        self.button_save.clicked.connect(self.save_settings)

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

        config['schoolyear_result_calculation_method'] = calculation_method
        config['openbox_on_startup'] = self.checkbox_openbox_on_startup.isChecked()
        config['open_file_on_startup'] = self.label_file_to_open.text()

        save_config(config)

        self.set_changed(False)
