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
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()

        save_action = tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.on_save)

        restore_action = tool_bar.addAction(icon_manager.load_icon("restore.png", COLORS.PRIMARY), "Reload File (F5)")
        restore_action.setShortcut("F5")
        restore_action.triggered.connect(self.on_restore)

        tool_bar.addSeparator()

        resize_layout = QtWidgets.QHBoxLayout()
        resize_layout.setContentsMargins(5, 0, 5, 0)

        resize_layout.addWidget(QtWidgets.QLabel("Width:"))
        self.width_spin_box.setRange(1, 9999)
        resize_layout.addWidget(self.width_spin_box)

        resize_layout.addWidget(QtWidgets.QLabel("Height:"))
        self.height_spin_box.setRange(1, 9999)
        resize_layout.addWidget(self.height_spin_box)

        resize_layout.addWidget(QtWidgets.QLabel("Keep Aspect Ratio:"))
        resize_layout.addWidget(self.ratio_check_box)

        resize_widget = QtWidgets.QWidget()
        resize_widget.setLayout(resize_layout)
        tool_bar.addWidget(resize_widget)

        main_layout.addWidget(tool_bar)
        main_layout.addStretch(1)

        self.img_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.img_preview.setMinimumSize(1, 1)
        self.img_preview.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        main_layout.addWidget(self.img_preview)
        main_layout.addStretch(1)

        self.help_file_path = "DontShow"

    def on_save(self):
        pixmap = self.img_preview.pixmap()
        pixmap.save(self.img_path)

    def on_restore(self):
        self.set_image(self.img_path)

    def set_image(self, image_path: str):
        self.img_size = QtGui.QImage(image_path).size()
        w = min(self.img_preview.width(), self.img_size.width())
        h = min(self.img_preview.height(), self.img_size.height())
        self.img_preview.setPixmap(QtGui.QPixmap(image_path).scaled(w, h, QtCore.Qt.KeepAspectRatio))
        self.img_path = image_path.replace("\\", "/")
        self.tab_name = self.img_path.split("/")[-1]
        self.unsaved_changes = False

    def resizeEvent(self, event):
        w = min(self.img_preview.width(), self.img_size.width())
        h = min(self.img_preview.height(), self.img_size.height())
        self.img_preview.setPixmap(QtGui.QPixmap(self.img_path).scaled(w, h, QtCore.Qt.KeepAspectRatio))
        super().resizeEvent(event)

    def to_json(self) -> dict:
        page_json = {"imagePath": self.img_path}
        return page_json

    def from_json(self, json_obj: dict):
        self.set_image(json_obj["imagePath"])
