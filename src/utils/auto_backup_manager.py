from PySide6 import QtCore

from src.utils import settings_manager, mod_settings_loader

import datetime
import os
import logging

WME_AUTO_BACKUP_PREFIX = "wme_auto_backup_"


class AutoBackupManager(QtCore.QObject):
    request_backup = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.auto_backup_frequency = 60
        self.auto_backup_count = 3

        self.update_settings()

        settings_manager.SettingsChangedNotifier.instance.mod_state_changed.connect(self.on_mod_state_changed)
        settings_manager.SettingsChangedNotifier.instance.app_state_saved.connect(self.update_settings)

    def update_settings(self):
        try:
            mod_state = mod_settings_loader.get_mod_settings()
            val = int(mod_state[settings_manager.AUTO_BACKUP_FREQUENCY_KEY])
            self.auto_backup_frequency = val
        except Exception:
            val = settings_manager.get_settings_value(settings_manager.AUTO_BACKUP_FREQUENCY_KEY)
            if not val:
                val = 60
                settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_FREQUENCY_KEY, val)
            else:
                val = int(val)
            self.auto_backup_frequency = val

        try:
            mod_state = mod_settings_loader.get_mod_settings()
            val = int(mod_state[settings_manager.AUTO_BACKUP_COUNT_KEY])
            self.auto_backup_count = val
        except Exception:
            val = settings_manager.get_settings_value(settings_manager.AUTO_BACKUP_COUNT_KEY)
            if not val:
                val = 3
                settings_manager.write_settings_value(settings_manager.AUTO_BACKUP_COUNT_KEY, val)
            else:
                val = int(val)
            self.auto_backup_count = val
            
    def on_mod_state_changed(self, changed: bool):
        if not changed:
            return

        mod_state = mod_settings_loader.get_mod_settings()
        if not mod_state:
            mod_state = {}
        last_backup = mod_state.get(settings_manager.LAST_AUTO_BACKUP_KEY, None)

        if not last_backup:
            self.backup()
            return

        # create time from last backup string
        last_backup_time = datetime.datetime.strptime(last_backup, "%Y%m%d%H%M")

        # add frequency to last backup time
        next_backup_time = last_backup_time + datetime.timedelta(minutes=self.auto_backup_frequency)

        # get current time
        current_time = datetime.datetime.now()

        if current_time > next_backup_time:
            self.backup()

    def backup(self):
        self.parent().show_loading_screen("Auto-backup in progress...")

        backup_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        backup_name = WME_AUTO_BACKUP_PREFIX + backup_time

        self.request_backup.emit(backup_name)
        logging.info("Auto-backup created: " + backup_name + ".zip")

        # list all backups
        backup_dir = os.path.join(self.parent().get_loaded_mod_path(), "Backup")
        backups = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))
                   and f.startswith(WME_AUTO_BACKUP_PREFIX) and f.endswith(".zip")]

        # sort by name
        backups.sort()

        # delete oldest backups
        while len(backups) > self.auto_backup_count:
            os.remove(os.path.join(backup_dir, backups[0]))
            logging.info("Auto-backup deleted: " + backups[0])
            backups.pop(0)

        mod_state = mod_settings_loader.get_mod_settings()
        if not mod_state:
            mod_state = {}
        mod_state[settings_manager.LAST_AUTO_BACKUP_KEY] = backup_time
        mod_settings_loader.set_mod_settings(mod_state)

        self.parent().hide_loading_screen()
