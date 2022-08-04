from src.utils import settings_manager

themes = {
    "light green": "dark_lightgreen.xml",
    #"light light green": "light_lightgreen.xml",
    "amber": "dark_amber.xml",
    #"light amber": "light_amber.xml",
    "purple": "dark_purple.xml",
    #"light purple": "light_purple.xml",
    "cyan": "dark_cyan.xml",
    #"light cyan": "light_cyan.xml",
}


def get_all_themes():
    theme_names = list(themes.keys())
    theme_names.sort()
    return theme_names


def get_theme_file(theme_name: str):
    if not themes.__contains__(theme_name):
        settings_manager.write_settings_value(settings_manager.THEME_KEY, "light green")
        return "resources/themes/" + themes["light green"], False
    invert_secondary = False
    if themes[theme_name].startswith("light"):
        invert_secondary = True
    return "resources/themes/" + themes[theme_name], invert_secondary
