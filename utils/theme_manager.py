from utils import settings_manager

themes = dict(dark="dark_lightgreen.xml", light="light_lightgreen.xml")


def get_all_themes():
    return list(themes.keys())


def get_theme_file(theme_name: str):
    if not themes.__contains__(theme_name):
        settings_manager.write_settings_value(settings_manager.THEME_KEY, "dark")
        return "resources/" + themes["dark"], False
    invert_secondary = False
    if themes[theme_name].startswith("light"):
        invert_secondary = True
    return "resources/" + themes[theme_name], invert_secondary
