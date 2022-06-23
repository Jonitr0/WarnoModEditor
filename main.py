import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet

import main_window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()

    scale = -2
    if dpi > 100:
        scale = 2

    extra = {'density_scale': scale,
             'danger': '#dc3545',
             'warning': '#ffc107',
             'success': '#17a2b8',
             }
    apply_stylesheet(app, theme="dark_nato.xml", extra=extra)

    stylesheet = app.styleSheet()
    with open('resources/custom_style.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    QtWidgets.QApplication.instance().setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)

    app_icon = QtGui.QIcon()
    app_icon.addFile('resources/img/icon16.png', QtCore.QSize(16, 16))
    app_icon.addFile('resources/img/icon24.png', QtCore.QSize(24, 24))
    app_icon.addFile('resources/img/icon32.png', QtCore.QSize(32, 32))
    app_icon.addFile('resources/img/icon48.png', QtCore.QSize(48, 48))
    app_icon.addFile('resources/img/icon64.png', QtCore.QSize(64, 64))
    app_icon.addFile('resources/img/icon128.png', QtCore.QSize(128, 128))
    app_icon.addFile('resources/img/icon256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    main_window = main_window.MainWindow()
    sys.exit(app.exec_())
