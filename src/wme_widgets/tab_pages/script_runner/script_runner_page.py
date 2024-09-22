import sys
import importlib
import inspect
import os

from PySide6 import QtWidgets, QtCore

from src.wme_widgets import wme_essentials
from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets.tab_pages.script_runner import base_script
from src.utils import icon_manager, resource_loader
from src.utils.color_manager import *


class ScriptRunnerPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.tool_bar = QtWidgets.QToolBar()
        self.main_layout.addWidget(self.tool_bar)

        run_action = self.tool_bar.addAction(icon_manager.load_icon("play.png", COLORS.PRIMARY),
                                             "Run Selected Script (Ctrl + F5)")
        run_action.setShortcut("Ctrl+F5")
        run_action.triggered.connect(self.run_script)

        # define import location, automatically import from there
        # add script objects as data
        self.script_selector = wme_essentials.WMECombobox()
        self.tool_bar.addWidget(self.script_selector)

        # TODO: restore action
        # TODO: action that opens import location in explorer

        restore_action = self.tool_bar.addAction(icon_manager.load_icon("restore.png", COLORS.PRIMARY),
                                                 "Discard changes and restore page (F5)")
        restore_action.setShortcut("F5")
        restore_action.triggered.connect(self.update_page)

        import_location_action = self.tool_bar.addAction(icon_manager.load_icon("dir.png", COLORS.PRIMARY),
                                                         "Open the script import location in the file explorer")
        import_location_action.triggered.connect(self.open_script_dir)

        self.script_description_label = QtWidgets.QLabel("This will display the description of the selected script")
        self.main_layout.addWidget(self.script_description_label)

        self.parameter_layout = QtWidgets.QFormLayout()
        self.main_layout.addLayout(self.parameter_layout)

        self.main_layout.addStretch(1)

        self.scripts: [base_script.BaseScript] = []
        self.update_page()

    def update_page(self):
        self.import_scripts()
        # TODO: reset to default parameters

    def on_new_script_selected(self, script: base_script.BaseScript):
        # clear parameter layout
        for i in reversed(range(self.parameter_layout.count())):
            widget_to_remove = self.parameter_layout.itemAt(i).widget()
            self.parameter_layout.removeWidget(widget_to_remove)
            if widget_to_remove:
                widget_to_remove.setParent(None)

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
        self.import_scripts_from_dir(resource_loader.get_persistant_path("Scripts"))
        for script in self.scripts:
            self.script_selector.addItem(script.name, script)

    def import_scripts_from_dir(self, dir_path):
        for file in os.listdir(dir_path):
            if file.endswith(".py") and file != "__init__.py":
                try:
                    # check if module with same name is already imported
                    module_name = "resources.scripts." + file[:-3]
                    if module_name not in sys.modules:
                        importlib.import_module(module_name)
                    else:
                        importlib.reload(sys.modules[module_name])
                    # get classes from module
                    for name, obj in inspect.getmembers(sys.modules[module_name]):
                        if inspect.isclass(obj) and issubclass(obj, base_script.BaseScript):
                            script = obj()
                            self.scripts.append(script)
                            logging.info(f"Imported script {script.name} from {file}")
                except Exception as e:
                    logging.error(f"Failed to import script from {file}: {e}")

    def open_script_dir(self):
        # open explorer in script dir
        QtCore.QProcess.startDetached("explorer", [resource_loader.get_persistant_path("Scripts")])

    def get_parameter_values(self) -> dict:
        # make this return names to current values of parameters
        return {}

    def run_script(self):
        # lots of error handling, maybe backup before?
        pass
