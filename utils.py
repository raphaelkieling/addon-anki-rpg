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
