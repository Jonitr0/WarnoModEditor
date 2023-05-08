# TODO (0.3):
# TODO: Descriptor_Deck_US_11ACR_multi_HB_OP_01_DEP_PLAYER
# TODO: add Units to DivisionRules.ndf
# TODO: change Descriptor in Packs.ndf
# TODO: change availability in DeckCombatGroupList in Decks.ndf

# TODO: create NDF scanner to get top level assignment IDs

from src.wme_widgets.tab_pages.napo_pages import base_napo_page


class OperationEditor(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()
