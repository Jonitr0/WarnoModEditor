import sys
import os
import logging
from pathlib import Path

from src.utils.resource_loader import *

os.environ["NDF_LIB_PATH"] = get_resource_path("resources/dependencies/ndf.dll")

from PySide6 import QtWidgets
from qt_material import apply_stylesheet

from src import main_window
from src.utils import settings_manager, theme_manager
from src.dialogs import exception_handler_dialog
from src.wme_widgets import wme_splash_screen

if __name__ == '__main__':
    # setup logging
    log_file = get_persistant_path("wme.log")
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                        filename=log_file,
                        level=logging.INFO,
                        datefmt='%d/%m/%Y %H:%M:%S')

    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(console_logger)

    # if a wme_config.json still exists in the old location, move it to the new location
    old_config_path = os.path.join(Path.home(), "WarnoModEditor\\wme_config.json")
    if os.path.exists(old_config_path) and not os.path.exists(get_persistant_path("wme_config.json")):
        new_config_path = get_persistant_path("wme_config.json")
        os.rename(old_config_path, new_config_path)

    # create settings changed notifier
    settings_manager.SettingsChangedNotifier()

    # load theme
    theme_name = settings_manager.get_settings_value(settings_manager.THEME_KEY)
    theme, invert_secondary = theme_manager.get_theme_file(theme_name)
    theme = get_resource_path("resources\\themes\\" + theme)

    app = QtWidgets.QApplication(sys.argv)

    extra = {'density_scale': 0,
             'danger': '#dc3545',
             'warning': '#ffc107',
             'success': '#17a2b8',
             }
    apply_stylesheet(app, theme=theme, extra=extra, invert_secondary=invert_secondary)

    stylesheet = app.styleSheet()
    with open(get_resource_path('resources/custom_style.css')) as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    # setup exception handler
    exception_handler = exception_handler_dialog.ExceptionHandler()
    sys.excepthook = exception_handler.exceptHook

    # set version
    version = "0.4.0"
    settings_manager.write_settings_value(settings_manager.VERSION_KEY, version)

    # append line breaks to log
    with open(log_file, 'a') as file:
        file.write("\n\n")
    logging.info("Starting WME " + version)
    logging.info("Working Directory: " + get_resource_path(''))

    # make sure scripts dir exits and has __init__.py
    scripts_dir = get_export_path("Scripts")
    if not os.path.exists(os.path.join(scripts_dir, "__init__.py")):
        with open(os.path.join(scripts_dir, "__init__.py"), "w") as file:
            pass

    # setup splash screen
    splash_screen = wme_splash_screen.WMESplashScreen("Warno Mod Editor v" + version)
    app.processEvents()

    main_window = main_window.MainWindow()
    splash_screen.finish(main_window)

    # only start app if warno path was verified
    if main_window.isVisible():
        sys.exit(app.exec())
