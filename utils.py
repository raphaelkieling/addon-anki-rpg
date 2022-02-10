from pathlib import Path
import shutil
from aqt import mw
import os

def get_anki_media_folder():
    return Path(mw.col.media.dir())


def copy_directory(dir_addon: str, dir_anki: str = None):
    addon_dir = Path(__file__).parents[0]
    mediafolder = get_anki_media_folder()

    if not dir_anki:
        dir_anki = dir_addon
    fromdir = addon_dir / dir_addon
    todir = mediafolder / dir_anki
    if not fromdir.is_dir():
        return
    if not todir.is_dir():
        shutil.copytree(str(fromdir), str(todir))


def get_file_from_resource(filename):
    return os.path.join(
        get_anki_media_folder(), "rpg_resources", filename)


def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
                     for key, value in obj.__dict__.items()
                     if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


