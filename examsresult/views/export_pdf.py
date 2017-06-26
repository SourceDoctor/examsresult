from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QFileDialog, \
    QGroupBox, QRadioButton, QLineEdit, QMessageBox, QCheckBox

from examsresult import current_config
from examsresult.tools import lng_load


class PDFExportSettings(object):

    settings = {'failure': False}
    encryption = False

    def __init__(self, parent, width=480, height=300):

        self.load_language()

        self.window = QDialog(parent=parent)
        self.window.setFixedHeight(height)
        self.window.setFixedWidth(width)
        self.window.setWindowTitle(self.lng['title'])

        self.radio_no_encryption = QRadioButton(self.window)
        self.radio_no_encryption.move(20, 20)
        self.radio_no_encryption.setText(self.lng['no_encryption'])
        self.radio_no_encryption.clicked.connect(self.encryption_type_changed)

        self.radio_encryption = QRadioButton(self.window)
        self.radio_encryption.move(20, 40)
        self.radio_encryption.setText(self.lng['encryption'])
        self.radio_encryption.clicked.connect(self.encryption_type_changed)

        self.security_settings = QGroupBox(self.window)
        self.security_settings.setGeometry(30, 45, self.window.width() - 20 - 20, 200)

        self.button_export = QPushButton(self.lng['export'], self.window)
        self.button_export.move(self.window.width() - self.button_export.width() - 20,
                                self.window.height() - self.button_export.height() - 10)
        self.button_export.clicked.connect(self.window_close)

        option_x = 300
        self.cancopy = QCheckBox(self.security_settings)
        self.cancopy.setText(self.lng['cancopy'])
        self.cancopy.move(option_x, 24)
        self.canmodify = QCheckBox(self.security_settings)
        self.canmodify.setText(self.lng['canmodify'])
        self.canmodify.move(option_x, 44)
        self.canprint = QCheckBox(self.security_settings)
        self.canprint.setText(self.lng['canprint'])
        self.canprint.move(option_x, 64)
        self.canannotate = QCheckBox(self.security_settings)
        self.canannotate.setText(self.lng['canannotate'])
        self.canannotate.move(option_x, 84)

        self.chk_userpassword_title = QCheckBox(self.lng['userpassword'], self.security_settings)
        self.chk_userpassword_title.clicked.connect(self.set_user_password_ability)
        self.chk_userpassword_title.move(10, 30)
        self.label_userpassword = QLabel(self.lng['password'], self.security_settings)
        self.label_userpassword.move(40, 50)
        self.text_userpassword = QLineEdit(self.security_settings)
        self.text_userpassword.setGeometry(160, 47, 100, 20)
        self.text_userpassword.setEchoMode(QLineEdit.Password)
        self.label_userpassword_retype = QLabel(self.lng['password_retype'], self.security_settings)
        self.label_userpassword_retype.move(40, 70)
        self.text_userpassword_retype = QLineEdit(self.security_settings)
        self.text_userpassword_retype.setEchoMode(QLineEdit.Password)
        self.text_userpassword_retype.setGeometry(160, 67, 100, 20)

        self.chk_ownerpassword_title = QCheckBox(self.lng['ownerpassword'], self.security_settings)
        self.chk_ownerpassword_title.clicked.connect(self.set_owner_password_ability)
        self.chk_ownerpassword_title.move(10, 130)
        self.label_ownerpassword = QLabel(self.lng['password'], self.security_settings)
        self.label_ownerpassword.move(40, 150)
        self.text_ownerpassword = QLineEdit(self.security_settings)
        self.text_ownerpassword.setEchoMode(QLineEdit.Password)
        self.text_ownerpassword.setGeometry(160, 147, 100, 20)
        self.label_ownerpassword_retype = QLabel(self.lng['password_retype'], self.security_settings)
        self.label_ownerpassword_retype.move(40, 170)
        self.text_ownerpassword_retype = QLineEdit(self.security_settings)
        self.text_ownerpassword_retype.setEchoMode(QLineEdit.Password)
        self.text_ownerpassword_retype.setGeometry(160, 167, 100, 20)

        self.radio_no_encryption.setChecked(True)
        self.chk_userpassword_title.setChecked(True)
        
        self.canannotate.setChecked(True)
        self.cancopy.setChecked(True)
        self.canmodify.setChecked(True)
        self.canprint.setChecked(True)

        self.set_user_password_ability()
        self.set_owner_password_ability()
        self.encryption_type_changed()

        self.window.exec_()

    def set_user_password_ability(self):
        enabled = self.chk_userpassword_title.isChecked()
        self.label_userpassword.setEnabled(enabled)
        self.text_userpassword.setEnabled(enabled)
        self.label_userpassword_retype.setEnabled(enabled)
        self.text_userpassword_retype.setEnabled(enabled)

        self.canannotate.setEnabled(enabled)
        self.cancopy.setEnabled(enabled)
        self.canmodify.setEnabled(enabled)
        self.canprint.setEnabled(enabled)
        if not enabled:
            self.chk_ownerpassword_title.setChecked(enabled)
            self.set_owner_password_ability()

    def set_owner_password_ability(self):
        enabled = self.chk_ownerpassword_title.isChecked()
        self.label_ownerpassword.setEnabled(enabled)
        self.text_ownerpassword.setEnabled(enabled)
        self.label_ownerpassword_retype.setEnabled(enabled)
        self.text_ownerpassword_retype.setEnabled(enabled)

    def encryption_type_changed(self):
        if self.radio_no_encryption.isChecked():
            self.encryption = False
        elif self.radio_encryption.isChecked():
            self.encryption = True

        self.security_settings.setEnabled(self.encryption)

    def collect_settings(self):
        settings = {}

        if self.chk_userpassword_title.isChecked():
            settings['userpassword'] = self.text_userpassword.text()
            settings['cancopy'] = self.cancopy.isChecked()
            settings['canmodify'] = self.canmodify.isChecked()
            settings['canprint'] = self.canprint.isChecked()
            settings['canannotate'] = self.canannotate.isChecked()

            if self.chk_ownerpassword_title.isChecked():
                settings['ownerpassword'] = self.text_ownerpassword.text()

        self.settings = settings

    def window_close(self):
        self.collect_settings()

        self.settings['failure'] = True

        if self.encryption:
            # check if enabled Password Types are filled with an password
            for key in ['userpassword', 'ownerpassword']:
                if key in self.settings.keys() and self.settings[key] == "":
                    QMessageBox.warning(self.window, "",self.lng['msg_empty_password'])
                    return
            # are passwords equal?
            if 'userpassword' in self.settings.keys():
                if self.text_userpassword.text() != self.text_userpassword_retype.text():
                    QMessageBox.warning(self.window, "",self.lng['msg_unequal_user_password'])
                    return
                if 'ownerpassword' in self.settings.keys():
                    if self.text_ownerpassword.text() != self.text_ownerpassword_retype.text():
                        QMessageBox.warning(self.window, "",self.lng['msg_unequal_owner_password'])
                        return

            if 'ownerpassword' in self.settings.keys():
                if self.text_userpassword.text() == self.text_ownerpassword.text():
                    QMessageBox.warning(self.window, "", self.lng['msg_user_owner_password_equal'])
                    return

        self.settings['failure'] = False
        self.window.close()

    def load_language(self):
        config = current_config
        lng = lng_load(config['language'])
        self.lng = lng['pdfexport']
