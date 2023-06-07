from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.utils.color_manager import *


class WMELineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.placeholder_color = COLORS.SECONDARY_LIGHT
        if theme_manager.is_light_theme():
            self.placeholder_color = COLORS.SECONDARY_TEXT

        self.textChanged.connect(self.on_text_changed)
        self.on_text_changed()

    def on_text_changed(self):
        if self.text() == "":
            self.setStyleSheet("QLineEdit { color: " + get_color_for_key(self.placeholder_color.value) +
                               "; font: italic; }")
        else:
            self.setStyleSheet("QLineEdit { color: " + get_color_for_key(COLORS.PRIMARY.value) + "; }")


# form here: https://stackoverflow.com/questions/5129211/qcompleter-custom-completion-rules
class CustomQCompleter(QtWidgets.QCompleter):
    def __init__(self, parent=None):
        super(CustomQCompleter, self).__init__(parent)
        self.local_completion_prefix = ""
        self.source_model = None

    def setModel(self, model):
        self.source_model = model
        super(CustomQCompleter, self).setModel(self.source_model)

    def updateModel(self):
        local_completion_prefix = self.local_completion_prefix

        class InnerProxyModel(QtCore.QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
                return local_completion_prefix.lower() in self.sourceModel().data(index0).lower()

        proxy_model = InnerProxyModel()
        proxy_model.setSourceModel(self.source_model)
        super(CustomQCompleter, self).setModel(proxy_model)

    def splitPath(self, path):
        self.local_completion_prefix = path
        self.updateModel()
        return ""


class WMEComboboxLineEdit(QtWidgets.QLineEdit):
    focus_out = QtCore.Signal()

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.focus_out.emit()


class WMECombobox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.setFocusPolicy(Qt.StrongFocus)

        self.setLineEdit(WMEComboboxLineEdit())
        self.lineEdit().focus_out.connect(self.on_close_lineedit)

        completer = CustomQCompleter(self)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setModel(self.model())
        self.setCompleter(completer)

    def on_close_lineedit(self):
        if self.lineEdit().hasFocus():
            print("focus")
            return

        if self.findText(self.currentText()) < 0:
            self.setCurrentIndex(0)

    def wheelEvent(self, e) -> None:
        if self.hasFocus():
            super().wheelEvent(e)
        else:
            e.ignore()


class WMESpinbox(QtWidgets.QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, e) -> None:
        if self.hasFocus():
            super().wheelEvent(e)
        else:
            e.ignore()


class WMEDoubleSpinbox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, e) -> None:
        if self.hasFocus():
            super().wheelEvent(e)
        else:
            e.ignore()
