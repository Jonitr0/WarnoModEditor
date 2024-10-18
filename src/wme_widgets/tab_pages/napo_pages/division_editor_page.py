from src.wme_widgets.tab_pages.napo_pages import base_napo_page


class DivisionEditorPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()

        '''toolbar'''

        # New Div Button
        # Save Button
        # Copy Div Button
        # Div Selector Combobox/Load Div Button with Dialog

        self.add_help_button()

        '''main page'''

        # general editor: name, side/country, class, icon,... (collapsible)
        # action point editor (collapsible)
        # collapsible category editors: Gridlayout? Transport Popup Menu?

