# TabWidget that manages pages such as editors, etc.

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt

from wme_widgets import wme_title_bar
from wme_widgets.tab_pages import ndf_editor_widget, tab_page_base


class WMETabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # TODO: add tab context menu (close all, close all but this, close all saved)

        tab_bar = self.WMETabBar(self)
        self.setTabBar(tab_bar)

        # TODO: style button
        new_tab_button = QtWidgets.QPushButton()
        new_tab_button.setText("Add Tab..")
        new_tab_button.setMinimumHeight(20)
        self.setCornerWidget(new_tab_button)

        self.tab_menu = QtWidgets.QMenu()
        new_tab_button.setMenu(self.tab_menu)

        self.add_new_tab_action(".ndf Editor")

        self.setTabsClosable(True)
        # TODO: run save check
        self.tabCloseRequested.connect(self.on_tab_close_pressed)

    def to_json(self) -> str:
        # TODO: call to_json on all pages
        pass

    def save_state(self):
        # TODO: call to_json and save to settings
        pass

    def add_new_tab_action(self, name: str):
        action = self.tab_menu.addAction(name)
        if name == ".ndf Editor":
            action.triggered.connect(self.add_ndf_editor)
        return action

    def add_ndf_editor(self):
        self.addTab(ndf_editor_widget.NdfEditorWidget(), ".ndf Editor")

    def on_tab_close_pressed(self, index: int):
        # TODO: ask to save progress
        self.removeTab(index)

    class WMETabBar(QtWidgets.QTabBar):
        def __init__(self, parent=None):
            self.dragStartPos = QtCore.QPoint(0,0)
            self.dragging_tab = -1

            super().__init__(parent)

        def mousePressEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                self.dragStartPos = event.pos()
                self.dragging_tab = self.tabAt(self.dragStartPos)

            QtWidgets.QTabBar.mousePressEvent(self, event)

        def mouseReleaseEvent(self, event):
            widget = self.parent().widget(self.dragging_tab)
            # TODO: get type
            copy_widget = ndf_editor_widget.NdfEditorWidget(other=widget)

            detached = WMETabWidget.WMEDetachedTab(widget=copy_widget, title="TODO tab title")
            detached.move(self.mapToGlobal(event.pos()))
            detached.showNormal()

            self.parent().removeTab(self.dragging_tab)
            self.dragging_tab = -1

            QtWidgets.QTabBar.mouseReleaseEvent(self, event)

        def mouseMoveEvent(self, event):
            super().mouseMoveEvent(event)

    class WMEDetachedTab(QtWidgets.QDialog):
        close_pressed = QtCore.Signal(tab_page_base.TabPageBase)

        def __init__(self, parent=None, widget: tab_page_base.TabPageBase = None, title: str = ""):
            super().__init__(parent)

            self.setModal(False)
            self.setWindowFlags(Qt.FramelessWindowHint)

            self.bar_layout = QtWidgets.QVBoxLayout(self)
            self.bar_layout.setContentsMargins(1, 0, 1, 16)
            self.bar_layout.setSpacing(0)
            self.setLayout(self.bar_layout)

            self.title_bar = wme_title_bar.WMETitleBar(self)
            self.bar_layout.addWidget(self.title_bar)
            self.widget = widget
            self.bar_layout.addWidget(self.widget)

            self.grip = QtWidgets.QSizeGrip(self)
            self.grip.resize(16, 16)

            self.setWindowTitle(title)

        def resizeEvent(self, event):
            QtWidgets.QDialog.resizeEvent(self, event)
            rect = self.rect()
            self.grip.move(rect.right() - 16, rect.bottom() - 16)

        def close(self):
            # TODO: ask to save progress
            self.close_pressed.emit(self.widget)
            return super().close()

        def setWindowTitle(self, title: str):
            super().setWindowTitle(title)
            self.title_bar.set_title(title)
