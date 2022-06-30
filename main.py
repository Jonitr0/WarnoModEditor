import sys
import os
import logging

from PySide2 import QtWidgets, QtCore
from qt_material import apply_stylesheet

import main_window

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                        filename='wme.log',
                        level=logging.INFO,
                        datefmt='%d/%m/%Y %H:%M:%S')

    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(console_logger)

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
    apply_stylesheet(app, theme="dark_lightgreen.xml", extra=extra)

    stylesheet = app.styleSheet()
    with open('resources/custom_style.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    QtWidgets.QApplication.instance().setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)

    main_window = main_window.MainWindow()
    sys.exit(app.exec_())
