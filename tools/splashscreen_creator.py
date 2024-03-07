import sys

from glitch_this import ImageGlitcher
from PIL import Image
from PIL.ImageQt import ImageQt

import cv2
import numpy as np

from PySide6 import QtWidgets, QtCore, QtGui


class SplashScreenCreator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Splash Screen Creator")

        self.label = QtWidgets.QLabel("Select an image for the splash screen")
        self.label.setFixedSize(475, 313)
        self.image_path_line_edit = QtWidgets.QLineEdit()
        self.image_path_line_edit.setPlaceholderText("Select an image")
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.create_button = QtWidgets.QPushButton("Create Splash Screen")
        self.create_button.setEnabled(False)
        self.save_button = QtWidgets.QPushButton("Save Splash Screen")
        self.save_button.setEnabled(False)
        self.amount_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.amount_slider.setRange(1, 100)
        self.amount_slider.setValue(20)
        self.scan_lines_checkbox = QtWidgets.QCheckBox("Scan Lines")
        self.color_offset_checkbox = QtWidgets.QCheckBox("Color Offset")
        self.fixed_seed_checkbox = QtWidgets.QCheckBox("Fixed Seed")
        self.vignette_spinbox = QtWidgets.QSpinBox()
        self.vignette_spinbox.setRange(0, 1000)
        self.vignette_spinbox.setValue(300)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)

        self.options_layout = QtWidgets.QHBoxLayout()
        self.options_layout.addWidget(QtWidgets.QLabel("Glitch Amount: "))
        self.options_layout.addWidget(self.amount_slider)
        self.options_layout.addWidget(self.scan_lines_checkbox)
        self.options_layout.addWidget(self.color_offset_checkbox)
        self.options_layout.addWidget(self.fixed_seed_checkbox)
        self.layout.addLayout(self.options_layout)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.save_button)
        self.layout.addLayout(self.button_layout)

        self.image_selector_layout = QtWidgets.QHBoxLayout()
        self.image_selector_layout.addWidget(self.image_path_line_edit)
        self.image_selector_layout.addWidget(self.browse_button)
        self.layout.addLayout(self.image_selector_layout)

        self.setLayout(self.layout)

        self.browse_button.clicked.connect(self.browse_image)
        self.create_button.clicked.connect(self.create_splash_screen)
        self.save_button.clicked.connect(self.save_splash_screen)
        self.image_path_line_edit.textChanged.connect(self.validate_image_path)

        QtCore.QCoreApplication.instance().aboutToQuit.connect(self.on_quit)

        # load settings from ini
        self.load_settings()

    def load_settings(self):
        settings = QtCore.QSettings("splash_screen_creator.ini", QtCore.QSettings.IniFormat)

        self.image_path_line_edit.setText(str(settings.value("image_path", "")))
        self.amount_slider.setValue(int(settings.value("glitch_amount", 20)))
        self.scan_lines_checkbox.setChecked(True if settings.value("scan_lines", False) == "true" else False)
        self.color_offset_checkbox.setChecked(True if settings.value("color_offset", False) == "true" else False)
        self.fixed_seed_checkbox.setChecked(True if settings.value("fixed_seed", False) == "true" else False)

    def browse_image(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.image_path_line_edit.setText(file_path)

    def validate_image_path(self, text):
        self.create_button.setEnabled(QtCore.QFile.exists(text))

    def create_splash_screen(self):
        img = Image.open(self.image_path_line_edit.text())
        img = img.convert("RGB")

        glitcher = ImageGlitcher()
        img = glitcher.glitch_image(img, glitch_amount=self.amount_slider.value() / 10.0,
                                    scan_lines=self.scan_lines_checkbox.isChecked(),
                                    color_offset=self.color_offset_checkbox.isChecked(),
                                    seed=None if not self.fixed_seed_checkbox.isChecked() else 1)

        if self.scan_lines_checkbox.isChecked():
            img = self.increase_brightness(img, 50)
            img = self.increase_contrast(img, 2.0, 8)

        img = img.resize((475, 313))
        img = QtGui.QPixmap.fromImage(ImageQt(img))
        self.label.setPixmap(img)
        self.save_button.setEnabled(True)

    def add_vignette(self, img):
        img = np.array(img)
        rows, cols, _ = img.shape
        kernel_x = cv2.getGaussianKernel(cols, self.vignette_spinbox.value())
        kernel_y = cv2.getGaussianKernel(rows, self.vignette_spinbox.value())
        kernel = kernel_y * kernel_x.T
        mask = 255 * kernel / np.linalg.norm(kernel)
        for i in range(3):
            img[:, :, i] = img[:, :, i] * mask
        img = Image.fromarray(img)
        return img

    def increase_brightness(self, img, value=30):
        img = np.array(img)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        img = Image.fromarray(img)
        return img

    def increase_contrast(self, img, limit: float = 2.0, grid_size: int = 8):
        img = np.array(img)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=limit, tileGridSize=(grid_size, grid_size))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        img = Image.fromarray(img)
        return img

    def save_splash_screen(self):
        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle("Save Splash Screen")
        dialog.setText("Do you want to save the splash screen?")
        dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dialog.setDefaultButton(QtWidgets.QMessageBox.Yes)
        response = dialog.exec()
        if response == QtWidgets.QMessageBox.No:
            return
        self.label.pixmap().save("../resources/img/splashscreen.png", "PNG")
        print("Splash screen saved")

    def on_quit(self):
        # save state to file
        settings = QtCore.QSettings("splash_screen_creator.ini", QtCore.QSettings.IniFormat)
        settings.setValue("image_path", self.image_path_line_edit.text())
        settings.setValue("glitch_amount", self.amount_slider.value())
        settings.setValue("scan_lines", self.scan_lines_checkbox.isChecked())
        settings.setValue("color_offset", self.color_offset_checkbox.isChecked())
        settings.setValue("fixed_seed", self.fixed_seed_checkbox.isChecked())

        settings.sync()


if __name__ == "__main__":
    # build Qt GUI that allows to select file and displays image
    app = QtWidgets.QApplication(sys.argv)
    window = SplashScreenCreator()
    window.show()
    sys.exit(app.exec())
