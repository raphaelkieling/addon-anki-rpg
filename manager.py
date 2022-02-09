from aqt import gui_hooks, mw, qconnect
from aqt.qt import *
from aqt.utils import showText

from aqt.reviewer import Reviewer
from anki.cards import Card

from .loot import StartLoot

from .utils import copy_directory
from .ui import PlayerInformationDialog
from .player import Player


class AnkiManager():
    def __init__(self) -> None:
        self.player = Player(
            level=0,
            exp=0
        )

        self.playerInformationDialog = PlayerInformationDialog(
            mw=mw, player=self.player)

    def calculate_loot(self):
        pass

    def load_user(self):
        copy_directory("rpg_resources")
        self.player.receive_loot(StartLoot().getLoot())

    def hit_card(self, reviewer: Reviewer, card: Card, ease: int):
        self.player.increase_exp(10)
        self.playerInformationDialog.update_player()

    def start_hooks(self):
        gui_hooks.reviewer_will_end.append(self.calculate_loot)
        gui_hooks.reviewer_did_answer_card.append(self.hit_card)
        gui_hooks.main_window_did_init.append(self.load_user)

    def open_stats_window(self):
        self.playerInformationDialog.update_player()
        self.playerInformationDialog.show()

    def start_menu(self):
        menu = QAction("Player", mw)
        qconnect(menu.triggered, self.open_stats_window)

        mw.rpg = QMenu('&RPG', mw)
        mw.rpg.addAction(menu)
        mw.form.menubar.addMenu(mw.rpg)

    def start(self):
        self.start_hooks()
        self.start_menu()
