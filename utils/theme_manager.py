from utils import settings_manager

themes = dict(dark="dark_lightgreen.xml", light="light_lightgreen.xml")


def get_all_themes():
    return list(themes.keys())


def get_theme_file(theme_name: str):
    if not themes.__contains__(theme_name):
        settings_manager.write_settings_value(settings_manager.THEME_KEY, "dark")
        return themes["dark"]
    return themes[theme_name]
