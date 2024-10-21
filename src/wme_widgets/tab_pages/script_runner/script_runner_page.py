import sys
import importlib
import inspect
import os
import traceback

from PySide6 import QtWidgets, QtCore

from src.wme_widgets import wme_essentials, main_widget
from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets.tab_pages.script_runner import base_script
from src.utils import icon_manager, resource_loader, parser_utils
from src.utils.color_manager import *
from src.dialogs import exception_handler_dialog


class ScriptRunnerPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        self.files_to_save = {}

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.tool_bar = QtWidgets.QToolBar()
        self.main_layout.addWidget(self.tool_bar)

        run_action = self.tool_bar.addAction(icon_manager.load_icon("play.png", COLORS.PRIMARY),
                                             "Run Selected Script (Ctrl + F5)")
        run_action.setShortcut("Ctrl+F5")
        run_action.triggered.connect(self.run_script)

        self.script_selector = wme_essentials.WMECombobox()
        self.script_selector.currentIndexChanged.connect(lambda: self.on_new_script_selected(
            self.script_selector.currentData()))
        self.tool_bar.addWidget(self.script_selector)

        restore_action = self.tool_bar.addAction(icon_manager.load_icon("restore.png", COLORS.PRIMARY),
                                                 "Reload all scripts (F5)")
        restore_action.setShortcut("F5")
        restore_action.triggered.connect(self.update_page)

        import_location_action = self.tool_bar.addAction(icon_manager.load_icon("dir.png", COLORS.PRIMARY),
                                                         "Open the script import location in the file explorer")
        import_location_action.triggered.connect(self.open_script_dir)

        stretch = QtWidgets.QWidget()
        stretch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.tool_bar.addWidget(stretch)

        help_action = self.tool_bar.addAction(icon_manager.load_icon("help.png", COLORS.PRIMARY),
                                              "Open Page Help Popup (Alt + H)")
        help_action.triggered.connect(self.on_help)

        self.script_description_label = QtWidgets.QLabel()
        self.script_description_label.setWordWrap(True)
        self.main_layout.addWidget(self.script_description_label)

        self.parameter_layout = QtWidgets.QFormLayout()
        self.main_layout.addLayout(self.parameter_layout)

        self.main_layout.addStretch(1)

        self.scripts: [base_script.BaseScript] = []
        self.update_page()

        # TODO: write this
        self.help_page = "Help_ScriptRunner.md"

    def update_page(self):
        current_script_name = self.script_selector.currentText()
        self.import_scripts()
        if self.script_selector.findText(current_script_name) != -1:
            self.script_selector.setCurrentIndex(self.script_selector.findText(current_script_name))
        self.on_new_script_selected(self.script_selector.currentData())

    def on_new_script_selected(self, script: base_script.BaseScript):
        if script is None:
            return
        self.script_description_label.setText(script.description)
        # clear parameter layout
        while self.parameter_layout.rowCount() > 0:
            self.parameter_layout.removeRow(0)

        for param in script.parameters:
            label = QtWidgets.QLabel(param.name)
            label.setToolTip(param.description)

            match type(param.default_value).__qualname__:
                case int.__qualname__:
                    input_widget = wme_essentials.WMESpinbox()
                    input_widget.setValue(param.default_value)
                case float.__qualname__:
                    input_widget = wme_essentials.WMEDoubleSpinbox()
                    input_widget.setValue(param.default_value)
                case str.__qualname__:
                    input_widget = wme_essentials.WMELineEdit()
                    input_widget.setText(param.default_value)
                case bool.__qualname__:
                    input_widget = QtWidgets.QCheckBox()
                    input_widget.setChecked(param.default_value)
                case _:
                    input_widget = wme_essentials.WMELineEdit()
                    input_widget.setText(str(param.default_value))

            self.parameter_layout.addRow(label, input_widget)

    def import_scripts(self):
        self.scripts.clear()
        self.script_selector.clear()
        self.import_scripts_from_dir(resource_loader.get_resource_path("resources/scripts"))
        self.import_scripts_from_dir(resource_loader.get_persistant_path("Scripts"), external=True)
        for script in self.scripts:
            self.script_selector.addItem(script.name, script)

    def import_scripts_from_dir(self, dir_path, external: bool = False):
        for file in os.listdir(dir_path):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    # check if module with same name is already imported
                    if external:
                        module_name = file[:-3]
                    else:
                        module_name = "resources.scripts." + file[:-3]
                    if module_name not in sys.modules:
                        if external:
                            sys.path.append(dir_path)
                        importlib.import_module(module_name)
                    else:
                        importlib.reload(sys.modules[module_name])
                    # get classes from module
                    for name, obj in inspect.getmembers(sys.modules[module_name]):
                        if name == "BaseScript":
                            continue
                        if inspect.isclass(obj) and issubclass(obj, base_script.BaseScript):
                            script = obj()
                            script.page = self
                            self.scripts.append(script)
                            logging.info(f"Imported script {script.name} from {file}")
                except Exception as e:
                    logging.error(f"Failed to import script from {file}: {e}")

    def open_script_dir(self):
        # open explorer in script dir
        QtCore.QProcess.startDetached("explorer", [resource_loader.get_persistant_path("Scripts")])

    def get_parameter_values(self) -> dict:
        params = {}
        for i in range(self.parameter_layout.rowCount()):
            label = self.parameter_layout.itemAt(i, QtWidgets.QFormLayout.LabelRole).widget()
            input_widget = self.parameter_layout.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()
            match type(input_widget):
                case wme_essentials.WMESpinbox:
                    params[label.text()] = input_widget.value()
                case wme_essentials.WMEDoubleSpinbox:
                    params[label.text()] = input_widget.value()
                case wme_essentials.WMELineEdit:
                    params[label.text()] = input_widget.text()
                case QtWidgets.QCheckBox:
                    params[label.text()] = input_widget.isChecked()
                case _:
                    params[label.text()] = input_widget.text()
        return params

    def run_script(self):
        script = self.script_selector.currentData()
        main_widget.instance.show_loading_screen(f"Running script {script.name}...")
        try:
            t = main_widget.instance.run_worker_thread(script.run, self.get_parameter_values())
            self.files_to_save = main_widget.instance.wait_for_worker_thread(t)
            for file in self.files_to_save.keys():
                full_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file)
                self.file_paths.add(full_path)
                self.unsaved_changes = True
            self.save_changes()
        except Exception as e:
            logging.error(f"Failed to run script {script.name}: {e}")
            logging.error(traceback.format_exc())
            dialog = exception_handler_dialog.ExceptionHandlerDialog()
            dialog.set_exception(type(e), e, traceback.format_exc())
            info_text = f"An error occurred while trying to run {script.name}."
            dialog.set_info_text(info_text)
            dialog.exec_()
        main_widget.instance.hide_loading_screen()

    def _save_changes(self) -> bool:
        try:
            for file in self.files_to_save.keys():
                text = parser_utils.get_text_from_ndf_obj(self.files_to_save[file])
                full_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file)
                with open(full_path, "w") as f:
                    f.write(text)
        except Exception as e:
            logging.error("Error while saving script files: " + str(e))
            return False
        return True

    def to_json(self) -> dict:
        return {
            "script": self.script_selector.currentData().name,
        }

    def from_json(self, data: dict):
        for i in range(self.script_selector.count()):
            if self.script_selector.itemText(i) == data["script"]:
                self.script_selector.setCurrentIndex(i)
                break
        self.on_new_script_selected(self.script_selector.currentData())
