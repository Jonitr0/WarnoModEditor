# TODO: copy icon to preferred location
# TODO: scale and preview icon
# TODO: convert to png
from PySide6 import QtWidgets

from src.dialogs import base_dialog
from src.wme_widgets import wme_essentials


class AddIconDialog(base_dialog.BaseDialog):
    def __init__(self):
        self.origin_line_edit = wme_essentials.WMELineEdit()
        self.destination_line_edit = wme_essentials.WMELineEdit()
        self.img_preview = QtWidgets.QLabel()
        self.height_spin_box = wme_essentials.WMESpinbox()
        self.width_spin_box = wme_essentials.WMESpinbox()
        self.ratio_check_box = QtWidgets.QCheckBox()
        super().__init__()

        self.setWindowTitle("Add Image")

    def setup_ui(self):
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(h_layout)

        self.img_preview.setFixedSize(200, 200)
        self.img_preview.setObjectName("img_preview")
        h_layout.addWidget(self.img_preview)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addLayout(form_layout)

        origin_widget = QtWidgets.QWidget()
        origin_layout = QtWidgets.QHBoxLayout()
        origin_layout.setContentsMargins(0, 0, 0, 0)
        origin_widget.setLayout(origin_layout)
        self.origin_line_edit.setMinimumWidth(300)
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
        form_layout.addRow("Keep Aspect Ratio:", self.ratio_check_box)

    def on_origin_button_clicked(self):
        pass

    def on_destination_button_clicked(self):
        pass

    def on_width_spin_box_value_changed(self, value: int):
        pass

    def on_height_spin_box_value_changed(self, value: int):
        pass
