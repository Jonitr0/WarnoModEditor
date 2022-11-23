# tab page that displays markdown files

from src.wme_widgets.tab_pages import tab_page_base


class MdViewerPage(tab_page_base.TabPageBase):
    def __init__(self, md_file_path):
        super().__init__()
