from src.wme_widgets.tab_pages.script_runner.base_script import BaseScript

import re


class RangeScaling(BaseScript):
    def __init__(self):
        super().__init__()
        self.name = "Range Scaling"
        self.description = "Changes the scale of LBUs (Level Build Units; actual size of units and maps) to GRUs " \
                           "(Game Range Units; weapon ranges, line of sight tool,...). A gru_multiplier of 2 for " \
                           "example makes it that 2 meters of weapon range correspond to 1 meter of actual terrain. " \
                           "The default factor used in Warno is about 2.9. Be aware that some game mechanics might" \
                           " not work as intended anymore if the factor too low or too high. " \
                           "Edits InitialisationGameDistanceUnits.ndf"
        self.add_parameter("gru_multiplier", "All weapon ranges and vision distances are scaled by this amount",
                           2.92198967)

    def _run(self, parameter_values: dict):
        distance_units = self.get_parsed_ndf_file(r"CommonData\Gameplay\Constantes\InitialisationGameDistanceUnits.ndf")
        obj_str = distance_units[0].v
        # replace assignment by regex
        goal_str = f"LBUToGRUConversionFactor = {parameter_values['gru_multiplier']}"
        obj_str = re.sub("LBUToGRUConversionFactor = \d+\.?\d*", goal_str, obj_str)
        distance_units[0].v = obj_str
