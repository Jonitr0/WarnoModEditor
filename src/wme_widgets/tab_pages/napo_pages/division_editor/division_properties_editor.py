from PySide6 import QtWidgets

from src.wme_widgets import wme_essentials, wme_collapsible


class DivisionPropertiesEditor(wme_collapsible.WMECollapsible):
    def __init__(self, parent=None):
        super().__init__(title="Properties", parent=parent)
        form_layout = QtWidgets.QFormLayout()
        form_widget = QtWidgets.QWidget()
        form_widget.setLayout(form_layout)
        self.add_widget(form_widget)

        # needs to be able to find existing strings
        self.name_token_edit = wme_essentials.WMELineEdit()
        form_layout.addRow("Name Token:", self.name_token_edit)

        self.alliance_combobox = wme_essentials.WMECombobox(editable=False)
        self.alliance_combobox.addItems(["NATO", "PACT"])
        form_layout.addRow("Alliance:", self.alliance_combobox)

        # needs to list available countries
        self.nation_combobox = wme_essentials.WMECombobox()
        form_layout.addRow("Nation:", self.nation_combobox)

        self.rating_combobox = wme_essentials.WMECombobox(editable=False)
        self.rating_combobox.addItems(["A", "B", "C"])
        form_layout.addRow("Division Rating:", self.rating_combobox)

        self.type_combobox = wme_essentials.WMECombobox()
        form_layout.addRow("Division Type:", self.type_combobox)

        # needs to be able to load existing icon or import new one
        self.icon_lineedit = wme_essentials.WMELineEdit()
        form_layout.addRow("Emblem:", self.icon_lineedit)

    def get_state(self) -> dict:
        pass

    def set_state(self, state: dict):
        pass
