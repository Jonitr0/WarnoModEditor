from PySide2 import QtWidgets

from dialogs.base_dialog import BaseDialog
from utils import theme_manager, path_validator, settings_manager
from wme_widgets import main_widget


class OptionsDialog(BaseDialog):
    def __init__(self):
        self.theme_combobox = QtWidgets.QComboBox()
        self.path_line_edit = QtWidgets.QLineEdit()

        super().__init__()
        self.setWindowTitle("Options")

    def setup_ui(self):
        form_layout = QtWidgets.QFormLayout()
        self.main_layout.addLayout(form_layout)

        self.theme_combobox.addItems(theme_manager.get_all_themes())
        self.theme_combobox.setCurrentText(settings_manager.get_settings_value(settings_manager.THEME_KEY))
        form_layout.addRow("Theme:", self.theme_combobox)
        form_layout.addWidget(
            QtWidgets.QLabel("Changes to the theme will be applied when the application is restarted."))

        warno_path_layout = QtWidgets.QHBoxLayout()
        self.path_line_edit.setText(main_widget.MainWidget.instance.get_warno_path())
        warno_path_layout.addWidget(self.path_line_edit)
        browse_button = QtWidgets.QPushButton("Browse..")
        browse_button.clicked.connect(self.on_browse_clicked)
        warno_path_layout.addWidget(browse_button)
        form_layout.addRow("WARNO path:", warno_path_layout)

    def on_browse_clicked(self):
        warno_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter WARNO path", self.path_line_edit.text())
        self.path_line_edit.setText(warno_path)

    def accept(self):
        warno_path = self.path_line_edit.text()
        if not path_validator.validate_warno_path(warno_path):
            QtWidgets.QMessageBox().information(QtWidgets.QWidget(), "Path invalid",
                                                "The WARNO path appears to be invalid. "
                                                "Please enter the correct path.")
            return

        settings_manager.write_settings_value(settings_manager.WARNO_PATH_KEY, warno_path)
        main_widget.MainWidget.instance.set_warno_path(warno_path)
        settings_manager.write_settings_value(settings_manager.THEME_KEY, str(self.theme_combobox.currentText()))

        super().accept()