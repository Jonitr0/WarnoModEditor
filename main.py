import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet

import main_window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    print("Screen dpi: " + str(dpi))

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
