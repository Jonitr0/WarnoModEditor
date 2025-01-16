from PySide6 import QtWidgets, QtCore

from src.wme_widgets import wme_essentials, wme_collapsible


class DivisionSlotMatrixEditor(wme_collapsible.WMECollapsible):
    def __init__(self, parent=None):
        super().__init__(title="Activation Points", parent=parent)
        # TODO: maybe replace with table
        self.grid_layout = QtWidgets.QGridLayout()
        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(self.grid_layout)
        self.add_widget(grid_widget)

        row_names = ["LOG:", "INF:", "ART:", "TNK:", "REC:", "AA:", "HEL:", "AIR:"]
        selection = ["-"]
        for i in range(10):
            selection.append(str(i))

        # rows
        for i in range(8):
            self.grid_layout.addWidget(QtWidgets.QLabel(row_names[i]), i, 0)
            for j in range(10):
                combobox = SlotMatrixComboBox(i, j)
                combobox.addItems(selection)
                combobox.setCurrentIndex(1)
                combobox.value_changed.connect(self.on_value_changed)
                self.grid_layout.addWidget(combobox, i, j + 1)

        form_layout = QtWidgets.QFormLayout()
        form_widget = QtWidgets.QWidget()
        form_widget.setLayout(form_layout)
        self.add_widget(form_widget)

        self.ap_spinbox = wme_essentials.WMESpinbox()
        self.ap_spinbox.setRange(0, 100)
        self.ap_spinbox.setValue(50)
        form_layout.addRow("Activation Points:", self.ap_spinbox)

    def on_value_changed(self, val: str, row: int, col: int):
        if val == "-":
            for i in range(9 - col):
                w = self.grid_layout.itemAtPosition(row, col + i + 2).widget()
                w.setCurrentText("-")
        elif col <= 9:
            for i in range(col + 1):
                w = self.grid_layout.itemAtPosition(row, i + 1).widget()
                if w.currentText() == "-":
                    if i == 0:
                        w.setCurrentText("0")
                    else:
                        last = self.grid_layout.itemAtPosition(row, i).widget()
                        w.setCurrentText(last.currentText())

    def get_state(self) -> dict:
        pass

    def set_state(self, state: dict):
        pass


class SlotMatrixComboBox(wme_essentials.WMECombobox):
    value_changed = QtCore.Signal(str, int, int)

    def __init__(self, row: int, col: int, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.currentTextChanged.connect(lambda t: self.value_changed.emit(t, self.row, self.col))
