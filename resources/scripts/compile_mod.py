from hmg_ap_damage import *
from mlrs_rof_increase import *

if __name__ == "__main__":
    src_mod = r"D:\SteamLibrary\steamapps\common\WARNO\Mods\SrcMod"
    tgt_mod = r"D:\SteamLibrary\steamapps\common\WARNO\Mods\HmgApDmg"

    mod = ndf.Mod(src_mod, tgt_mod)
    mod.check_if_src_is_newer()

    with mod.edit(r"GameData\Generated\Gameplay\Gfx\Ammunition.ndf") as ammo_desc, \
            mod.edit(r"GameData\Generated\Gameplay\Gfx\WeaponDescriptor.ndf") as weapon_descs:
        add_ap_to_hmgs(ammo_desc, weapon_descs)
        increase_mlrs_rof(ammo_desc, weapon_descs)
