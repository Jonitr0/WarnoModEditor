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
        self.noise_checkbox = QtWidgets.QCheckBox("Noise")
        self.vignette_checkbox = QtWidgets.QCheckBox("Vignette")
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
        self.options_layout.addWidget(self.noise_checkbox)
        self.options_layout.addWidget(self.vignette_checkbox)
        self.options_layout.addWidget(QtWidgets.QLabel("Vignette Sigma: "))
        self.options_layout.addWidget(self.vignette_spinbox)
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
        img = img.resize((475, 313)).convert("RGB")

        if self.vignette_checkbox.isChecked():
            img = self.add_vignette(img)

        glitcher = ImageGlitcher()
        result = glitcher.glitch_image(img, glitch_amount=self.amount_slider.value()/10.0,
                                       scan_lines=self.scan_lines_checkbox.isChecked(),
                                       color_offset=self.color_offset_checkbox.isChecked())

        if self.noise_checkbox.isChecked():
            result = self.add_noise(result)

        result = QtGui.QPixmap.fromImage(ImageQt(result))
        self.label.setPixmap(result)
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

    def add_noise(self, img):
        # TODO: Add noise to the image
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


if __name__ == "__main__":
    # build Qt GUI that allows to select file and displays image
    app = QtWidgets.QApplication(sys.argv)
    window = SplashScreenCreator()
    window.show()
    sys.exit(app.exec())
