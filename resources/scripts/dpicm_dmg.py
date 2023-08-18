import ndf_parse as ndf
import math


def change_ammo_entry_to_dpicm(weapon_obj, heavy: bool = True, ap: int = 6, he: float = 1.0):
    weapon = weapon_obj.value

    weapon.by_member("Arme").value.by_member("Family").value = "'dpicm'"
    weapon.by_member("Arme").value.by_member("Index").value = ap
    weapon.by_member("PhysicalDamages").value = he

    if heavy:
        weapon.by_member("ImpactHappening").value[0].value = "'RoquetteM26M270227MmCluster'"
    else:
        weapon.by_member("ImpactHappening").value[0].value = "'Roquette110Mm130Mm'"


def create_dpicm_mlrs(ammo_desc, dmg_resist, ui_mouse, ui_weapon, terrain):
    dmg_type_expr = "TDamageTypeRTTI(Family=\"dpicm\" Index={index})"

    resist_types = dmg_resist[0].value[0]
    dmg_types = dmg_resist[0].value[1]
    dmg_values = dmg_resist[0].value[2]

    dpicm_dmg_values = []
    # create DPICM damage values
    for resist in resist_types.value:
        family = resist.value[0].value.removeprefix("\"").removesuffix("\"")
        index = int(resist.value[1].value)
        match family:
            case "batiment":
                dpicm_dmg_values.append(0.5)
            case "blindage":
                if index == 1:
                    dpicm_dmg_values.append(6)
                else:
                    dpicm_dmg_values.append(max(3.5 - 0.5 * index, 0.1))
            case "canon":
                dpicm_dmg_values.append(3)
            case "helico":
                dpicm_dmg_values.append(12 - 2 * index)
            case "infanterie":
                dpicm_dmg_values.append(3)
            case "vehicule":
                dpicm_dmg_values.append(10 / math.pow(2.0, index - 1))
            case "toit":
                dpicm_dmg_values.append(1)
            case "vehicule_leger":
                dpicm_dmg_values.append(3)
            case _:
                dpicm_dmg_values.append(0)

    dpicm_dmg_str = "["
    for val in dpicm_dmg_values:
        dpicm_dmg_str += str(val) + ", "
    dpicm_dmg_str += "]"

    dpicm_dmg_dict = ndf.expression(dpicm_dmg_str)

    cluster_index = -1
    for index, dmg in enumerate(dmg_types.value):
        family = dmg.value[0].value.removeprefix("\"").removesuffix("\"")
        if family == "cluster":
            cluster_index = index

    # max AP which DPICM rounds should have
    dpicm_index_count = 6
    for i in range(dpicm_index_count):
        dmg_type_dict = ndf.expression(dmg_type_expr.format(index=i + 1))
        dmg_types.value.insert(cluster_index + i, **dmg_type_dict)
        dmg_values.value.insert(cluster_index + i, **dpicm_dmg_dict)

    # add necessary UI modifications
    for obj_row in ui_mouse:
        obj = obj_row.value

        if obj.type == "TUIMouseWidgetSelector_Attack":
            ui_mouse_dict = {"key": "\"dpicm\"", "value": "\"TC_HE\""}
            obj.by_member("TextForDamageType").value.add(**ui_mouse_dict)
            break

    for obj_row in ui_weapon:
        obj = obj_row.value

        if obj_row.namespace == "DamageTypeComponentConfigurations":
            ui_weapon_txt = "TDamageComponentConfiguration (\n" \
                            "DamageType = \"dpicm\"\n" \
                            "Button = \"ClusterHEButton\"\n" \
                            "AmmoText = \"WeaponClusterHEAmmoText\"\n" \
                            "CalibreText = \"WeaponClusterHECalibreText\"\n" \
                            ")"
            ui_weapon_dict = ndf.expression(ui_weapon_txt)
            obj.add(**ui_weapon_dict)

    # add increased damage resistance for infantry in Terrains.ndf
    for terrain_row in terrain:
        name = terrain_row.namespace
        terrain_obj = terrain_row.value

        try:
            dmg_resistance = terrain_obj.by_member("DamageModifierPerFamilyAndResistance").value
        except Exception:
            continue

        resist_str = "MAP[(\"infanterie\",{value})]"

        match name:
            case "ForetDense":
                resist_str = resist_str.format(value=0.6)
            case "ForetLegere":
                resist_str = resist_str.format(value=0.7)
            case "PetitBatiment":
                resist_str = resist_str.format(value=0.3)
            case "Batiment":
                resist_str = resist_str.format(value=0.3)
            case "Ruin":
                resist_str = resist_str.format(value=0.5)
            case _:
                continue

        resist_dict = ndf.expression(resist_str)
        resist_dict["key"] = "'dpicm'"

        dmg_resistance.add(**resist_dict)

    for weapon_row in ammo_desc:
        name = weapon_row.namespace
        match name:
            case "Ammo_RocketArt_LARS_110mm_cluster":
                change_ammo_entry_to_dpicm(weapon_row, False, 3, 1.2)
            case "Ammo_RocketArt_M21OF_122mm_cluster":
                change_ammo_entry_to_dpicm(weapon_row, False, 3, 1)
            case "Ammo_RocketArt_M26_227mm_Cluster":
                change_ammo_entry_to_dpicm(weapon_row, True, 6, 2)
            case "Ammo_RocketArt_9M55K5_300mm":
                change_ammo_entry_to_dpicm(weapon_row, True, 6, 2)
            case _:
                pass
