from .player import Player
from aqt import mw
import datetime
config = mw.addonManager.getConfig(__name__)


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
    else:
        resolved_config["player"] = Player().toJSON()

    if "last_daily_check" in config and config["last_daily_check"] is not None:
        resolved_config["last_daily_check"] = datetime.datetime.strptime(
            config["last_daily_check"], "%Y-%m-%d")
    else:
        resolved_config["last_daily_check"] = None

    if "first_loot" in config:
        resolved_config["first_loot"] = config["first_loot"]
    else:
        resolved_config["first_loot"] = False

    return resolved_config
