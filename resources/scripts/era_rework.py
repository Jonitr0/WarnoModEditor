import logging

import ndf_parse as ndf

from src.wme_widgets.tab_pages.script_runner.base_script import BaseScript


class EraRework(BaseScript):
    def __init__(self):
        super().__init__()
        self.name = "ERA Rework"
        self.description = ("Redone damage calculation for explosive reactive armor (ERA). ERA-equipped vehicles will "
                            "now have a damage reduction for incoming HEAT munitions from the front and side instead "
                            "of an HP increase. Tandem weapons will negate this damage reduction. Edits the following "
                            "files:\n- DamageResistance.ndf\n- WeaponConstantes.ndf\n- DamageResistanceFamilyList.ndf"
                            "\n- DamageResistanceFamilyListImpl.ndf\n- UIMousePolicyResources.ndf"
                            "\n- UIInGameUnitLabelResources.ndf\n- WeaponTypePriorities.ndf\n- UniteDescriptor.ndf"
                            "\n- Ammunition.ndf\n- AmmunitionMissiles.ndf")

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

        resist_lists = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\DamageResistanceFamilyList.ndf",
                                                save=False)
        if self.get_number_of_objects_by_prefix("ResistanceFamily_ERA", resist_lists) > 0:
            logging.info("ERA resistance family already in DamageResistanceFamilyList.ndf, skipping")
        else:
            self.adjust_resist_lists()

        resist_lists_impl = self.get_parsed_ndf_file(
            r"GameData\Generated\Gameplay\Gfx\DamageResistanceFamilyListImpl.ndf", save=False).by_namespace(
            "Generated_ResistanceFamily_Enum").value.by_member("Values").value
        if any(obj.value == "\"ResistanceFamily_ERA\"" for obj in resist_lists_impl):
            logging.info("ERA resistance family already in DamageResistanceFamilyListImpl.ndf, skipping")
        else:
            self.adjust_resist_lists_impl()

        ui_mouse_policy = self.get_parsed_ndf_file(
            r"GameData\UserInterface\Use\Ingame\UIMousePolicyResources.ndf", save=False).by_namespace(
            "MouseWidgetSelector_Attack").value.by_member("TextForDamageType").value
        if any(obj.key == "DamageFamily_tandem" for obj in ui_mouse_policy):
            logging.info("Tandem damage family already in UIMousePolicyResources.ndf, skipping")
        else:
            self.adjust_ui_mouse_policy()

        ui_unit_resources = self.get_parsed_ndf_file(
            r"GameData\UserInterface\Use\Ingame\UIInGameUnitLabelResources.ndf", save=False).by_namespace(
            "SpecificInGameUnitLabelResources").value.by_member("DamageTypeNameToFeedbackType").value
        if any(obj.key == "DamageFamily_tandem" for obj in ui_unit_resources):
            logging.info("Tandem damage family already in UIInGameUnitLabelResources.ndf, skipping")
        else:
            self.adjust_ui_unit_resources()

        weapon_type_priorities = self.get_parsed_ndf_file(
            r"GameData\Gameplay\Constantes\WeaponTypePriorities.ndf", save=False).by_namespace(
            "WeaponTypePriorities").value.by_member("WeaponTypes").value
        if any(obj.value.__contains__("DamageFamily_tandem") for obj in weapon_type_priorities):
            logging.info("Tandem weapon type already in WeaponTypePriorities.ndf, skipping")
        else:
            self.adjust_weapon_type_priorities()

        self.adjust_units()
        self.adjust_weapons()

    def adjust_damage_resistance(self):
        dmg_resist_obj = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\DamageResistance.ndf")
        resistance_families = dmg_resist_obj[0].value.by_member("ResistanceFamilyDefinitionList").value
        # add ERA resistance family to list
        blindage_index = -1
        blindage_count = 0
        for i, resist_type in enumerate(resistance_families):
            if resist_type.value.by_member("Family").value == "ResistanceFamily_blindage":
                blindage_index += 1
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
                ap_missile_index += 1
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
                dmg_matrix.add(dmg_vals.copy())
            elif i >= ap_missile_index + ap_missile_count:
                break
        # for each entry, copy the values from the range of blindage to the end (ERA resistance)
        for i, dmg_vals in enumerate(dmg_matrix):
            for j, val in enumerate(dmg_vals.value):
                if blindage_index <= j < blindage_index + blindage_count:
                    val = val.copy()
                    if ap_missile_index <= i < ap_missile_index + ap_missile_count:
                        val.value = str(max(1.0, float(val.value) - 1.0))
                    dmg_vals.value.add(val)

    def adjust_weapon_constants(self):
        weapon_constants = self.get_parsed_ndf_file(r"GameData\Gameplay\Constantes\WeaponConstantes.ndf")[0].value
        weapon_constants.by_member("ResistanceFamiliesNeedPiercing").value.add("ResistanceFamily_ERA")
        ignore_armor = weapon_constants.by_member("BlindagesToIgnoreForDamageFamilies").value
        for row in ignore_armor:
            row.value.add("ResistanceFamily_ERA")

    def adjust_resist_lists(self):
        resist_lists = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\DamageResistanceFamilyList.ndf")
        resist_count = self.get_number_of_objects_by_prefix("ResistanceFamily_", resist_lists)
        era_str = f"ResistanceFamily_ERA is {resist_count}"
        dmg_count = self.get_number_of_objects_by_prefix("DamageFamily_", resist_lists)
        tandem_str = f"DamageFamily_tandem is {dmg_count}"
        resist_lists.add(era_str)
        resist_lists.add(tandem_str)

    def get_number_of_objects_by_prefix(self, prefix: str, obj_list: list) -> int:
        count = 0
        for obj in obj_list:
            if obj.namespace.startswith(prefix):
                count += 1
        return count

    def adjust_resist_lists_impl(self):
        resist_lists_impl = self.get_parsed_ndf_file(
            r"GameData\Generated\Gameplay\Gfx\DamageResistanceFamilyListImpl.ndf")
        for obj in resist_lists_impl:
            if obj.namespace == "Generated_ResistanceFamily_Enum":
                obj.value.by_member("Values").value.add("\"ResistanceFamily_ERA\"")
            if obj.namespace == "Generated_DamageFamily_Enum":
                obj.value.by_member("Values").value.add("\"DamageFamily_tandem\"")

    def adjust_ui_mouse_policy(self):
        ui_mouse_policy = self.get_parsed_ndf_file(
            r"GameData\UserInterface\Use\Ingame\UIMousePolicyResources.ndf")
        for obj in ui_mouse_policy:
            if obj.namespace == "MouseWidgetSelector_Attack":
                obj.value.by_member("TextForDamageType").value.add("(DamageFamily_tandem, \"TC_HEAT\")")
                break

    def adjust_ui_unit_resources(self):
        ui_unit_resources = self.get_parsed_ndf_file(
            r"GameData\UserInterface\Use\Ingame\UIInGameUnitLabelResources.ndf")
        for obj in ui_unit_resources:
            if obj.namespace == "SpecificInGameUnitLabelResources":
                obj.value.by_member("DamageTypeNameToFeedbackType").value.add(
                    "(DamageFamily_tandem, ~/InGameUnitLabelUpdateFeedbackType/Missile)")
                break

    def adjust_weapon_type_priorities(self):
        weapon_type_priorities = self.get_parsed_ndf_file(
            r"GameData\Gameplay\Constantes\WeaponTypePriorities.ndf")
        for obj in weapon_type_priorities:
            if obj.namespace == "WeaponTypePriorities":
                obj.value.by_member("WeaponTypes").value.add("(DamageFamily_tandem, EWeaponRangeDependant/NotDefined)")
                break

    def adjust_units(self):
        units = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
        for unit in units:
            # get TUnitUIModuleDescriptor
            try:
                ui_module = unit.value.by_member("ModulesDescriptors").value.find_by_cond(
                    lambda m: type(m.value) == ndf.model.Object and m.value.type == "TUnitUIModuleDescriptor")
            except Exception:
                continue
            for trait in ui_module.value.by_member("SpecialtiesList").value:
                if trait.value == "\'_era\'":
                    # set health to 10
                    dmg_module = unit.value.by_member("ModulesDescriptors").value.find_by_cond(
                        lambda m: type(m.value) == ndf.model.Object and m.value.type == "TBaseDamageModuleDescriptor")
                    dmg_module.value.by_member("MaxPhysicalDamages").value = "10"
                    # set armor family to ERA
                    armor_module = unit.value.by_member("ModulesDescriptors").value.find_by_cond(
                        lambda m: type(m.value) == ndf.model.Object and
                                m.value.type == "TDamageModuleDescriptor").value.by_member("BlindageProperties")
                    armor_module.value.by_member("ResistanceFront").value.by_member("Family").value = \
                        "ResistanceFamily_ERA"
                    armor_module.value.by_member("ResistanceSides").value.by_member("Family").value = \
                        "ResistanceFamily_ERA"
                    # Remove Eugen ERA trait
                    armor_module.value.by_member("ExplosiveReactiveArmor").value = "False"
                    break

    def adjust_weapons(self):
        weapons = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\Ammunition.ndf")
        missiles = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\AmmunitionMissiles.ndf")
        self.adjust_weapons_list(weapons)
        self.adjust_weapons_list(missiles)

    def adjust_weapons_list(self, w_list):
        for wpn in w_list.match_pattern("TAmmunitionDescriptor(TandemCharge = True)"):
            wpn.value.by_member("Arme").value.by_member("Family").value = "DamageFamily_tandem"
            wpn.value.by_member("TandemCharge").value = "False"
