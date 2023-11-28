from PySide6 import QtWidgets

from src.dialogs import base_dialog
from src.wme_widgets import wme_essentials
from src.utils import settings_manager


class AutoBackupDialog(base_dialog.BaseDialog):
    def __init__(self):
        self.auto_backup_frequency_combobox = wme_essentials.WMECombobox()
        self.auto_backup_count_spinbox = wme_essentials.WMESpinbox()
        self.auto_backup_while_running_checkbox = QtWidgets.QCheckBox()

        super().__init__()
        self.setWindowTitle("Auto-Backup Settings")

    def setup_ui(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(form_layout)

        self.auto_backup_frequency_combobox.addItem("Never", 0)
        self.auto_backup_frequency_combobox.addItem("Every 10 minutes", 10)
        self.auto_backup_frequency_combobox.addItem("Every 30 minutes", 30)
        self.auto_backup_frequency_combobox.addItem("Every hour", 60)
        self.auto_backup_frequency_combobox.addItem("Every 2 hours", 120)
        self.auto_backup_frequency_combobox.addItem("Every 24 hours", 1440)

        # TODO: get values from mod config
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
