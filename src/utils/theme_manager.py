from src.utils import settings_manager

themes = {
    "dark light green": "dark_lightgreen.xml",
    "light light green": "light_lightgreen.xml",
    "dark amber": "dark_amber.xml",
    "light amber": "light_amber.xml",
    "dark purple": "dark_purple.xml",
    "light purple": "light_purple.xml",
    "dark cyan": "dark_cyan.xml",
    "light cyan": "light_cyan.xml",
}


def get_all_themes():
    theme_names = list(themes.keys())
    theme_names.sort()
    return theme_names


# TODO: fix light themes (darker secondary_dark, maybe different color on titlebar)
def get_theme_file(theme_name: str):
    if not themes.__contains__(theme_name):
        settings_manager.write_settings_value(settings_manager.THEME_KEY, "dark light green")
        return themes["dark light green"], False
    invert_secondary = False
    if themes[theme_name].startswith("light"):
        invert_secondary = True
    return themes[theme_name], invert_secondary
