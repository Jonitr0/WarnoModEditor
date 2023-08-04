import ndf_parse as ndf
import math


def increase_mlrs_rof(ammo_desc, weapon_desc):
    # list of all MLRS which need salvo size adjustment
    double_salvo_length_list = ["Ammo_RocketArt_M21OF_122mm", "Ammo_RocketArt_M21OF_122mm_cluster",
                                "Ammo_RocketArt_M21OF_122mm_napalm"]
    # list of all "low caliber" MLRS which get higher RoF
    light_mlrs_list = double_salvo_length_list + ["Ammo_RocketArt_LARS_110mm", "Ammo_RocketArt_LARS_110mm_cluster",
                                                  "Ammo_RocketArt_M21OF_122mm_x12"]
    # list of all units to be skipped
    skip_list = ["Ammo_RocketArt_thermobaric_220mm", "Ammo_RocketArt_thermobaric_220mm_x30"]

    for obj_row in ammo_desc:
        obj = obj_row.value

        # skip anything that is not of this type
        if obj.type != "TAmmunitionDescriptor":
            continue

        # find all MLRS
        category = obj.by_member("TypeCategoryName").value
        if category == "'LTMWHXRDRX'":
            name = obj_row.namespace
            if skip_list.__contains__(name):
                continue
            if light_mlrs_list.__contains__(name):
                obj.by_member("TempsEntreDeuxTirs").value = 0.7
                obj.by_member("TempsEntreDeuxFx").value = 0.7
            else:
                obj.by_member("TempsEntreDeuxTirs").value = 1.4
                obj.by_member("TempsEntreDeuxFx").value = 1.4

            if double_salvo_length_list.__contains__(name):
                ammo_count = int(obj.by_member("NbTirParSalves").value)
                obj.by_member("NbTirParSalves").value = ammo_count * 2
                obj.by_member("AffichageMunitionParSalve").value = ammo_count * 2
                supply_cost = int(obj.by_member("SupplyCost").value)
                obj.by_member("SupplyCost").value = supply_cost * 2

    for obj_row in weapon_desc:
        obj = obj_row.value

        # skip anything that is not of this type
        if obj.type != "TWeaponManagerModuleDescriptor":
            continue

        # search for edited weapon
        turret_list = obj.by_member("TurretDescriptorList").value
        for turret in turret_list:
            mount_list = turret.value.by_member("MountedWeaponDescriptorList").value
            for mount in mount_list:
                ammo_name = mount.value.by_member("Ammunition").value.removeprefix("~/")
                if double_salvo_length_list.__contains__(ammo_name):
                    index = int(mount.value.by_member("SalvoStockIndex").value)
                    salvos = int(obj.by_member("Salves").value[index].value)
                    obj.by_member("Salves").value[index].value = salvos / 2


def create_dpicm_mlrs(ammo_desc, dmg_resist, ui_mouse, ui_weapon):
    # create "ATACMS" for testing
    for obj_row in ammo_desc:
        obj = obj_row.value

        # skip anything that is not of this type
        if obj.type != "TAmmunitionDescriptor":
            continue
        name = obj_row.namespace
        if name == "Ammo_RocketArt_M26_227mm_Cluster":
            # set Arme to cluster
            obj.by_member("Arme").value.by_member("Family").value = "\"dpicm\""
            obj.by_member("Arme").value.by_member("Index").value = 6

            obj.by_member("TempsEntreDeuxTirs").value = 60.0
            obj.by_member("TempsEntreDeuxFx").value = 60.0

            obj.by_member("DispersionAtMaxRange").value = "((100) * Metre)"
            obj.by_member("DispersionAtMinRange").value = "((100) * Metre)"

            obj.by_member("NbTirParSalves").value = 2
            obj.by_member("AffichageMunitionParSalve").value = 2

            obj.by_member("PhysicalDamages").value = 3

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
                dpicm_dmg_values.append(0.1)
            case "blindage":
                if index == 1:
                    dpicm_dmg_values.append(5)
                elif index < 7:
                    dpicm_dmg_values.append(3.5 - 0.5 * index)
                else:
                    dpicm_dmg_values.append(0.1)
            case "canon":
                dpicm_dmg_values.append(3)
            case "helico":
                dpicm_dmg_values.append(12 - 2 * index)
            case "infanterie":
                dpicm_dmg_values.append(3)
            case "vehicule":
                dpicm_dmg_values.append(10 / math.pow(2.0, index - 1))
            case "toit":
                dpicm_dmg_values.append(18 - 6 * index)
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
    
