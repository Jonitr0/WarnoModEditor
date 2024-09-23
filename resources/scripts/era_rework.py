from src.wme_widgets.tab_pages.script_runner.base_script import BaseScript

import ndf_parse as ndf


class EraRework(BaseScript):
    def __init__(self):
        super().__init__()
        self.name = "ERA Rework"
        self.description = ("Redone damage calculation for explosive reactive armor (ERA). ERA-equipped vehicles will "
                            "now have a damage reduction for incoming HEAT munitions from the front and side instead "
                            "of an HP increase. Tandem weapons will negate this damage reduction. Edits "
                            "UniteDescriptor.ndf, AmmunitionMissiles.ndf and DamageResistance.ndf.")

    def _run(self, parameter_values: dict):
        # edit DamageResistance.ndf
        dmg_resist_obj = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\DamageResistance.ndf")
        # get armor types
        resistance_families = dmg_resist_obj[0].value.by_member("ResistanceFamilyDefinitionList").value
        # add ERA resistance family to list after ResistanceFamily_blindage
        blindage_index = -1
        era_resist_type_str = ""
        for i, resist_type in enumerate(resistance_families):
            if resist_type.value.by_member("Family").value == "ResistanceFamily_blindage":
                # create ERA resistance family as ndf
                era_resist_type_str = (f"TResistanceTypeFamilyDefinition"
                                       f"("
                                       f"Family = ResistanceFamily_ERA"
                                       f"MaxIndex = {resist_type.value.by_member('MaxIndex').value}"
                                       f")"
                                       ),

                blindage_index = i
                break
        resistance_families.insert(blindage_index + 1, era_resist_type_str)

        # get damage types
        dmg_types = dmg_resist_obj[0].value.by_member("DamageFamilyDefinitionList").value
        # add tandem damage family to list after DamageFamily_ap_missile
        ap_missile_index = -1
        tandem_dmg_type_str = ""
        for i, dmg_type in enumerate(dmg_types):
            if dmg_type.value.by_member("Family").value == "DamageFamily_ap_missile":
                # create tandem damage family as ndf
                tandem_dmg_type_str = (f"TDamageTypeFamilyDefinition"
                                       f"("
                                       f"Family = DamageFamily_tandem"
                                       f"MaxIndex = {dmg_type.value.by_member('MaxIndex').value}"
                                       f")"
                                       ),

                ap_missile_index = i
                break
        dmg_types.insert(ap_missile_index + 1, tandem_dmg_type_str)

        # TODO: edit WeaponConstants, ResistLists
        # TODO: add armor type to unit descriptors, remove reactive flag
        # TODO: add tandem type to tandem weapons, remove tandem flag
