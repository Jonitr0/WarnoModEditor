from PySide6 import QtWidgets

from src.dialogs import base_dialog
from src.wme_widgets import wme_essentials, main_widget
from src.utils import settings_manager


def get_mod_settings():
    try:
        app_state = settings_manager.get_settings_value(settings_manager.APP_STATE)
        mod_state = app_state[main_widget.instance.get_loaded_mod_name()]
        return mod_state
    except Exception:
        return {}


def set_mod_settings(mod_state):
    app_state = settings_manager.get_settings_value(settings_manager.APP_STATE)
    app_state[main_widget.instance.get_loaded_mod_name()] = mod_state
    settings_manager.write_settings_value(settings_manager.APP_STATE, app_state)


class AutoBackupDialog(base_dialog.BaseDialog):
    def __init__(self):
        self.auto_backup_frequency_combobox = wme_essentials.WMECombobox()
        self.auto_backup_count_spinbox = wme_essentials.WMESpinbox()

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

        try:
            mod_state = get_mod_settings()
            val = int(mod_state[settings_manager.AUTO_BACKUP_FREQUENCY_KEY])
            self.auto_backup_frequency_combobox.setCurrentIndex(self.auto_backup_frequency_combobox.findData(val))
        except Exception:
            val = int(settings_manager.get_settings_value(settings_manager.AUTO_BACKUP_FREQUENCY_KEY))
            if not val:
                val = 60
                settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_FREQUENCY_KEY, val)
            self.auto_backup_frequency_combobox.setCurrentIndex(self.auto_backup_frequency_combobox.findData(val))

        form_layout.addRow("Frequency:", self.auto_backup_frequency_combobox)

        try:
            mod_state = get_mod_settings()
            val = int(mod_state[settings_manager.AUTO_BACKUP_COUNT_KEY])
            self.auto_backup_count_spinbox.setValue(val)
        except Exception:
            val = int(settings_manager.get_settings_value(settings_manager.AUTO_BACKUP_COUNT_KEY))
            if not val:
                val = 3
                settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_COUNT_KEY, val)
            self.auto_backup_count_spinbox.setValue(val)

        self.auto_backup_count_spinbox.setMinimum(1)
        self.auto_backup_count_spinbox.setMaximum(100)
        form_layout.addRow("Maximum number of backups:", self.auto_backup_count_spinbox)

    def accept(self) -> None:
        mod_state = get_mod_settings()
        mod_state[settings_manager.AUTO_BACKUP_FREQUENCY_KEY] = self.auto_backup_frequency_combobox.currentData()
        mod_state[settings_manager.AUTO_BACKUP_COUNT_KEY] = self.auto_backup_count_spinbox.value()
        set_mod_settings(mod_state)

        super().accept()
