import openpyxl
from string import digits


class SheetManager:
    def __init__(self, xlsx_path: str, sheet_name: str, prefix: str):
        wb_obj = openpyxl.open(xlsx_path)
        self.sheet = wb_obj.get_sheet_by_name(sheet_name)

        self.object_name_to_index = {}

        # save row index for each object to be edited
        for i in range(2, self.sheet.max_row + 1):
            self.object_name_to_index[prefix + str(self.sheet.cell(row=i, column=1).value)] = i

        self.category_to_index = {}

        # save column index for each category
        for i in range(2, self.sheet.max_column + 1):
            self.category_to_index[str(self.sheet.cell(row=1, column=i).value)] = i

    def get_attribute_for_object(self, obj_name: str, attr_name: str):
        row = self.object_name_to_index[obj_name]
        column = self.category_to_index[attr_name]

        return self.sheet.cell(row=row, column=column).value

    def contains_object(self, obj_name: str):
        return self.object_name_to_index.__contains__(obj_name)


class SheetMultiManager:
    def __init__(self, xlsx_path: str, sheet_name: str, prefix: str):
        wb_obj = openpyxl.open(xlsx_path)
        self.sheet = wb_obj.get_sheet_by_name(sheet_name)

        self.object_name_to_index = {}

        # save row index for each object to be edited
        for i in range(2, self.sheet.max_row + 1):
            name = prefix + str(self.sheet.cell(row=i, column=1).value)
            if not self.object_name_to_index.__contains__(name):
                obj_index = 0
                self.object_name_to_index[name] = {}
            else:
                obj_index = len(self.object_name_to_index[name])
            self.object_name_to_index[name][obj_index] = i

        self.category_to_index = {}

        # save column index for each category
        for i in range(2, self.sheet.max_column + 1):
            self.category_to_index[str(self.sheet.cell(row=1, column=i).value)] = i

    def get_attribute_for_object(self, obj_name: str, attr_name: str, obj_index: int):
        row = self.object_name_to_index[obj_name][obj_index]
        column = self.category_to_index[attr_name]

        return self.sheet.cell(row=row, column=column).value

    def number_entries_for_object(self, obj_name: str):
        if not self.object_name_to_index.__contains__(obj_name):
            return 0
        return len(self.object_name_to_index[obj_name])


def edit_units_from_xlsx(unit_desc, xlsx_path: str = "Units.xlsx"):
    sheet_manager = SheetManager(xlsx_path, sheet_name="Units", prefix="Descriptor_Unit_")

    for unit in unit_desc:
        name = unit.namespace
        unit_obj = unit.value

        if not sheet_manager.contains_object(name):
            continue

        for module in unit_obj.by_member("ModulesDescriptors").value:
            # TODO: use type attribute here
            # set HP
            try:
                hp_module = module.value.by_member("Default").value.by_member("MaxPhysicalDamages")
                hp = int(sheet_manager.get_attribute_for_object(name, "hp"))
                hp_module.value = hp
            except Exception as e:
                pass
            # set armor
            try:
                armor_module = module.value.by_member("Default").value.by_member("BlindageProperties").value
                for aspect in ["Front", "Sides", "Rear", "Top"]:
                    armor_value = sheet_manager.get_attribute_for_object(name, aspect + "_armor_value")
                    if not armor_value:
                        continue
                    armor_type = sheet_manager.get_attribute_for_object(name, aspect + "_armor_type")
                    if not armor_type:
                        armor_type = armor_module.by_member("ArmorDescriptor" + aspect).value.rstrip(digits)
                    armor_module.by_member("ArmorDescriptor" + aspect).value = armor_type + str(armor_value)
            except Exception as e:
                pass
            # set price
            try:
                price_module = module.value.by_member("Default").value.by_member("ProductionRessourcesNeeded").value
                price = int(sheet_manager.get_attribute_for_object(name, "price"))
                price_module.by_key("~/Resource_CommandPoints").value = price
            except Exception as e:
                pass


# TODO: function to set ammo for given unit on given turret
def edit_turrets_from_xlsx(weapon_desc, xlsx_path: str = "Units.xlsx"):
    sheet_manager = SheetMultiManager(xlsx_path, sheet_name="Turrets", prefix="WeaponDescriptor_")

    for weapon in weapon_desc:
        name = weapon.namespace
        weapon_obj = weapon.value

        for i in range(sheet_manager.number_entries_for_object(name)):
            try:
                turret_index = int(sheet_manager.get_attribute_for_object(name, "turret_index", i))
                weapon_index = int(sheet_manager.get_attribute_for_object(name, "weapon_index", i))
            except TypeError:
                continue
            ammo = sheet_manager.get_attribute_for_object(name, "ammo_name", i)
            if not ammo:
                continue

            turret = weapon_obj.by_member("TurretDescriptorList").value[turret_index]
            mount = turret.value.by_member("MountedWeaponDescriptorList").value[weapon_index]
            mount.value.by_member("Ammunition").value = "~/Ammo_" + ammo


def edit_ammo_from_xlsx(ammo_desc, xlsx_path: str = "Units.xlsx"):
    sheet_manager = SheetManager(xlsx_path, sheet_name="Ammo", prefix="Ammo_")
