from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt

from wme_widgets.tab_pages import ndf_editor_widget
from wme_widgets.tab_widget import wme_detached_tab


class WMETabBar(QtWidgets.QTabBar):
    def __init__(self, parent=None):
        self.dragStartPos = QtCore.QPoint(0, 0)
        self.dragging_tab_index = -1
        self.detached_list = []

        super().__init__(parent)

        self.setMinimumWidth(100)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragStartPos = event.pos()
            self.dragging_tab_index = self.tabAt(self.dragStartPos)

        QtWidgets.QTabBar.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        widget = self.parent().widget(self.dragging_tab_index)
        # TODO: get type
        copy_widget = ndf_editor_widget.NdfEditorWidget(other=widget)

        detached = wme_detached_tab.WMEDetachedTab(widget=copy_widget, title="TODO tab title")
        point = self.mapToGlobal(event.pos())
        point.setX(point.x() - 320)
        detached.move(point)
        detached.resize(640, 480)
        detached.show()

        detached.close_pressed.connect(self.on_detached_close)
        self.detached_list.append(detached)

        self.parent().removeTab(self.dragging_tab_index)
        self.dragging_tab_index = -1

        QtWidgets.QTabBar.mouseReleaseEvent(self, event)

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
            drop_action = drag.exec_(Qt.MoveAction | Qt.CopyAction)

            # outside tab bar
            if drop_action == Qt.IgnoreAction:
                print("outside")
                event.accept()

        else:
            super().mouseMoveEvent(event)

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.property('tab_bar') is not None and mime_data.property('index') is not None:
            print("Has props")
        super().dragEnterEvent(event)

    def tabRemoved(self, index: int):
        if self.count() < 1:
            self.setMinimumWidth(100)
        super().tabRemoved(index)

    def tabInserted(self, index: int):
        if self.count() > 0:
            self.setMinimumWidth(0)
        super().tabInserted(index)

    def get_detached_list(self):
        return self.detached_list

    def on_detached_close(self, detached):
        self.detached_list.remove(detached)
