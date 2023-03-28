# tab page that generates GUIDs

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages import base_tab_page
from src.utils.color_manager import *

import uuid


class GuidGeneratorPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout()
        hyperlink_color = get_color_for_key(COLORS.PRIMARY.value)
        info_layout = QtWidgets.QHBoxLayout()

        info_label = QtWidgets.QLabel()
        info_text = "<a style =\"color: " + hyperlink_color + "\"href='https://en.wikipedia.org/wiki" \
                                                              "/Universally_unique_identifier'>GUIDs</a> (Globally " \
                                                              "Unique Identifiers) are randomly generated, " \
                                                              "fixed length pieces of text that are used to identify " \
                                                              "certain NDF objects. They will typically appear in " \
                                                              ".ndf files in the following format: <code>GUID:{" \
                                                              "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}</code>. Each " \
                                                              "generated GUID is, for practical purposes, guaranteed " \
                                                              "to be unique. This tool generates 10 new GUIDs each " \
                                                              "time you press the \"Generate\" button. "
        info_label.setTextFormat(Qt.RichText)
        info_label.setText(info_text)
        info_label.setOpenExternalLinks(True)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)

        generate_button = QtWidgets.QPushButton("Generate")
        generate_button.setFixedWidth(150)
        generate_button.clicked.connect(self.on_generate)
        info_layout.addWidget(generate_button)

        self.text_edit = QtWidgets.QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setObjectName("code_editor")
        self.text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)

        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)

    def on_generate(self):
        self.text_edit.clear()

        text = ""

        for i in range(10):
            text += "GUID:{" + str(uuid.uuid4()) + "}\n"

        self.text_edit.setPlainText(text)

    def to_json(self) -> dict:
        page_json = {"type": str(type(self)),
                     "currentText": self.text_edit.toPlainText()}
        return page_json

