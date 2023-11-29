from src.utils import settings_manager
from src.wme_widgets import main_widget

def get_mod_settings():
    try:
        app_state = settings_manager.get_settings_value(settings_manager.APP_STATE)
        mod_state = app_state[main_widget.instance.get_loaded_mod_name()]
        return mod_state
    except Exception:
        return {}


def set_mod_settings(mod_state):
    app_state = settings_manager.get_settings_value(settings_manager.APP_STATE)
    app_state[main_widget.instance.get_loaded_mod_name()] = mod_state
    settings_manager.write_settings_value(settings_manager.APP_STATE, app_state)
