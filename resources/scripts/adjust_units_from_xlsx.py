import openpyxl
from string import digits


class SheetManager:
    def __init__(self, xlsx_path: str, sheet_name: str = "Units"):
        wb_obj = openpyxl.open(xlsx_path)
        self.sheet = wb_obj.get_sheet_by_name(sheet_name)
        
        self.unit_name_to_index = {}

        # save row index for each unit to be edited
        for i in range(2, self.sheet.max_row + 1):
            self.unit_name_to_index["Descriptor_Unit_" + str(self.sheet.cell(row=i, column=1).value)] = i
    
        self.category_to_index = {}
    
        # save column index for each category
        for i in range(2, self.sheet.max_column + 1):
            self.category_to_index[str(self.sheet.cell(row=1, column=i).value)] = i

    def get_attribute_for_unit(self, unit_name: str, attr_name: str):
        row = self.unit_name_to_index[unit_name]
        column = self.category_to_index[attr_name]

        return self.sheet.cell(row=row, column=column).value

    def contains_unit(self, unit_name: str):
        return self.unit_name_to_index.__contains__(unit_name)


def edit_units_from_xlsx(unit_desc, xlsx_path: str = "Units.xlsx"):
    sheet_manager = SheetManager(xlsx_path)

    for unit in unit_desc:
        name = unit.namespace
        unit_obj = unit.value

        if not sheet_manager.contains_unit(name):
            continue

        for module in unit_obj.by_member("ModulesDescriptors").value:
            # set HP
            try:
                hp_module = module.value.by_member("Default").value.by_member("MaxPhysicalDamages")
                hp = int(sheet_manager.get_attribute_for_unit(name, "hp"))
                hp_module.value = hp
            except Exception as e:
                pass
            # set armor
            try:
                armor_module = module.value.by_member("Default").value.by_member("BlindageProperties").value
                for aspect in ["Front", "Sides", "Rear", "Top"]:
                    armor_value = sheet_manager.get_attribute_for_unit(name, aspect + "_armor_value")
                    if not armor_value:
                        continue
                    armor_type = sheet_manager.get_attribute_for_unit(name, aspect + "_armor_type")
                    if not armor_type:
                        armor_type = armor_module.by_member("ArmorDescriptor" + aspect).value.rstrip(digits)
                    armor_module.by_member("ArmorDescriptor" + aspect).value = armor_type + str(armor_value)
                print(module)
            except Exception as e:
                pass


