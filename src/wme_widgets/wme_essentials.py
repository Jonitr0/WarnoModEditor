from PySide6 import QtWidgets, QtCore, QtGui
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


class WMECombobox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.setFocusPolicy(Qt.StrongFocus)

        completer = CustomQCompleter(self)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setModel(self.model())
        self.setCompleter(completer)

    def focusOutEvent(self, event) -> None:
        super(WMECombobox, self).focusOutEvent(event)

        if self.lineEdit().hasFocus():
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


def wrapEF(ef):
    w = QtCore.QObject()
    w.eventFilter = ef
    return w


def sbEventFilter(s, e):
    q = s
    if (e.type() == QtCore.QEvent.MouseButtonPress and e.button() == Qt.LeftButton
            or e.type() == QtCore.QEvent.MouseButtonDblClick):
        # pixelPosToRangeValue(pos)
        opt = QtWidgets.QStyleOptionSlider()
        q.initStyleOption(opt)
        gr = q.style().subControlRect(QtWidgets.QStyle.CC_ScrollBar, opt,
                                      QtWidgets.QStyle.SC_ScrollBarGroove, q)
        sr = q.style().subControlRect(QtWidgets.QStyle.CC_ScrollBar, opt,
                                      QtWidgets.QStyle.SC_ScrollBarSlider, q)
        if q.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
            if q.layoutDirection() == Qt.RightToLeft:
                opt.upsideDown = not opt.upsideDown
            dt = sr.width() / 2
            pos = e.pos().x()
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
            dt = sr.height() / 2
            pos = e.pos().y()
        r = QtWidgets.QStyle.sliderValueFromPosition(q.minimum(), q.maximum(),
                                                     pos - sliderMin - dt,
                                                     sliderMax - sliderMin, opt.upsideDown)
        # pixelPosToRangeValue,
        q.setValue(r)
    return q.eventFilter(s, e)


class WMEScrollBar(QtWidgets.QScrollBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ef = wrapEF(sbEventFilter)
        self.installEventFilter(self.ef)


class WMETextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setVerticalScrollBar(WMEScrollBar())
        self.setHorizontalScrollBar(WMEScrollBar())
        self.anchor = None

    def mousePressEvent(self, e):
        # if Ctrl is pressed
        if e.modifiers() == Qt.ControlModifier:
            self.anchor = self.anchorAt(e.pos())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if self.anchor:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.anchor))
            self.anchor = None
        super().mouseReleaseEvent(e)
