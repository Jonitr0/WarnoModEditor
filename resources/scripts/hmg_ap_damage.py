import ndf_parse as ndf
import uuid


def create_ap_ammo_entry(orig, ap_value):
    # copy original
    orig_text = ndf.printer.string(orig)
    weapon_obj = ndf.convert(orig_text)[0]

    # change entry name
    new_name = weapon_obj.namespace.replace("Ammo_", "Ammo_AP_")
    weapon_obj.namespace = new_name
    weapon = weapon_obj.value

    # set UI min max category
    weapon.by_member("MinMaxCategory").value = "MinMax_AutocanonHE"

    # generate new GUID
    guid = "GUID:{" + str(uuid.uuid4()) + "}"
    weapon.by_member("DescriptorId").value = guid

    # set Arme
    weapon.by_member("Arme").value.by_member("Family").value = "\"ap\""
    weapon.by_member("Arme").value.by_member("Index").value = ap_value

    # set anti-helo/plane range to 0
    weapon.by_member("PorteeMinimaleTBA").value = "((0) * Metre)"
    weapon.by_member("PorteeMaximaleTBA").value = "((0) * Metre)"
    weapon.by_member("PorteeMinimaleHA").value = "((0) * Metre)"
    weapon.by_member("PorteeMaximaleHA").value = "((0) * Metre)"

    # set damage
    weapon.by_member("RadiusSplashPhysicalDamages").value = "0 * Metre"
    weapon.by_member("PhysicalDamages").value = 1.0
    weapon.by_member("ShowDamageInUI").value = False

    # set suppression
    old_sup_radius = float(weapon.by_member("RadiusSplashSuppressDamages").value.removesuffix(" * Metre"))
    weapon.by_member("RadiusSplashSuppressDamages").value = old_sup_radius * 4.0
    old_sup_dmg = float(weapon.by_member("SuppressDamages").value)
    weapon.by_member("SuppressDamages").value = old_sup_dmg / 2.0

    # hit roll descriptor
    hit_roll_desc = weapon.by_member("HitRollRuleDescriptor").value
    guid = "GUID:{" + str(uuid.uuid4()) + "}"
    hit_roll_desc.by_member("DescriptorId").value = guid
    hit_roll_desc.by_member("BaseCriticModifier").value = 0
    weapon.by_member("HitRollRuleDescriptor").value = hit_roll_desc

    # misc
    weapon.by_member("CanShootOnPosition").value = False
    weapon.by_member("FireDescriptor").value = "nil"
    weapon.by_member("IsHarmlessForAllies").value = True
    weapon.by_member("PiercingWeapon").value = True
    weapon.by_member("DamageTypeEvolutionOverRangeDescriptor").value = "~/DamageTypeEvolutionOverRangeDescriptor_DCA"

    weapon_obj.value = weapon
    return weapon_obj


def create_ap_mount(orig):
    # copy original
    orig_text = ndf.printer.string(orig)
    turret_obj = ndf.convert(orig_text)[0]
    turret = turret_obj.value

    # set new ammunition
    new_name = turret.by_member("Ammunition").value.replace("Ammo_", "Ammo_AP_")
    turret.by_member("Ammunition").value = new_name

    turret_obj.value = turret
    return turret_obj


def add_ap_to_hmgs(ammo_desc, weapon_desc):
    cal_127_tokens = ["'XBOZOTODIF'", "'XROPZVJKKE'", "'VXYLWCZLCA'"]
    cal_145_tokens = ["'PBJYEGALCO'"]

    weapons = {}

    # get all 12.7/14.5mm weapons and add AP descriptors for them
    for obj_row in ammo_desc:
        obj = obj_row.value

        # skip anything that is not of this type
        if obj.type != "TAmmunitionDescriptor":
            continue

        # get all weapons with relevant caliber
        caliber = obj.by_member("Caliber").value
        if cal_145_tokens.__contains__(caliber) or cal_127_tokens.__contains__(caliber):
            weapons[obj_row.namespace] = obj_row

    # add new AP ammo entries
    for weapon_obj in weapons.values():
        ap_val = 2
        caliber = weapon_obj.value.by_member("Caliber").value
        if cal_145_tokens.__contains__(caliber):
            ap_val = 3
        ap_ammo = create_ap_ammo_entry(weapon_obj, ap_val)
        ammo_desc.append(ap_ammo)

    # add new TMountedWeaponDescriptor to each TWeaponManagerModuleDescriptor with a 12.7/14.5mm weapon
    # TODO: some sound effects not working
    for obj_row in weapon_desc:
        obj = obj_row.value

        # skip anything that is not of this type
        if obj.type != "TWeaponManagerModuleDescriptor":
            continue

        # get all relevant mounts
        turret_list = obj.by_member("TurretDescriptorList").value
        for turret in turret_list:
            mount_list = turret.value.by_member("MountedWeaponDescriptorList").value
            for index, mount in enumerate(mount_list):
                ammo_name = mount.value.by_member("Ammunition").value.removeprefix("~/")
                if weapons.__contains__(ammo_name):
                    ap_mount = create_ap_mount(mount).value
                    ap_mount.parent = None
                    mount_list.insert(index, value=ap_mount)
                    break
