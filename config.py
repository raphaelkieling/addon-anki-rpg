from aqt import mw
config = mw.addonManager.getConfig(__name__)

from .player import Player

def save_config_prop(prop, value):
    config[prop] = value
    mw.addonManager.writeConfig(__name__, config)


def get_config_prop(prop):
    if prop in config:
        return config[prop]
    return None


def load_config_state():
    resolved_config = {}
    if "player" in config:
        resolved_config["player"] = config["player"]

    if "last_daily_loot" in config:
        resolved_config["last_daily_loot"] = config["last_daily_loot"]
    else:
        resolved_config["last_daily_loot"] = None

    if "first_loot" in config:
        resolved_config["first_loot"] = config["first_loot"]
    else:
        resolved_config["first_loot"] = False

    return resolved_config
