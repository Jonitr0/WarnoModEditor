# tab page that generates GUIDs

from PySide6 import QtWidgets

from src.wme_widgets.tab_pages import tab_page_base

import uuid


class GuidGeneratorPage(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout()

        info_label = QtWidgets.QLabel("GUIDs (Globally Unique Identifiers) are randomly generated, fixed length pieces"
                                      " of text that are used to identify certain NDF objects.")
        main_layout.addWidget(info_label)

        self.setLayout(main_layout)