from PyQt5.QtWidgets import QDialog, QPushButton, QCheckBox, QComboBox, QLabel, QFileDialog

from examsresult.configuration import current_config, save_config
from examsresult.tools import lng_list
from examsresult.views.core import CoreView


class ViewSettings(CoreView):

    def __init__(self, parent, lng, width=400, height=200):
        self.lng = lng
        local_lng = self.lng['window_settings']

        self.language_list = lng_list()
        config = current_config

        self.set_filetypes(self.lng['filetypes'])

        self.window = QDialog(parent=parent)
        self.window.setFixedHeight(height)
        self.window.setFixedWidth(width)
        self.window.setWindowTitle(local_lng['title'])

        self.button_save = QPushButton(local_lng['save'], self.window)
        self.button_save.move(215, 170)
        self.button_save.clicked.connect(self.save_settings)

        button_cancel = QPushButton(local_lng['close'], self.window)
        button_cancel.move(300, 170)
        button_cancel.clicked.connect(self.window.close)

        # File Openbox on startup ------------------------------------------
        self.checkbox_openbox_on_startup = QCheckBox(local_lng['openbox_on_startup'], self.window)
        self.checkbox_openbox_on_startup.move(40, 30)
        self.checkbox_openbox_on_startup.setChecked(config['openbox_on_startup'])
        self.checkbox_openbox_on_startup.stateChanged.connect(self.openbox_on_startup_change)

        # language ------------------------------------------
        self.listbox_language = QComboBox(self.window)

        tmp_list = []
        for l in self.language_list:
            tmp_list.append(l[0])
        tmp_list.sort()

        for t in tmp_list:
            self.listbox_language.addItem(t)
            self.listbox_language.move(40, 60)

        for l in self.language_list:
            if l[1] == config['language']:
                self.listbox_language.setCurrentIndex(self.listbox_language.findText(l[0]))
                break
        self.listbox_language.currentIndexChanged.connect(self.language_change)

        label_language = QLabel(local_lng['listbox_language'], self.window)
        label_language.move(130, 64)

        # File to open on startup ------------------------------------------
        label_openfile = QLabel(local_lng['open_file_on_startup_label'], self.window)
        label_openfile.move(40, 100)

        self.button_select = QPushButton(local_lng['open_file_on_startup_select'], self.window)
        self.button_select.move(215, 95)
        self.button_select.clicked.connect(self.openfile_on_startup_select)
        
        self.button_clear = QPushButton(local_lng['open_file_on_startup_clear'], self.window)
        self.button_clear.move(300, 95)
        self.button_clear.clicked.connect(self.openfile_on_startup_clear)

        self.label_file_to_open = QLabel(config['open_file_on_startup'], self.window)
        self.label_file_to_open.setGeometry(40, 120, 300, self.label_file_to_open.height())

        self.settings_changed(False)
        self.window.exec_()

    def settings_changed(self, flag):
        self.button_save.setEnabled(flag)

    def language_change(self, index):
        self.settings_changed(True)

    def openbox_on_startup_change(self):
        self.settings_changed(True)

    def openfile_on_startup_select(self):
        lng = self.lng['window_openfile']
        file_handler = QFileDialog()
        file_tuple = file_handler.getOpenFileName(parent=self.window, caption=lng['title'], filter=self.filetypes)
        database_file = file_tuple[0]

        if not database_file:
            return
        self.label_file_to_open.setText(database_file)
        self.settings_changed(True)

    def openfile_on_startup_clear(self):
        self.label_file_to_open.setText("")
        self.settings_changed(True)

    def save_settings(self):
        config = current_config

        for l in self.language_list:
            if l[0] == self.listbox_language.currentText():
                language = l[1]
                config['language'] = language
                break

        config['openbox_on_startup'] = self.checkbox_openbox_on_startup.isChecked()
        config['open_file_on_startup'] = self.label_file_to_open.text()

        save_config(config)

        self.settings_changed(False)
