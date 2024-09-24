import logging

from src.wme_widgets.tab_pages.script_runner.base_script import BaseScript


class EraRework(BaseScript):
    def __init__(self):
        super().__init__()
        self.name = "ERA Rework"
        self.description = ("Redone damage calculation for explosive reactive armor (ERA). ERA-equipped vehicles will "
                            "now have a damage reduction for incoming HEAT munitions from the front and side instead "
                            "of an HP increase. Tandem weapons will negate this damage reduction. Edits the following "
                            "files:\n- DamageResistance.ndf\n- WeaponConstantes.ndf\n")

    def _run(self, parameter_values: dict):
        # load DamageResistance.ndf read-only
        dmg_resist_obj = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\DamageResistance.ndf",
                                                  save=False)
        resistance_families = dmg_resist_obj[0].value.by_member("ResistanceFamilyDefinitionList").value
        # check if ERA resistance family already exists
        if any(resist_type.value.by_member("Family").value == "ResistanceFamily_ERA"
                for resist_type in resistance_families):
            logging.info("ERA resistance family already in DamageResistance.ndf, skipping")
        else:
            self.adjust_damage_resistance()

        weapon_constants = self.get_parsed_ndf_file(r"GameData\Gameplay\Constantes\WeaponConstantes.ndf",
                                                    save=False)[0].value
        if any(fam.value == "ResistanceFamily_ERA" for fam in
               weapon_constants.by_member("ResistanceFamiliesNeedPiercing").value):
            logging.info("ERA resistance family already in WeaponConstantes.ndf, skipping")
        else:
            self.adjust_weapon_constants()

        # TODO: edit ResistLists
        # TODO: add armor type to unit descriptors, remove reactive flag
        # TODO: add tandem type to tandem weapons, remove tandem flag

    def adjust_damage_resistance(self):
        dmg_resist_obj = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\DamageResistance.ndf")
        resistance_families = dmg_resist_obj[0].value.by_member("ResistanceFamilyDefinitionList").value
        # add ERA resistance family to list
        blindage_index = -1
        blindage_count = 0
        for i, resist_type in enumerate(resistance_families):
            if resist_type.value.by_member("Family").value == "ResistanceFamily_blindage":
                blindage_index = i
                blindage_count = int(resist_type.value.by_member("MaxIndex").value)
                break
            else:
                blindage_index += int(resist_type.value.by_member("MaxIndex").value)
        era_resist_type_str = (f"TResistanceTypeFamilyDefinition\n "
                               f"(\n "
                               f"Family = ResistanceFamily_ERA\n "
                               f"MaxIndex = {blindage_count}\n "
                               f")"
                               ),
        resistance_families.add(era_resist_type_str)

        # get damage types
        dmg_types = dmg_resist_obj[0].value.by_member("DamageFamilyDefinitionList").value
        # add tandem damage family to list
        ap_missile_index = -1
        ap_missile_count = 0
        for i, dmg_type in enumerate(dmg_types):
            if dmg_type.value.by_member("Family").value == "DamageFamily_ap_missile":
                ap_missile_index = i
                ap_missile_count = int(dmg_type.value.by_member("MaxIndex").value)
                break
            else:
                ap_missile_index += int(dmg_type.value.by_member("MaxIndex").value)

        # create tandem damage family as ndf
        tandem_dmg_type_str = (f"TDamageTypeFamilyDefinition\n "
                               f"(\n "
                               f"Family = DamageFamily_tandem\n "
                               f"MaxIndex = {ap_missile_count}\n "
                               f")"
                               ),
        dmg_types.add(tandem_dmg_type_str)

        # get damage matrix
        dmg_matrix = dmg_resist_obj[0].value.by_member("Values").value
        # copy each entry in the ap_missile range to the end (tandem damage)
        for i, dmg_vals in enumerate(dmg_matrix):
            if ap_missile_index <= i < ap_missile_index + ap_missile_count:
                dmg_matrix.add(dmg_vals)
            elif i >= ap_missile_index + ap_missile_count:
                break
        # for each entry, copy the values from the range of blindage to the end (ERA resistance)
        for i, dmg_vals in enumerate(dmg_matrix):
            for j, val in enumerate(dmg_vals.value):
                if blindage_index <= j < blindage_index + blindage_count:
                    if ap_missile_index <= i < ap_missile_index + ap_missile_count:
                        val.value = str(max(1.0, float(val.value) - 1.0))
                    dmg_vals.value.add(val)

    def adjust_weapon_constants(self):
        weapon_constants = self.get_parsed_ndf_file(r"GameData\Gameplay\Constantes\WeaponConstantes.ndf")[0].value
        weapon_constants.by_member("ResistanceFamiliesNeedPiercing").value.add("ResistanceFamily_ERA")
        ignore_armor = weapon_constants.by_member("BlindagesToIgnoreForDamageFamilies").value
        for row in ignore_armor:
            row.value.add("ResistanceFamily_ERA")
