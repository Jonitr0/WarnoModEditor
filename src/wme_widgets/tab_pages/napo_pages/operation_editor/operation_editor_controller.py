from src.wme_widgets.tab_pages.napo_pages import base_napo_controller


class OperationEditorController(base_napo_controller.BaseNapoController):
    def load_state_from_file(self) -> dict:
        # Decks.ndf: get units in battle group
        # DeckRules.ndf: get enemy units
        pass

    def write_state_to_file(self, state: dict):
        # Decks.ndf: save units in battle group
        # DeckRules.ndf: save enemy units
        # DivisionCostMatrix.ndf: adjust if needed
        # Packs.ndf: save availability constraints
        # Divisions.ndf: ?
        # DivisionRules.ndf: ?
        pass
