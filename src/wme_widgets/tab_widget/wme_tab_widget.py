# TabWidget that manages pages such as editors, etc.

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets import main_widget
from src.wme_widgets.tab_widget import wme_detached_tab, wme_tab_bar
from src.wme_widgets.tab_pages import base_tab_page, rich_text_viewer_page, global_search_page, guid_generator_page, \
    csv_editor_page, mod_config_page
from src.wme_widgets.tab_pages.script_runner import script_runner_page
from src.wme_widgets.tab_pages.diff_page import diff_page, file_comparison_page
from src.wme_widgets.tab_pages.text_editor_page import ndf_editor_page
from src.wme_widgets.tab_pages.napo_pages import game_settings_page, division_editor_page
from src.dialogs import essential_dialogs
from src.utils import icon_manager, parser_utils
from src.utils.color_manager import *


class WMETabWidget(QtWidgets.QTabWidget):
    tab_removed_by_button = QtCore.Signal()

    icon_paths_for_pages = {
        ndf_editor_page.NdfEditorPage: "text_editor.png",
        global_search_page.GlobalSearchPage: "magnify.png",
        guid_generator_page.GuidGeneratorPage: "cert.png",
        rich_text_viewer_page.RichTextViewerPage: "help.png",
        game_settings_page.GameSettingsPage: "game_settings.png",
        csv_editor_page.CsvEditorPage: "edit_table.png",
        diff_page.DiffPage: "diff.png",
        file_comparison_page.FileComparisonPage: "file_compare.png",
        mod_config_page.ModConfigPage: "file_config.png",
        script_runner_page.ScriptRunnerPage: "file_code.png",
        division_editor_page.DivisionEditorPage: "div_editor.png"
    }

    # TODO: add back Operation Editor
    # TODO: add String Manager
    # TODO: add Icon Manager

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

        text_editor_icon = self.get_icon_for_page_type(ndf_editor_page.NdfEditorPage)
        text_editor_action = self.tab_menu.addAction(text_editor_icon, "Text Editor")
        text_editor_action.setToolTip("Create or edit .ndf files.")
        text_editor_action.setShortcut("Ctrl+Alt+E")
        text_editor_action.setShortcutContext(Qt.WindowShortcut)
        text_editor_action.triggered.connect(self.on_text_editor)

        csv_editor_icon = self.get_icon_for_page_type(csv_editor_page.CsvEditorPage)
        csv_editor_action = self.tab_menu.addAction(csv_editor_icon, "CSV Editor")
        csv_editor_action.setToolTip("Create or edit .csv files.")
        csv_editor_action.triggered.connect(self.on_csv_editor)

        global_search_icon = self.get_icon_for_page_type(global_search_page.GlobalSearchPage)
        global_search_action = self.tab_menu.addAction(global_search_icon, "Global Search")
        global_search_action.setToolTip("Search for text in all files of your mod.")
        global_search_action.setShortcut("Ctrl+Alt+F")
        global_search_action.setShortcutContext(Qt.WindowShortcut)
        global_search_action.triggered.connect(self.on_global_search)

        diff_icon = self.get_icon_for_page_type(diff_page.DiffPage)
        diff_action = self.tab_menu.addAction(diff_icon, "Diff Page")
        diff_action.setToolTip("Compare the files of your mod to another or the unmodded game files.")
        diff_action.triggered.connect(self.on_diff)

        guid_generator_icon = self.get_icon_for_page_type(guid_generator_page.GuidGeneratorPage)
        guid_generator_action = self.tab_menu.addAction(guid_generator_icon, "GUID Generator")
        guid_generator_action.setToolTip("Generate GUIDs (Globally Unique Identifiers), "
                                         "which are used in some NDF objects.")
        guid_generator_action.triggered.connect(self.on_guid_generator)

        self.tab_menu.addSeparator()

        game_settings_icon = self.get_icon_for_page_type(game_settings_page.GameSettingsPage)
        game_settings_action = self.tab_menu.addAction(game_settings_icon, "Game Settings Editor")
        game_settings_action.setToolTip("Edit available game settings such as starting points and income.")
        game_settings_action.triggered.connect(self.on_game_settings)

        script_runner_icon = self.get_icon_for_page_type(script_runner_page.ScriptRunnerPage)
        script_runner_action = self.tab_menu.addAction(script_runner_icon, "Script Runner")
        script_runner_action.setToolTip("Run predefined scripts to perform changes on your mod.")
        script_runner_action.triggered.connect(self.on_script_runner)

        div_editor_icon = self.get_icon_for_page_type(division_editor_page.DivisionEditorPage)
        div_editor_action = self.tab_menu.addAction(div_editor_icon, "Division Editor")
        div_editor_action.setToolTip("Edit available units and slots for a division.")
        div_editor_action.triggered.connect(self.on_div_editor)

        self.tab_menu.addSeparator()

        documentation_icon = icon_manager.load_icon("help.png", COLORS.PRIMARY)
        documentation_menu = self.tab_menu.addMenu(documentation_icon, "Help && Documentation")

        quickstart_action = documentation_menu.addAction("Quickstart Guide")
        quickstart_action.setToolTip("The Quickstart Guide walks you through the basics of using WME.")
        quickstart_action.triggered.connect(self.on_open_quickstart)
        ndf_reference_action = documentation_menu.addAction("NDF Reference")
        ndf_reference_action.setToolTip("The NDF Reference contains rules and conventions of the NDF language.")
        ndf_reference_action.triggered.connect(self.on_open_ndf_reference)
        # TODO: finish manual
        manual_action = documentation_menu.addAction("Shortcut Reference")
        manual_action.setToolTip("A list of available shortcuts.")
        manual_action.triggered.connect(self.on_open_manual)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_tab_close_pressed)
        self.setAcceptDrops(True)

        # make sure explorer isn't so big
        self.resize(1000, self.height())

    def to_json(self) -> list:
        json_obj = []
        for i in range(self.count()):
            page = self.widget(i)
            page_json = page.to_json()
            page_json["type"] = page.get_full_class_name()
            page_json["title"] = self.tabText(i)
            json_obj.append(page_json)
        return json_obj

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

    def get_icon_for_page_type(self, page_type):
        if not self.icon_paths_for_pages.__contains__(page_type):
            return icon_manager.load_icon("help.png", COLORS.PRIMARY)
        return icon_manager.load_icon(self.icon_paths_for_pages[page_type], COLORS.PRIMARY)

    def add_tab_with_auto_icon(self, page: base_tab_page.BaseTabPage, title: str):
        icon = self.get_icon_for_page_type(type(page))
        self.addTab(page, icon, title)

    def on_open_ndf_editor(self, file_path: str) -> ndf_editor_page.NdfEditorPage:
        file_path = file_path.replace("/", "\\")
        file_name = file_path[file_path.rindex('\\') + 1:]
        editor_icon = icon_manager.load_icon("text_editor.png", COLORS.PRIMARY)
        editor = ndf_editor_page.NdfEditorPage()
        self.addTab(editor, editor_icon, file_name)
        editor.open_file(file_path)
        editor.unsaved_changes = False
        return editor

    def on_open_and_find_ndf_editor(self, file_path: str, search_pattern: str, case_sensitive: bool):
        editor = self.on_open_ndf_editor(file_path)
        editor.find_action.setChecked(True)
        editor.find_bar.line_edit.setText(search_pattern)
        editor.find_bar.case_button.setChecked(case_sensitive)
        editor.code_editor.case_sensitive_search = case_sensitive
        editor.code_editor.find_pattern(search_pattern)

    def on_text_editor(self):
        editor = ndf_editor_page.NdfEditorPage()
        self.add_tab_with_auto_icon(editor, "Text Editor")
        editor.code_editor.setFocus()

    def on_open_csv_editor(self, file_path: str):
        file_path = file_path.replace("/", "\\")
        file_name = file_path[file_path.rindex('\\') + 1:]
        editor_icon = icon_manager.load_icon("edit_table.png", COLORS.PRIMARY)
        editor = csv_editor_page.CsvEditorPage()
        self.addTab(editor, editor_icon, file_name)
        editor.open_file(file_path)
        editor.unsaved_changes = False

    def on_csv_editor(self):
        editor = csv_editor_page.CsvEditorPage()
        self.add_tab_with_auto_icon(editor, "CSV Editor")

    def on_global_search(self):
        page = global_search_page.GlobalSearchPage()
        self.add_tab_with_auto_icon(page, "Global Search")
        page.search_line_edit.setFocus()

    def on_diff(self):
        page = diff_page.DiffPage()
        self.add_tab_with_auto_icon(page, "Diff Page")

    def on_guid_generator(self):
        page = guid_generator_page.GuidGeneratorPage()
        self.add_tab_with_auto_icon(page, "GUID Generator")

    def on_game_settings(self):
        page = game_settings_page.GameSettingsPage()
        self.add_tab_with_auto_icon(page, "Game Settings Editor")

    def on_open_quickstart(self):
        viewer = rich_text_viewer_page.RichTextViewerPage("Quickstart.html")
        self.add_tab_with_auto_icon(viewer, "Quickstart Guide")

    def on_open_ndf_reference(self):
        viewer = rich_text_viewer_page.RichTextViewerPage("NdfReference.html")
        self.add_tab_with_auto_icon(viewer, "NDF Reference")

    def on_open_manual(self):
        viewer = rich_text_viewer_page.RichTextViewerPage("UserManual.html")
        self.add_tab_with_auto_icon(viewer, "Shortcut Reference")

    def on_open_comparison(self, file_name, left_text, right_text, left_mod, right_mod, parser_based=False):
        main_widget.instance.show_loading_screen("Comparing files...")
        comp_page = file_comparison_page.FileComparisonPage()
        t = main_widget.instance.run_worker_thread(self.compare_files_task, file_name, left_text, right_text,
                                                   left_mod, right_mod, parser_based, comp_page)
        text = main_widget.instance.wait_for_worker_thread(t)
        self.add_tab_with_auto_icon(comp_page, text)
        main_widget.instance.hide_loading_screen()

    def compare_files_task(self, file_name, left_text, right_text, left_mod, right_mod, parser_based, comp_page):
        if parser_based:
            text = f"Parser-based Diff: {file_name}"
            try:
                left_text = parser_utils.round_trip(left_text)
            except Exception as e:
                logging.error(f"Error parsing text form file {file_name} of {left_mod}: {str(e)}")
                essential_dialogs.MessageDialog("Parser Error",
                                                f"Error parsing text form file {file_name} of {left_mod}").exec()
                main_widget.instance.hide_loading_screen()
                return
            try:
                right_text = parser_utils.round_trip(right_text)
            except Exception as e:
                logging.error(f"Error parsing text form file {file_name} of {right_mod}: {str(e)}")
                essential_dialogs.MessageDialog("Parser Error",
                                                f"Error parsing text form file {file_name} of {right_mod}").exec()
                main_widget.instance.hide_loading_screen()
                return
        else:
            text = f"Text Diff: {file_name}"

        comp_page.highlight_differences(left_text, right_text, left_mod, right_mod)
        return text

    def on_mod_config(self):
        page = mod_config_page.ModConfigPage()
        self.add_tab_with_auto_icon(page, "Mod Config")

    def on_script_runner(self):
        page = script_runner_page.ScriptRunnerPage()
        self.add_tab_with_auto_icon(page, "Script Runner")

    def on_div_editor(self):
        page = division_editor_page.DivisionEditorPage()
        self.add_tab_with_auto_icon(page, "Division Editor")

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
        # iterate through own tabs
        restore_list = []
        i = 0
        while i < self.count():
            page = self.widget(i)
            if not page.unsaved_changes:
                i += 1
                continue

            dialog = essential_dialogs.AskToSaveDialog(page.tab_name)
            result = dialog.exec()

            # don't close on cancel
            if not result == QtWidgets.QDialog.Accepted:
                return self.cancel_ask_all_tabs(restore_list)
            # on save
            elif dialog.save_changes:
                if not page.save_changes():
                    self.setTabText(i, self.tabText(i).removesuffix("(*)"))
                    restore_list.append(i)
                    return self.cancel_ask_all_tabs(restore_list)
            # on discard, remove tab
            else:
                self.setTabText(i, self.tabText(i).removesuffix("(*)"))
                restore_list.append(i)
            i += 1

        if all_windows:
            # call function on other windows
            for detached in wme_detached_tab.detached_list:
                if not detached.tab_widget.ask_all_tabs_to_save(False):
                    return self.cancel_ask_all_tabs(restore_list)

        # if cancel is never pressed, return True
        return True

    def cancel_ask_all_tabs(self, restore_list: list):
        for i in restore_list:
            self.widget(i).update_page()
        return False

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
