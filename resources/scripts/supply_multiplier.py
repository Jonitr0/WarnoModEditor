from src.wme_widgets.tab_pages.script_runner.base_script import BaseScript


class SupplyMultiplier(BaseScript):
    def __init__(self):
        super().__init__()
        self.name = "Supply Multiplier"
        self.description = "Multiplies the supply of all supply units by a given factor. Edits UniteDescriptor.ndf"
        self.add_parameter("multiplier", "All supply values are multiplied by this amount", 2.0)

    def _run(self, parameter_values: dict):
        units = self.get_parsed_ndf_file(r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
        for logi_descr in units.match_pattern(
                "TEntityDescriptor(ModulesDescriptors = [TSupplyModuleDescriptor()])"
        ):
            descriptors = logi_descr.v.by_member("ModulesDescriptors").v  # get modules list
            supply_row = descriptors.find_by_cond(  # find supply module
                # safe way to check if row has type and equals the one we search for
                lambda x: getattr(x.v, "type", None) == "TSupplyModuleDescriptor"
            )
            # get capacity row
            supply_capacity_row = supply_row.v.by_member("SupplyCapacity")
            old_capacity = supply_capacity_row.v
            new_capacity = float(old_capacity) * parameter_values["multiplier"]
            # round to nearest integer
            new_capacity = float(round(new_capacity))
            supply_capacity_row.v = str(new_capacity)
