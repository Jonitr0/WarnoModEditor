from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets.tab_widget import wme_detached_tab
from src.utils.color_manager import *

drop_bar = None


class WMETabBar(QtWidgets.QTabBar):
    tab_removed = QtCore.Signal()
    help_requested = QtCore.Signal(int)

    def __init__(self, parent=None):
        self.dragStartPos = QtCore.QPoint(0, 0)
        self.dragging_tab_index = -1
        self.hover_tab_index = -1
        self.dragInitiated = False

        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setUsesScrollButtons(False)
        self.setElideMode(Qt.ElideRight)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragStartPos = event.pos()
            self.dragging_tab_index = self.tabAt(self.dragStartPos)

        super().mousePressEvent(event)

    def create_detached_window(self):
        # make sure window is closed if needed
        self.parent().tab_removed_by_button.emit()

        detached = wme_detached_tab.WMEDetachedTab()

        widget = self.parent().widget(self.dragging_tab_index)
        icon = self.parent().tabIcon(self.dragging_tab_index)
        title = self.parent().tabText(self.dragging_tab_index)
        self.parent().removeTab(self.dragging_tab_index)
        detached.add_tab(widget, icon, title)
        point = QtGui.QCursor.pos()
        
        detached.move(point)
        detached.resize(640, 480)
        detached.show()

        wme_detached_tab.detached_list.append(detached)

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
            super().mouseMoveEvent(finish_move_event)

            # Convert the move event into a drag
            drag = QtGui.QDrag(self)

            # Create the appearance of dragging the tab content
            pixmap = QtGui.QPixmap(self.parent().size())
            self.parent().render(pixmap)
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
            mime_data.setProperty('icon', self.tabIcon(self.dragging_tab_index))
            mime_data.setProperty('title', self.tabText(self.dragging_tab_index))
            drag.setMimeData(mime_data)

            # Initiate the drag
            global drop_bar
            drop_bar = self
            self.hover_tab_index = self.dragging_tab_index
            self.update()
            drag.exec_(Qt.MoveAction | Qt.CopyAction)

            # outside tab bar
            if drop_bar is None:
                event.accept()
                self.create_detached_window()
            # inside drop bar
            else:
                event.accept()
                self.handle_inside_drop(drag.mimeData(), drop_bar)

            # reset all relevant members and repaint
            self.dragging_tab_index = -1
            self.hover_tab_index = -1
            self.update()

        else:
            super().mouseMoveEvent(event)

    # handles a drop inside a TabBar or TabWidget
    def handle_inside_drop(self, mime_data: QtCore.QMimeData, trigger):
        point = trigger.mapFromGlobal(QtGui.QCursor.pos())
        new_index = trigger.tabAt(point)
        origin_index = mime_data.property('index')
        origin_bar = mime_data.property('tab_bar')
        icon = mime_data.property('icon')
        title = mime_data.property('title')

        # the drop comes from the own TabBar
        if origin_bar == trigger:
            if origin_index == new_index or new_index == -1:
                return
            widget = origin_bar.parent().widget(origin_index)
            origin_bar.parent().removeTab(origin_index)
            origin_bar.parent().insertTab(new_index, widget, icon, title)
            origin_bar.parent().setCurrentIndex(new_index)
        # the drop comes from a different TabBar
        else:
            widget = origin_bar.parent().widget(origin_index)
            origin_bar.parent().removeTab(origin_index)
            # make sure window is closed if needed
            self.parent().tab_removed_by_button.emit()
            if new_index == -1:
                trigger.parent().addTab(widget, icon, title)
                trigger.parent().setCurrentIndex(trigger.parent().count() - 1)
            else:
                trigger.parent().insertTab(new_index, widget, icon, title)
                trigger.parent().setCurrentIndex(new_index)

            # repaint the triggering TabBar
            trigger.hover_tab_index = -1
            trigger.update()

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
        self.hover_tab_index = -1
        self.update()
        super().dragLeaveEvent(event)

    def dragMoveEvent(self, event):
        event.accept()
        point = self.mapFromGlobal(QtGui.QCursor.pos())
        current_index = self.tabAt(point)
        if self.hover_tab_index != current_index:
            self.hover_tab_index = current_index
            self.update()
        super().dragMoveEvent(event)

    def tabRemoved(self, index: int):
        self.tab_removed.emit()
        super().tabRemoved(index)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.hover_tab_index < 0:
            return

        painter = QtGui.QPainter(self)
        option = QtWidgets.QStyleOptionTab()
        palette = option.palette

        self.initStyleOption(option, self.hover_tab_index)

        palette.setColor(palette.WindowText, QtGui.QColor(get_color_for_key(COLORS.PRIMARY.value)))

        option.palette = palette
        self.style().drawControl(QtWidgets.QStyle.CE_TabBarTab, option, painter)

    def mouseReleaseEvent(self, event):
        if not event.button() == Qt.RightButton:
            return
        index = self.tabAt(event.pos())
        if index < 0:
            return

        context_menu = QtWidgets.QMenu(self)
        close_self_action = context_menu.addAction("Close Tab")
        close_all_action = None
        close_others_action = None
        if self.count() > 1:
            close_all_action = context_menu.addAction("Close All Tabs")
            close_others_action = context_menu.addAction("Close Other Tabs")

        if self.parent().widget(index).help_file_path != "":
            context_menu.addSeparator()
            help_action = context_menu.addAction("Help")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        start_count = self.count()

        if action is None:
            super().mouseReleaseEvent(event)
            return

        if action == close_self_action:
            self.tabCloseRequested.emit(index)
        elif action == close_all_action:
            for i in range(start_count):
                self.tabCloseRequested.emit(start_count - i - 1)
        elif action == close_others_action:
            for i in range(start_count):
                if start_count- i - 1 is not index:
                    self.tabCloseRequested.emit(start_count - i - 1)
        elif action == help_action:
            self.help_requested.emit(index)

        super().mouseReleaseEvent(event)
