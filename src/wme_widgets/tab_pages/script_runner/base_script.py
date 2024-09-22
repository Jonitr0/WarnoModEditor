class ScriptParameter:
    def __init__(self, name: str, description: str, default_value):
        self.name = name
        self.description = description
        self.default_value = default_value


class BaseScript:
    def __init__(self):
        self.parameters: [ScriptParameter] = []
        # to make sure page checks if files can be safely edited
        self.edited_files: [str] = []
        # name displayed in script selector
        self.name = ""
        pass

    def run(self, parameter_values: dict):
        # to be overwritten with actual script
        pass

    def add_parameter(self, param: ScriptParameter):
        # to be called in init, adds parameters to list
        # automatically setup widget based on type
        pass

    def get_parsed_ndf_file(self):
        # should use some function from parser utils
        pass
