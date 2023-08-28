import shutil

from hmg_ap_damage import *
from mlrs_rof_increase import *
from dpicm_dmg import *
from armor_rework import *
from adjust_units_from_xlsx import *

# TODO: tank armor rework
# TODO: vehicle mobility rework?
# TODO: model fixes (MGs on Leo 1s)
# TODO: optics rework for tanks

if __name__ == "__main__":
    src_mod = r"D:\SteamLibrary\steamapps\common\WARNO\Mods\SrcMod"
    #src_mod = r"C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\SrcMod"
    tgt_mod = r"D:\SteamLibrary\steamapps\common\WARNO\Mods\HmgApDmg"
    #tgt_mod = r"C:\Program Files (x86)\Steam\steamapps\common\WARNO\Mods\HmgApDmg"

    try:
        shutil.rmtree(tgt_mod)
    except Exception as e:
        print(e)

    mod = ndf.Mod(src_mod, tgt_mod)
    mod.check_if_src_is_newer()

    with mod.edit(r"GameData\Generated\Gameplay\Gfx\DamageResistance.ndf") as dmg_resist, \
            mod.edit(r"GameData\Generated\Gameplay\Gfx\Ammunition.ndf") as ammo_desc, \
            mod.edit(r"GameData\Generated\Gameplay\Gfx\WeaponDescriptor.ndf") as weapon_desc, \
            mod.edit(r"GameData\Generated\Gameplay\Gfx\ArmorDescriptor.ndf") as armor_desc, \
            mod.edit(r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf") as unit_desc, \
            mod.edit(r"GameData\UserInterface\Use\InGame\UIMousePolicyResources.ndf") as ui_mouse, \
            mod.edit(r"GameData\UserInterface\Use\InGame\UISpecificUnitInfoSingleWeaponPanelView.ndf") as ui_weapon, \
            mod.edit(r"GameData\Gameplay\Constantes\WeaponConstantes.ndf") as weapon_const, \
            mod.edit(r"GameData\Gameplay\Terrains\Terrains.ndf") as terrain:
        create_dpicm_mlrs(ammo_desc, dmg_resist, ui_mouse, ui_weapon, terrain)
        add_ap_to_hmgs(ammo_desc, weapon_desc)
        increase_mlrs_rof(ammo_desc, weapon_desc)
        create_era_resist_type(dmg_resist, armor_desc, weapon_const)
        edit_units_from_xlsx(unit_desc)
        edit_ammo_from_xlsx(ammo_desc)
        edit_turrets_from_xlsx(weapon_desc)
