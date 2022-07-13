from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt

from wme_widgets.tab_pages import ndf_editor_widget
from wme_widgets.tab_widget import wme_detached_tab

drop_bar = None


class WMETabBar(QtWidgets.QTabBar):
    tab_removed = QtCore.Signal()

    def __init__(self, parent=None):
        self.dragStartPos = QtCore.QPoint(0, 0)
        self.dragging_tab_index = -1

        super().__init__(parent)

        self.setMinimumWidth(100)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragStartPos = event.pos()
            self.dragging_tab_index = self.tabAt(self.dragStartPos)

        QtWidgets.QTabBar.mousePressEvent(self, event)

    def create_detached_window(self):
        detached = wme_detached_tab.WMEDetachedTab()

        widget = self.parent().widget(self.dragging_tab_index)
        self.parent().removeTab(self.dragging_tab_index)
        detached.add_tab(widget, "TODO title")
        point = QtGui.QCursor.pos()
        detached.move(point)
        # TODO: proper size
        detached.resize(640, 480)
        detached.show()

        wme_detached_tab.detached_list.append(detached)

        self.parent().removeTab(self.dragging_tab_index)
        self.dragging_tab_index = -1

    def mouseMoveEvent(self, event):
        # Determine if the current movement is detected as a drag
        if not self.dragStartPos.isNull() and (
                (event.pos() - self.dragStartPos).manhattanLength() < QtWidgets.QApplication.startDragDistance()):
            self.dragInitiated = True

        # If the current movement is a drag initiated by the left button
        if (event.buttons() & Qt.LeftButton) and self.dragInitiated:

            # Stop the move event
            finish_move_event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, event.pos(), Qt.NoButton,
                                                  Qt.NoButton, Qt.NoModifier)
            QtWidgets.QTabBar.mouseMoveEvent(self, finish_move_event)

            # Convert the move event into a drag
            drag = QtGui.QDrag(self)

            # Create the appearance of dragging the tab content
            pixmap = QtGui.QPixmap.grabWindow(self.parentWidget().currentWidget().winId())
            pixmap = pixmap.scaledToHeight(100)
            target_pixmap = QtGui.QPixmap(pixmap.size())
            target_pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(target_pixmap)
            painter.setOpacity(0.85)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
            drag.setPixmap(target_pixmap)

            mime_data = QtCore.QMimeData()
            mime_data.setProperty('tab_bar', self)
            mime_data.setProperty('index', self.dragging_tab_index)
            drag.setMimeData(mime_data)

            # Initiate the drag
            drag.exec_(Qt.MoveAction | Qt.CopyAction)

            global drop_bar
            # outside tab bar
            if drop_bar is None:
                self.create_detached_window()
                event.accept()
            # inside drop bar
            else:
                self.handle_inside_drop(drag.mimeData(), drop_bar)
                event.accept()

        else:
            super().mouseMoveEvent(event)

    def handle_inside_drop(self, mime_data: QtCore.QMimeData, trigger):
        point = self.mapFromGlobal(QtGui.QCursor.pos())
        new_index = self.tabAt(point)
        origin_index = mime_data.property('index')
        origin_bar = mime_data.property('tab_bar')

        if origin_bar == trigger:
            print("drop from self")
            print(new_index)
        else:
            print("drop from other")

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        event.accept()
        if mime_data.property('tab_bar') is not None and mime_data.property('index') is not None:
            global drop_bar
            drop_bar = self
        super().dragEnterEvent(event)

    def dragLeaveEvent(self, event):
        event.accept()
        global drop_bar
        drop_bar = None
        super().dragLeaveEvent(event)

    def tabRemoved(self, index: int):
        self.tab_removed.emit()
        if self.count() < 1:
            self.setMinimumWidth(100)
        super().tabRemoved(index)

    def tabInserted(self, index: int):
        if self.count() > 0:
            self.setMinimumWidth(0)
        super().tabInserted(index)
