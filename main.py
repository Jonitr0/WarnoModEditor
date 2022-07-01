import sys
import os
import logging

from PySide2 import QtWidgets, QtCore
from qt_material import apply_stylesheet

import main_window
from utils import settings_manager, theme_manager

if __name__ == '__main__':
    # setup logging
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                        filename='wme.log',
                        level=logging.INFO,
                        datefmt='%d/%m/%Y %H:%M:%S')

    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(console_logger)

    # load theme
    theme_name = settings_manager.get_settings_value(settings_manager.THEME_KEY)
    theme = theme_manager.get_theme_file(theme_name)
    invert_secondary = False
    if theme.startswith("light"):
        invert_secondary = True

    app = QtWidgets.QApplication(sys.argv)

    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    logging.info("WME started with screen dpi: " + str(dpi))

    scale = -2
    if dpi > 100:
        scale = 2

    extra = {'density_scale': scale,
             'danger': '#dc3545',
             'warning': '#ffc107',
             'success': '#17a2b8',
             }
    apply_stylesheet(app, theme=theme, extra=extra, invert_secondary=invert_secondary)

    stylesheet = app.styleSheet()
    with open('resources/custom_style.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    QtWidgets.QApplication.instance().setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)

    main_window = main_window.MainWindow()
    sys.exit(app.exec_())
