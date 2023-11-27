from PySide6 import QtWidgets

from src.dialogs.base_dialog import BaseDialog
from src.dialogs import essential_dialogs
from src.utils import path_validator, settings_manager
from src.utils import theme_manager
from src.wme_widgets import main_widget
from src.wme_widgets import wme_essentials


class OptionsDialog(BaseDialog):
    def __init__(self):
        self.color_combobox = wme_essentials.WMECombobox()
        self.theme_checkbox = QtWidgets.QCheckBox()
        self.path_line_edit = wme_essentials.WMELineEdit()

        self.auto_backup_frequency_combobox = wme_essentials.WMECombobox()
        self.auto_backup_count_spinbox = wme_essentials.WMESpinbox()
        self.auto_backup_while_running_checkbox = QtWidgets.QCheckBox()

        super().__init__()
        self.setWindowTitle("Options")

    def setup_ui(self):
        form_layout = QtWidgets.QFormLayout()
        self.main_layout.addLayout(form_layout)

        color_list = theme_manager.get_all_themes()
        color_list = color_list[:len(color_list) // 2]
        for i in range(len(color_list)):
            color_list[i] = color_list[i].removeprefix("dark ")

        self.color_combobox.addItems(color_list)

        theme = settings_manager.get_settings_value(settings_manager.THEME_KEY)
        if theme.startswith("dark"):
            self.theme_checkbox.setChecked(True)
        else:
            self.theme_checkbox.setChecked(False)
        self.color_combobox.setCurrentText(theme[theme.index(" ") + 1:])

        form_layout.addRow("Dark Theme:", self.theme_checkbox)
        form_layout.addRow("Accent Color:", self.color_combobox)
        form_layout.addWidget(
            QtWidgets.QLabel("Changes to the theme will be applied when the application is restarted."))

        warno_path_layout = QtWidgets.QHBoxLayout()
        self.path_line_edit.setText(main_widget.instance.get_warno_path())
        warno_path_layout.addWidget(self.path_line_edit)
        browse_button = QtWidgets.QPushButton("Browse..")
        browse_button.clicked.connect(self.on_browse_clicked)
        warno_path_layout.addWidget(browse_button)
        form_layout.addRow("WARNO path:", warno_path_layout)

        auto_backup_label = QtWidgets.QLabel("Auto-Backup default settings")
        auto_backup_label.setObjectName("heading")
        form_layout.addRow(auto_backup_label)

        self.auto_backup_frequency_combobox.addItem("Never", 0)
        self.auto_backup_frequency_combobox.addItem("Every 10 minutes", 10)
        self.auto_backup_frequency_combobox.addItem("Every 30 minutes", 30)
        self.auto_backup_frequency_combobox.addItem("Every hour", 60)
        self.auto_backup_frequency_combobox.addItem("Every 2 hours", 120)
        self.auto_backup_frequency_combobox.addItem("Every 24 hours", 1440)

        try:
            val = int(settings_manager.get_settings_value(settings_manager.AUTO_BACKUP_FREQUENCY_KEY))
            self.auto_backup_frequency_combobox.setCurrentIndex(self.auto_backup_frequency_combobox.findData(val))
        except Exception:
            settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_FREQUENCY_KEY, 60)
            self.auto_backup_frequency_combobox.setCurrentIndex(self.auto_backup_frequency_combobox.findData(60))

        form_layout.addRow("Frequency:", self.auto_backup_frequency_combobox)

        try:
            val = int(settings_manager.get_settings_value(settings_manager.AUTO_BACKUP_COUNT_KEY))
            self.auto_backup_count_spinbox.setValue(val)
        except Exception:
            settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_COUNT_KEY, 3)
            self.auto_backup_count_spinbox.setValue(3)

        self.auto_backup_count_spinbox.setMinimum(1)
        self.auto_backup_count_spinbox.setMaximum(100)
        form_layout.addRow("Maximum number of backups:", self.auto_backup_count_spinbox)

        form_layout.addRow("Auto-Backup while running:", self.auto_backup_while_running_checkbox)
        form_layout.addWidget(QtWidgets.QLabel("If checked, auto-backups will be created while WME is running.\n"
                                               "If unchecked, auto-backups will only be created when WME is closed."))

        try:
            val = int(settings_manager.get_settings_value(settings_manager.AUTO_BACKUP_WHILE_RUNNING_KEY))
            self.auto_backup_while_running_checkbox.setChecked(bool(val))
        except Exception:
            settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_WHILE_RUNNING_KEY, 0)
            self.auto_backup_while_running_checkbox.setChecked(False)

    def on_browse_clicked(self):
        warno_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter WARNO path", self.path_line_edit.text(),
                                                                  options=(QtWidgets.QFileDialog.ShowDirsOnly |
                                                                           QtWidgets.QFileDialog.ReadOnly))
        self.path_line_edit.setText(warno_path)

    def accept(self):
        warno_path = self.path_line_edit.text()
        if not path_validator.validate_warno_path(warno_path):
            essential_dialogs.MessageDialog("Path invalid",
                                            "The WARNO path appears to be invalid. "
                                            "Please enter the correct path.").exec()
            return

        settings_manager.write_settings_value(settings_manager.WARNO_PATH_KEY, warno_path)
        main_widget.instance.set_warno_path(warno_path)

        theme = "light "
        if self.theme_checkbox.isChecked():
            theme = "dark "
        theme += str(self.color_combobox.currentText())
        settings_manager.write_settings_value(settings_manager.NEXT_THEME_KEY, theme)

        settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_FREQUENCY_KEY,
                                              self.auto_backup_frequency_combobox.currentData())
        settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_COUNT_KEY,
                                              self.auto_backup_count_spinbox.value())
        settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_WHILE_RUNNING_KEY,
                                              1 if self.auto_backup_while_running_checkbox.isChecked() else 0)

        super().accept()
