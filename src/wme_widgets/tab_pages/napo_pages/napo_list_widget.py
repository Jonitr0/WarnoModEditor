from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.utils import icon_manager
from src.utils.color_manager import *


class NapoListWidget(QtWidgets.QWidget):
    # TODO: handle duplicates and empty items
    list_updated = QtCore.Signal(list)

    def __init__(self, title: str = "", input_mask: str = ".*", allow_empty: bool = False):
        super().__init__()

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setHidden(title == "")

        self.list_widget = ListFitToContents()
        delegate = ListValidatorDelegate(input_mask)
        delegate.closeEditor.connect(self.on_edit_finished)
        self.list_widget.setItemDelegate(delegate)
        self.input_mask = input_mask
        self.allow_empty = allow_empty

        self.add_button = QtWidgets.QToolButton()
        self.remove_button = QtWidgets.QToolButton()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(0)
        main_layout.addLayout(header_layout)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1)

        header_layout.addWidget(self.add_button)
        self.add_button.setIcon(icon_manager.load_icon("plus.png", COLORS.PRIMARY))
        self.add_button.setFixedSize(36, 36)
        self.add_button.setIconSize(QtCore.QSize(36, 36))
        self.add_button.setToolTip("Add entry")
        self.add_button.clicked.connect(self.on_add)

        header_layout.addWidget(self.remove_button)
        remove_icon = QtGui.QIcon()
        remove_icon.addPixmap(icon_manager.load_pixmap("minus.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        remove_icon.addPixmap(icon_manager.load_pixmap("minus.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.remove_button.setIcon(remove_icon)
        self.remove_button.setFixedSize(36, 36)
        self.remove_button.setIconSize(QtCore.QSize(36, 36))
        self.remove_button.setToolTip("Remove selected entry")
        self.remove_button.clicked.connect(self.on_remove)

        main_layout.addWidget(self.list_widget)

    def update_list(self, items: []):
        self.list_widget.clear()
        items = [str(i) for i in items]

        # remove items that don't fit input mask
        regex = QtCore.QRegularExpression(self.input_mask)
        items_filtered = [i for i in items if regex.match(i).hasMatch()]

        self.list_widget.addItems(items_filtered)
        self.list_widget.sortItems()

        remove = self.list_widget.count() > 1 or self.allow_empty
        self.remove_button.setEnabled(remove)

    def update_widget(self):
        self.update_list(self.list_widget.all_item_labels())

    def on_edit_finished(self):
        self.update_widget()
        self.list_updated.emit(self.list_widget.all_item_labels())

    def on_add(self):
        self.update_widget()
        self.list_widget.addItem("")

        self.list_widget.clearSelection()
        self.list_widget.setFocus()
        self.list_widget.editItem(self.list_widget.last())

    def on_remove(self):
        selected = self.list_widget.selectedItems()
        if len(selected) == 0:
            return

        for item in selected:
            self.list_widget.takeItem(self.list_widget.row(item))

        self.update_widget()
        self.list_updated.emit(self.list_widget.all_item_labels())


class ListValidatorDelegate(QtWidgets.QItemDelegate):
    def __init__(self, input_mask: str):
        super().__init__()
        self.input_mask = input_mask

    def createEditor(self, parent: QtWidgets.QWidget, option: QtWidgets.QStyleOptionViewItem,
                     index) -> QtWidgets.QWidget:
        editor = QtWidgets.QLineEdit(parent)
        editor.setValidator(QtGui.QRegularExpressionValidator(self.input_mask))
        return editor


class ListFitToContents(QtWidgets.QListWidget):
    def minimumSizeHint(self) -> QtCore.QSize:
        return self.calculate_size()

    def sizeHint(self) -> QtCore.QSize:
        return self.calculate_size()

    def calculate_size(self):
        height = 0
        if self.count() > 0:
            height = self.sizeHintForRow(0) * self.count() + 8

        s = QtCore.QSize()
        s.setHeight(height)
        s.setWidth(super().sizeHint().width())
        return s

    def last(self) -> QtWidgets.QListWidgetItem:
        return self.item(self.count() - 1)

    def all_item_labels(self) -> [str]:
        items = []
        for i in range(self.count()):
            items.append(self.item(i).text())
        return items

    def addItems(self, labels) -> None:
        for label in labels:
            self.addItem(label)
        self.updateGeometry()

    def addItem(self, item) -> None:
        super().addItem(ListItemSortable(item))
        added = self.item(self.count() - 1)
        added.setFlags(added.flags() | Qt.ItemIsEditable)
        self.updateGeometry()


class ListItemSortable(QtWidgets.QListWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except Exception:
            return QtWidgets.QListWidgetItem.__lt__(self, other)
