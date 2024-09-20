
class ScriptParameter:
    def __init__(self, key: str, name, description, d_type, default_value):
        self.key = key
        self.name = name
        self.description = description
        self.d_type = d_type
        self.default_value = default_value



class BaseScript:
    def __init__(self):
        self.parameters = [ScriptParameter]
        # to make sure page checks if files can be safely edited
        self.edited_files = []
        pass

    def run(self):
        # to be overwritten with actual script
        pass

    def add_parameter(self, param: ScriptParameter):
        # to be called in init, adds parameters to list
        # automatically setup widget based on type
        pass

    def get_parsed_ndf_file(self):
        # should use some function from parser utils
        pass
