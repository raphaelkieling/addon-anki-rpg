from aqt import gui_hooks, mw, qconnect
from aqt.qt import *
from aqt.utils import showText
from PyQt5.QtMultimedia import QSound


from aqt.reviewer import Reviewer
from anki.cards import Card

from .config import load_config_state, save_config_prop

from .loot import CardStudyLoot, StartLoot

from .utils import copy_directory, get_file_from_resource
from .ui import PlayerInformationDialog
from .player import Player
import os


class AnkiManager():
    def __init__(self) -> None:
        self.player = Player(
            level=0,
            exp=0
        )

        self.first_loot = False

        self.playerInformationDialog = PlayerInformationDialog(
            mw=mw, player=self.player)

        self.player.subscribe("change", lambda x, y: self.save_state())
        self.player.subscribe("destroy_item", lambda x,
                              y: self.play_destroy_sound())

    def play_destroy_sound(self):
        QSound.play(
            get_file_from_resource(os.path.join("sounds", "delete_item.wav")))

    def calculate_loot(self):
        loots = CardStudyLoot().getLoot()
        showText(str(loots))
        self.player.receive_loot(loots)
        self.playerInformationDialog.update_player()

    def on_did_answer_card(self, reviewer: Reviewer, card: Card, ease: int):
        self.hit_card(ease)
        self.calculate_loot()

    def load_resources(self):
        copy_directory("rpg_resources")

        self.load_state()

        if self.first_loot is False:
            save_config_prop("first_loot", True)
            self.player.receive_loot(StartLoot().getLoot())

    def hit_card(self, ease: int):
        self.player.increase_exp_by_ease(ease)

    def open_stats_window(self):
        self.playerInformationDialog.update_player()
        self.playerInformationDialog.show()

    def save_state(self):
        save_config_prop("player", self.player.toJSON())

    def load_state(self):
        state = load_config_state()
        self.player.fromJSON(state["player"])
        self.first_loot = state["first_loot"]

    # Only UI logic
    def start_menu(self):
        menu = QAction("Player", mw)
        qconnect(menu.triggered, self.open_stats_window)

        mw.rpg = QMenu('&RPG', mw)
        mw.rpg.addAction(menu)
        mw.form.menubar.addMenu(mw.rpg)

    def start_hooks(self):
        gui_hooks.reviewer_did_answer_card.append(self.on_did_answer_card)
        gui_hooks.profile_did_open.append(self.load_resources)

    def start(self):
        self.start_hooks()
        self.start_menu()
