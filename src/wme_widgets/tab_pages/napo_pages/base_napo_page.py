# provides common functionality for Napo Tool Pages
import os
import json

from PySide6 import QtWidgets, QtGui

from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import main_widget

from src.utils import icon_manager, resource_loader, parser_utils
from src.utils.color_manager import *
from src.dialogs import essential_dialogs


class BaseNapoPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        self.saved_state = None

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.tool_bar = QtWidgets.QToolBar()
        self.main_layout.addWidget(self.tool_bar)

        save_action = self.tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        restore_icon = QtGui.QIcon()
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)

        self.restore_action = self.tool_bar.addAction(restore_icon, "Discard changes and restore page (F5)")
        self.restore_action.setShortcut("F5")
        self.restore_action.triggered.connect(self.on_restore)

        self.tool_bar.addSeparator()

        import_state_action = self.tool_bar.addAction(icon_manager.load_icon("import.png", COLORS.PRIMARY),
                                                      "Import configuration from file (Ctrl + I)")
        import_state_action.setShortcut("Ctrl+I")
        import_state_action.triggered.connect(self.import_state)

        export_state_action = self.tool_bar.addAction(icon_manager.load_icon("export.png", COLORS.PRIMARY),
                                                      "Export configuration to file (Ctrl + E)")
        export_state_action.setShortcut("Ctrl+E")
        export_state_action.triggered.connect(self.export_state)

    def _save_changes(self) -> bool:
        state = self.get_state()
        self.write_state_to_file(state)
        self.saved_state = state
        return True

    def write_state_to_file(self, state: dict):
        pass

    def load_state_from_file(self) -> dict:
        pass

    def update_page(self):
        main_widget.instance.show_loading_screen("loading data form .ndf files...")
        t = main_widget.instance.run_worker_thread(self.load_state_from_file)
        state = main_widget.instance.wait_for_worker_thread(t)
        self.saved_state = state
        self.set_state(state)
        main_widget.instance.hide_loading_screen()

    def get_parsed_ndf_file(self, file_name: str, editing: bool = True):
        mod_path = main_widget.instance.get_loaded_mod_path()
        file_path = os.path.join(mod_path, file_name)

        if editing:
            self.open_file(file_path)

        return parser_utils.get_parsed_ndf_file(file_path)

    def get_parsed_object_from_ndf_file(self, file_name: str, obj_name: str, editing: bool = True):
        mod_path = main_widget.instance.get_loaded_mod_path()
        file_path = os.path.join(mod_path, file_name)

        if editing:
            self.open_file(file_path)

        file_obj = self.get_parsed_ndf_file(file_name)
        for row in file_obj:
            if row.namespace == obj_name:
                return row.value

        logging.warning("Object " + obj_name + " not found in " + file_name)
        return None

    def save_files_to_mod(self, files_to_objs: dict):
        mod_path = main_widget.instance.get_loaded_mod_path()

        files = files_to_objs.keys()

        for file in files:
            text = parser_utils.get_text_from_ndf_obj(files_to_objs[file])
            file_path = os.path.join(mod_path, file)
            with open(file_path, "w") as f:
                f.write(text)

    def on_restore(self):
        if self.unsaved_changes:
            dialog = essential_dialogs.ConfirmationDialog("Your changes will be discarded! Are you sure?", "Warning!")
            if not dialog.exec():
                return
        self.update_page()

    def add_help_button(self):
        stretch = QtWidgets.QWidget()
        stretch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.tool_bar.addWidget(stretch)

        help_action = self.tool_bar.addAction(icon_manager.load_icon("help.png", COLORS.PRIMARY),
                                              "Open Page Help Popup (Alt + H)")
        help_action.triggered.connect(self.on_help)

    def get_state(self) -> dict:
        return {}

    def set_state(self, state: dict):
        pass

    def on_state_changed(self):
        self.unsaved_changes = self.saved_state != self.get_state()

    def import_state(self):
        if self.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog(self.tab_name)
            if not dialog.exec():
                return

            if dialog.save_changes:
                if not self.save_changes():
                    return

        current_state = self.get_state()
        try:
            file_name = resource_loader.get_persistant_path("")
            file_path, ret = QtWidgets.QFileDialog().getOpenFileName(self, "Select config file", file_name,
                                                                     options=QtWidgets.QFileDialog.ReadOnly,
                                                                     filter="*.txt")
            if not ret:
                return

            main_widget.instance.show_loading_screen("Importing state...")

            state = json.load(open(file_path, "r"))
            try:
                self.set_state(state)
            except Exception:
                essential_dialogs.MessageDialog("Error", "Could not import state. The file might be incompatible "
                                                         "with " + self.tab_name).exec()
                self.set_state(current_state)
        except Exception as e:
            logging.error("Error while loading config for " + str(self.__class__) + ":" + str(e))
            self.set_state(current_state)

        main_widget.instance.hide_loading_screen()

    def export_state(self):
        try:
            state = self.get_state()
            state["version"] = settings_manager.get_settings_value(settings_manager.VERSION_KEY)
            file_name = resource_loader.get_persistant_path(self.get_state_file_name())
            file_path, ret = QtWidgets.QFileDialog().getSaveFileName(self, "Select export file name", file_name,
                                                                     options=QtWidgets.QFileDialog.ReadOnly,
                                                                     filter="*.txt")
            if not ret:
                return

            json.dump(state, open(file_path, "w"), indent=4)
        except Exception as e:
            logging.error("Error while exporting config on " + str(self.__class__) + ":" + str(e))

    def get_state_file_name(self) -> str:
        return ""
