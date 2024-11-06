import os

from PySide6 import QtWidgets, QtGui

from src.dialogs import base_dialog
from src.wme_widgets import wme_essentials, main_widget


class AddIconDialog(base_dialog.BaseDialog):
    def __init__(self):
        self.origin_line_edit = wme_essentials.WMELineEdit()
        self.destination_line_edit = wme_essentials.WMELineEdit()
        self.img_preview = QtWidgets.QLabel()
        self.height_spin_box = wme_essentials.WMESpinbox()
        self.width_spin_box = wme_essentials.WMESpinbox()
        self.ratio_check_box = QtWidgets.QCheckBox()
        self.original_size_label = QtWidgets.QLabel()
        self.original_height = -1
        self.original_width = -1
        super().__init__()

        self.setWindowTitle("Add Image")

    def setup_ui(self):
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(h_layout)

        self.img_preview.setFixedSize(256, 256)
        self.img_preview.setObjectName("img_preview")
        # TODO: center image
        h_layout.addWidget(self.img_preview)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addLayout(form_layout)

        origin_widget = QtWidgets.QWidget()
        origin_layout = QtWidgets.QHBoxLayout()
        origin_layout.setContentsMargins(0, 0, 0, 0)
        origin_widget.setLayout(origin_layout)
        self.origin_line_edit.setMinimumWidth(300)
        self.origin_line_edit.textChanged.connect(self.on_origin_text_changed)
        origin_layout.addWidget(self.origin_line_edit)

        origin_button = QtWidgets.QPushButton("Browse..")
        origin_button.clicked.connect(self.on_origin_button_clicked)
        origin_layout.addWidget(origin_button)

        form_layout.addRow("Origin:", origin_widget)

        destination_widget = QtWidgets.QWidget()
        destination_layout = QtWidgets.QHBoxLayout()
        destination_layout.setContentsMargins(0, 0, 0, 0)
        destination_widget.setLayout(destination_layout)
        self.destination_line_edit.setMinimumWidth(300)
        destination_layout.addWidget(self.destination_line_edit)

        destination_button = QtWidgets.QPushButton("Browse..")
        destination_button.clicked.connect(self.on_destination_button_clicked)
        destination_layout.addWidget(destination_button)

        form_layout.addRow("Destination:", destination_widget)

        self.width_spin_box.setRange(0, 4096)
        self.width_spin_box.valueChanged.connect(self.on_width_spin_box_value_changed)
        form_layout.addRow("Width:", self.width_spin_box)
        self.height_spin_box.setRange(0, 4096)
        self.height_spin_box.valueChanged.connect(self.on_height_spin_box_value_changed)
        form_layout.addRow("Height:", self.height_spin_box)

        self.ratio_check_box.setChecked(True)
        self.ratio_check_box.stateChanged.connect(self.on_toggle_aspect)
        form_layout.addRow("Keep Original Aspect Ratio:", self.ratio_check_box)

        size_widget = QtWidgets.QWidget()
        size_layout = QtWidgets.QHBoxLayout()
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.addWidget(self.original_size_label)
        size_widget.setLayout(size_layout)
        size_layout.addStretch(1)
        reset_size_button = QtWidgets.QPushButton("Reset Size")
        reset_size_button.clicked.connect(self.on_reset_size)
        size_layout.addWidget(reset_size_button)
        form_layout.addRow("Original Size:", size_widget)

        # TODO: add common icon sizes with buttons to choose from

    def on_origin_button_clicked(self):
        path = os.path.expanduser("~\\Pictures")
        if os.path.exists(self.origin_line_edit.text()):
            path = self.origin_line_edit.text()
        img_path = QtWidgets.QFileDialog().getOpenFileName(self, "Select Image",
                                                           path,
                                                           "Image Files (*.png *.jpg *.bmp)")[0]
        if img_path == "":
            return
        self.origin_line_edit.setText(img_path)

    def on_origin_text_changed(self, text: str):
        image_loaded = self.load_preview(text, False)
        if image_loaded:
            self.set_width_no_signal(self.original_width)
            self.set_height_no_signal(self.original_height)

    def on_destination_button_clicked(self):
        path = main_widget.instance.get_loaded_mod_path()
        if os.path.exists(self.destination_line_edit.text()):
            path = self.destination_line_edit.text()
        img_path = QtWidgets.QFileDialog().getSaveFileName(self, "Select Saving Location",
                                                           path,
                                                           "PNG Files (*.png)")[0]
        if img_path == "":
            return
        self.destination_line_edit.setText(img_path)

    def on_width_spin_box_value_changed(self, value: int):
        if self.ratio_check_box.isChecked():
            self.set_height_no_signal(int(float(value) / self.get_original_aspect_ratio()))
        self.load_preview(self.origin_line_edit.text())

    def on_height_spin_box_value_changed(self, value: int):
        if self.ratio_check_box.isChecked():
            self.set_width_no_signal(int(float(value) * self.get_original_aspect_ratio()))
        self.load_preview(self.origin_line_edit.text())

    def on_reset_size(self):
        self.width_spin_box.setValue(self.original_width)
        self.height_spin_box.setValue(self.original_height)

    def get_original_aspect_ratio(self):
        return self.original_width / self.original_height

    def on_toggle_aspect(self, keep_aspect):
        if keep_aspect != 0:
            self.on_width_spin_box_value_changed(self.width_spin_box.value())

    def set_width_no_signal(self, w: int):
        self.width_spin_box.valueChanged.disconnect(self.on_width_spin_box_value_changed)
        self.width_spin_box.setValue(w)
        self.width_spin_box.valueChanged.connect(self.on_width_spin_box_value_changed)

    def set_height_no_signal(self, h: int):
        self.height_spin_box.valueChanged.disconnect(self.on_height_spin_box_value_changed)
        self.height_spin_box.setValue(h)
        self.height_spin_box.valueChanged.connect(self.on_height_spin_box_value_changed)

    def load_preview(self, path: str, scale: bool = True):
        if not os.path.exists(path):
            self.set_width_no_signal(0)
            self.set_height_no_signal(0)
            self.original_size_label.setText("")
            self.img_preview.setPixmap(QtGui.QPixmap())
            print(f"path {path} does not exist")
            return False
        try:
            image = QtGui.QImage(path)
        except Exception as e:
            self.set_width_no_signal(0)
            self.set_height_no_signal(0)
            self.original_size_label.setText("")
            self.img_preview.setPixmap(QtGui.QPixmap())
            print(e)
            return False
        self.original_width = image.width()
        self.original_height = image.height()
        self.original_size_label.setText(f"{self.original_width}x{self.original_height}")
        if scale:
            image = image.smoothScaled(self.width_spin_box.value(), self.height_spin_box.value())
        if image.width() >= image.height() and image.width() > self.img_preview.width():
            image = image.scaledToWidth(self.img_preview.width())
        elif image.width() < image.height() and image.height() > self.img_preview.height():
            image = image.scaledToHeight(self.img_preview.height())
        self.img_preview.setPixmap(QtGui.QPixmap(image))
        return True

    def accept(self):
        # TODO: check if origin and destination are valid
        # TODO: save image from origin as png with selected size
        super().accept()
