

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


def create_dpicm_mlrs(ammo_desc, dmg_resist):
    # create "ATACMS" for testing
    for obj_row in ammo_desc:
        obj = obj_row.value

        # skip anything that is not of this type
        if obj.type != "TAmmunitionDescriptor":
            continue
        name = obj_row.namespace
        if name == "Ammo_RocketArt_M26_227mm_Cluster":
            # set Arme to cluster
            obj.by_member("Arme").value.by_member("Family").value = "\"cluster\""
            obj.by_member("Arme").value.by_member("Index").value = 1

            obj.by_member("TempsEntreDeuxTirs").value = 60.0
            obj.by_member("TempsEntreDeuxFx").value = 60.0

            obj.by_member("DispersionAtMaxRange").value = "((100) * Metre)"
            obj.by_member("DispersionAtMinRange").value = "((100) * Metre)"

            obj.by_member("NbTirParSalves").value = 2
            obj.by_member("AffichageMunitionParSalve").value = 2

            obj.by_member("PhysicalDamages").value = 3

    resist_types = dmg_resist[0].value[0]
    # max AP which DPICM rounds should have
    dpicm_index_count = 6
    for i in range(dpicm_index_count):
        # TODO: create TDamageTypeRTTI for DamageTypeList and array for Values
        pass

    # TODO: add new entry to DamageTypeList
    # TODO: add array to Values: each entry corresponds to one ResistanceTypeList
    # TODO: for some reason, DamageResistance.ndf should be edited/saved last
