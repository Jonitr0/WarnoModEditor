from PySide6 import QtWidgets, QtCore, QtGui

from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import wme_essentials
from src.utils.color_manager import *
from src.utils import icon_manager


class ImgPreviewPage(base_tab_page.BaseTabPage):
    def __init__(self):
        self.img_preview = QtWidgets.QLabel()
        self.width_spin_box = wme_essentials.WMESpinbox()
        self.height_spin_box = wme_essentials.WMESpinbox()
        self.ratio_check_box = QtWidgets.QCheckBox()

        super().__init__()
        self.img_path = ""
        self.img_size = QtCore.QSize()
        self.saved_size = QtCore.QSize()
        self.original_aspect_ratio = 1.0
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()

        save_action = tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        restore_action = tool_bar.addAction(icon_manager.load_icon("restore.png", COLORS.PRIMARY), "Reload File (F5)")
        restore_action.setShortcut("F5")
        restore_action.triggered.connect(self.on_restore)

        tool_bar.addSeparator()

        resize_layout = QtWidgets.QHBoxLayout()
        resize_layout.setContentsMargins(5, 0, 5, 0)

        resize_layout.addWidget(QtWidgets.QLabel("Width:"))
        self.width_spin_box.setRange(1, 9999)
        self.width_spin_box.valueChanged.connect(self.on_width_changed)
        resize_layout.addWidget(self.width_spin_box)

        resize_layout.addWidget(QtWidgets.QLabel("Height:"))
        self.height_spin_box.setRange(1, 9999)
        self.height_spin_box.valueChanged.connect(self.on_height_changed)
        resize_layout.addWidget(self.height_spin_box)

        resize_layout.addWidget(QtWidgets.QLabel("Keep Original Aspect Ratio:"))
        self.ratio_check_box.setChecked(True)
        resize_layout.addWidget(self.ratio_check_box)

        resize_widget = QtWidgets.QWidget()
        resize_widget.setLayout(resize_layout)
        tool_bar.addWidget(resize_widget)

        main_layout.addWidget(tool_bar)

        self.img_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.img_preview.setMinimumSize(1, 1)
        self.img_preview.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        main_layout.addWidget(self.img_preview)
        print(self.img_preview.size())

        self.help_file_path = "DontShow"

    def _save_changes(self):
        pixmap = self.img_preview.pixmap()
        pixmap.save(self.img_path)
        self.saved_size = self.img_size

    def on_restore(self):
        self.set_image(self.img_path)

    def on_width_changed(self, value: int):
        if value == self.img_size.width():
            return
        self.img_size.setWidth(value)
        if self.ratio_check_box.isChecked():
            self.img_size.setHeight(int(value / self.original_aspect_ratio))
            self.height_spin_box.setValue(self.img_size.height())
        self.img_preview.setPixmap(QtGui.QPixmap(self.img_path).scaled(self.img_size))
        self.unsaved_changes = self.img_size == self.saved_size
        self.check_img_preview_size()

    def on_height_changed(self, value: int):
        if value == self.img_size.height():
            return
        self.img_size.setHeight(value)
        if self.ratio_check_box.isChecked():
            self.img_size.setWidth(int(value * self.original_aspect_ratio))
            self.width_spin_box.setValue(self.img_size.width())
        self.img_preview.setPixmap(QtGui.QPixmap(self.img_path).scaled(self.img_size))
        self.unsaved_changes = self.img_size == self.saved_size
        self.check_img_preview_size()

    def set_image(self, image_path: str):
        self.img_size = QtGui.QImage(image_path).size()
        self.saved_size = self.img_size
        self.original_aspect_ratio = self.img_size.width() / self.img_size.height()

        self.width_spin_box.blockSignals(True)
        self.width_spin_box.setValue(self.img_size.width())
        self.width_spin_box.blockSignals(False)
        self.height_spin_box.blockSignals(True)
        self.height_spin_box.setValue(self.img_size.height())
        self.height_spin_box.blockSignals(False)

        self.img_preview.setPixmap(QtGui.QPixmap(image_path).scaled(self.saved_size))
        self.img_path = image_path.replace("\\", "/")
        self.tab_name = self.img_path.split("/")[-1]
        self.unsaved_changes = False
        self.check_img_preview_size()

    def resizeEvent(self, event):
        self.check_img_preview_size()
        super().resizeEvent(event)

    def check_img_preview_size(self):
        # make sure image preview is not larger than the label
        if self.img_size.width() > self.img_preview.width():
            self.img_preview.setPixmap(QtGui.QPixmap(self.img_path).scaledToWidth(self.img_preview.width()))
        if self.img_size.height() > self.img_preview.height():
            self.img_preview.setPixmap(QtGui.QPixmap(self.img_path).scaledToHeight(self.img_preview.height()))

    def to_json(self) -> dict:
        page_json = {"imagePath": self.img_path}
        return page_json

    def from_json(self, json_obj: dict):
        self.set_image(json_obj["imagePath"])
