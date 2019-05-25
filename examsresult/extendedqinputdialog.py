from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QDialog, QLabel, QFrame, QPushButton, QStyle


class ExtendedQInputDialog(QInputDialog):

    def selectButtonText(self):
        return '&Select'

    def clearButtonText(self):
        return 'C&lear'

    filetype_all = "All Files(*.*)"
    filetype_image = "Images (*.jpg *.jpeg *.png *.bmp)"

    # standard icons
    # https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/

    def getImage(self, parent, title, label, image_data=None, image_width=300, image_height=300):
        self.return_state = False
        self.image_data = image_data
        self.image_data_temp = image_data

        button_offset = 10

        def cancel_button_action():
            dialog_window.close()

        def ok_button_action():
            self.image_data = self.image_data_temp
            self.return_state = True
            dialog_window.close()

        def select_image_action(dummy_param=None):
            filetypes = ';;'.join([self.filetype_all, self.filetype_image])

            file_handler = QFileDialog()
            file_tuple = file_handler.getOpenFileName(parent=dialog_window,
                                                      filter=filetypes)
            filename = file_tuple[0]

            if not filename:
                return
            self.image_data_temp = filename
            load_image()

        def reset_image_button_action():
            self.image_data_temp = None
            load_image()

        def load_image():
            self.pixmap = QPixmap(self.image_data_temp)
            if self.image_data_temp:
                self.pixmap = self.pixmap.scaled(image_height, image_width, QtCore.Qt.KeepAspectRatio)
            image_window.setPixmap(self.pixmap)

        dialog_window = QDialog(parent)
        dialog_window.setWindowTitle(title)

        label_top_coord = 10
        label_left_coord = 10

        dialog_label = QLabel(dialog_window)
        dialog_label.setText(label)
        dialog_label.move(label_top_coord, label_left_coord)

        image_window = QLabel(dialog_window)
        image_window.mousePressEvent = select_image_action
        image_window.setFrameShape(QFrame.Panel)
        image_window.setFrameShadow(QFrame.Sunken)
        image_window.setLineWidth(3)

        button_select = QPushButton(dialog_window)
        button_select.setText(self.selectButtonText())
        button_select.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogOpenButton')))
        button_select.clicked.connect(select_image_action)

        button_clear = QPushButton(dialog_window)
        button_clear.setText(self.clearButtonText())
        button_clear.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogCancelButton')))
        button_clear.clicked.connect(reset_image_button_action)

        button_ok = QPushButton(dialog_window)
        button_ok.setText(self.okButtonText())
        button_ok.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogApplyButton')))
        button_ok.clicked.connect(ok_button_action)

        button_cancel = QPushButton(dialog_window)
        button_cancel.setText(self.cancelButtonText())
        button_cancel.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogCloseButton')))
        button_cancel.clicked.connect(cancel_button_action)

        # define positions in dialog window

        image_window_top = label_top_coord + dialog_label.height()
        image_window_left = label_left_coord
        image_window.setGeometry(image_window_left, image_window_top, image_height, image_width)

        button_left_coord = image_window_left + image_window.width() + button_offset
        button_top_coord = image_window_top
        button_select.move(button_left_coord, button_top_coord)

        button_top_coord += 30
        button_clear.move(button_left_coord, button_top_coord)

        button_top_coord = image_window_top + image_window.height() + button_offset
        window_height = button_top_coord + button_ok.height()
        window_width = button_left_coord + button_select.width()

        dialog_window.setGeometry(window_width, window_height, window_width, window_height)
        dialog_window.move(parent.window().rect().center())

        button_left_coord = window_width - button_ok.width()
        button_ok.move(button_left_coord, button_top_coord)
        button_left_coord -= button_cancel.width() - button_offset
        button_cancel.move(button_left_coord, button_top_coord)

        if image_data:
            load_image()

        dialog_window.exec()

        return self.image_data, self.return_state
