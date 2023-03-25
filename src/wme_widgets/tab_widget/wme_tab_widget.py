# TabWidget that manages pages such as editors, etc.

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets.tab_widget import wme_detached_tab, wme_tab_bar
from src.wme_widgets.tab_pages import base_tab_page, rich_text_viewer_page, global_search_page, guid_generator_page
from src.wme_widgets.tab_pages.text_editor_page import ndf_editor_page
from src.wme_widgets import main_widget
from src.dialogs import essential_dialogs
from src.utils import icon_manager
from src.utils.color_manager import *


class WMETabWidget(QtWidgets.QTabWidget):
    tab_removed_by_button = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        tab_bar = wme_tab_bar.WMETabBar(self)
        tab_bar.help_requested.connect(self.on_help_requested)
        self.setTabBar(tab_bar)

        new_tab_button = QtWidgets.QToolButton(self)
        new_tab_button.setIcon(icon_manager.load_icon("add_tab.png", COLORS.SECONDARY_TEXT))
        new_tab_button.setText("Add Tab")
        new_tab_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        new_tab_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        new_tab_button.setShortcut("Ctrl+T")
        new_tab_button.setToolTip("Add a new tab page (Ctrl + T)")
        new_tab_button.setMinimumHeight(36)
        self.setCornerWidget(new_tab_button, Qt.TopRightCorner)

        self.tab_menu = QtWidgets.QMenu()
        self.tab_menu.setToolTipsVisible(True)
        new_tab_button.setMenu(self.tab_menu)

        text_editor_action = self.tab_menu.addAction("Text Editor")
        text_editor_action.setToolTip("Create or edit .ndf files.")
        text_editor_action.triggered.connect(self.on_text_editor)

        global_search_action = self.tab_menu.addAction("Global Search")
        global_search_action.setToolTip("Search for text in all files of your mod.")
        global_search_action.triggered.connect(self.on_global_search)

        guid_generator_action = self.tab_menu.addAction("GUID Generator")
        guid_generator_action.setToolTip("Generate GUIDs (Globally Unique Identifiers), "
                                         "which are used in some NDF objects.")
        guid_generator_action.triggered.connect(self.on_guid_generator)

        self.tab_menu.addSeparator()

        quickstart_action = self.tab_menu.addAction("Quickstart Guide")
        quickstart_action.setToolTip("The Quickstart Guide walks you through the basics of using WME.")
        quickstart_action.triggered.connect(self.on_open_quickstart)
        ndf_reference_action = self.tab_menu.addAction("NDF Reference")
        ndf_reference_action.setToolTip("The NDF Reference contains rules and conventions of the NDF language.")
        ndf_reference_action.triggered.connect(self.on_open_ndf_reference)
        # TODO (0.1.1): add action as soon as html files are ready
        #manual_action = self.tab_menu.addAction("User Manual")
        #manual_action.setToolTip("The User Manual explains WME features in depth.")
        #manual_action.triggered.connect(self.on_open_manual)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_tab_close_pressed)
        self.setAcceptDrops(True)

        # make sure explorer isn't so big
        self.resize(1000, self.height())

    def to_json(self) -> str:
        # TODO (0.1.1): call to_json on all pages
        pass

    def save_state(self):
        # TODO (0.1.1): call to_json and save to settings
        pass

    def on_tab_close_pressed(self, index: int):
        page = self.widget(index)
        if page.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog(page.tab_name)
            result = dialog.exec()

            # don't close on cancel
            if not result == QtWidgets.QDialog.Accepted:
                return
            # on save
            elif dialog.save_changes:
                if not page.save_changes():
                    return

        self.removeTab(index)
        self.tab_removed_by_button.emit()

    def on_open_ndf_editor(self, file_path: str) -> ndf_editor_page.NdfEditorPage:
        file_path = file_path.replace("/", "\\")
        file_name = file_path[file_path.rindex('\\') + 1:]
        editor_icon = icon_manager.load_icon("text_editor.png", COLORS.PRIMARY)
        editor = ndf_editor_page.NdfEditorPage()
        self.addTab(editor, editor_icon, file_name)
        editor.open_file(file_path)
        editor.unsaved_changes = False
        return editor

    def on_open_and_find_ndf_editor(self, file_path: str, search_pattern: str):
        editor = self.on_open_ndf_editor(file_path)
        editor.find_action.setChecked(True)
        editor.find_bar.line_edit.setText(search_pattern)
        editor.code_editor.find_pattern(search_pattern)

    def on_text_editor(self):
        editor_icon = icon_manager.load_icon("text_editor.png", COLORS.PRIMARY)
        editor = ndf_editor_page.NdfEditorPage()
        self.addTab(editor, editor_icon, "Text Editor")
        editor.code_editor.setFocus()

    def on_global_search(self):
        page_icon = icon_manager.load_icon("magnify.png", COLORS.PRIMARY)
        page = global_search_page.GlobalSearchPage()
        self.addTab(page, page_icon, "Global Search")
        page.search_line_edit.setFocus()

    def on_guid_generator(self):
        page_icon = icon_manager.load_icon("cert.png", COLORS.PRIMARY)
        page = guid_generator_page.GuidGeneratorPage()
        self.addTab(page, page_icon, "GUID Generator")

    def on_open_quickstart(self):
        quickstart_icon = icon_manager.load_icon("help.png", COLORS.PRIMARY)
        viewer = rich_text_viewer_page.RichTextViewerPage("Quickstart.html")
        self.addTab(viewer, quickstart_icon, "Quickstart Guide")

    # TODO: add pair and map to NDF reference
    def on_open_ndf_reference(self):
        reference_icon = icon_manager.load_icon("help.png", COLORS.PRIMARY)
        viewer = rich_text_viewer_page.RichTextViewerPage("NdfReference.html")
        self.addTab(viewer, reference_icon, "NDF Reference")

    def on_open_manual(self):
        manual_action = icon_manager.load_icon("help.png", COLORS.PRIMARY)
        viewer = rich_text_viewer_page.RichTextViewerPage("UserManual.md")
        # TODO (0.1.1): fill md file, convert to html
        self.addTab(viewer, manual_action, "User Manual")

    def addTab(self, widget, icon: QtGui.QIcon, title: str) -> int:
        ret = super().addTab(widget, icon, title)
        widget.tab_name = title
        self.setCurrentIndex(ret)
        self.setTabToolTip(ret, title)
        widget.unsaved_status_change.connect(self.on_save_status_changed)
        base_tab_page.all_pages.add(widget)
        return ret

    def insertTab(self, index: int, widget, icon: QtGui.QIcon, title: str) -> int:
        ret = super().insertTab(index, widget, icon, title)
        widget.tab_name = title
        self.setCurrentIndex(ret)
        self.setTabToolTip(ret, title)
        widget.unsaved_status_change.connect(self.on_save_status_changed)
        base_tab_page.all_pages.add(widget)
        return ret

    def removeTab(self, index: int):
        widget = self.widget(index)
        base_tab_page.all_pages.remove(widget)
        super().removeTab(index)

    def ask_all_tabs_to_save(self, all_windows: bool = False) -> bool:
        # close all tabs with no unsaved changes
        i = 0
        while i < self.count():
            page = self.widget(i)
            if not page.unsaved_changes:
                self.removeTab(i)
                i -= 1
            i += 1

        # iterate through own tabs with unsaved changes
        i = 0
        while i < self.count():
            page = self.widget(i)
            dialog = essential_dialogs.AskToSaveDialog(page.tab_name)
            result = dialog.exec()

            # don't close on cancel
            if not result == QtWidgets.QDialog.Accepted:
                return False
            # on save
            elif dialog.save_changes:
                if not page.save_changes():
                    return False
            # on discard, remove tab
            else:
                self.removeTab(i)
                i -= 1
            i += 1

        if all_windows:
            # call function on other windows
            for detached in wme_detached_tab.detached_list:
                if not detached.tab_widget.ask_all_tabs_to_save(False):
                    return False

        # if cancel is never pressed, return True
        return True

    def close_all(self, all_windows: bool = False):
        self.clear()
        if all_windows:
            for detached in wme_detached_tab.detached_list:
                detached.tab_widget.clear()
                detached.close()

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        event.accept()
        if mime_data.property('tab_bar') is not None and mime_data.property('index') is not None:
            wme_tab_bar.drop_bar = self.tabBar()
        super().dragEnterEvent(event)

    def dragLeaveEvent(self, event):
        event.accept()
        wme_tab_bar.drop_bar = None
        super().dragLeaveEvent(event)

    def on_save_status_changed(self, status: bool, widget: QtWidgets.QWidget):
        index = self.indexOf(widget)
        # if it has unsaved changes
        if status:
            self.setTabText(index, widget.tab_name + "(*)")
            self.setTabToolTip(index, widget.tab_name + "(*)")
        else:
            self.setTabText(index, widget.tab_name)
            self.setTabToolTip(index, widget.tab_name)

    def on_help_requested(self, index: int):
        self.widget(index).on_help()
