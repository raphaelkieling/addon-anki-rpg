from pathlib import Path
from aqt import QDialog, QIcon, QPixmap, QSize
from aqt.utils import showText

from .loot import DailyLoot

from .items import TypeConsumableItem

from .player import Player

from .utils import get_anki_media_folder
from .ui_player import Ui_Dialog
import os


class PlayerInformationDialog(QDialog, Ui_Dialog):
    def __init__(self, mw, player):
        super().__init__(mw)
        self.setupUi(self)
        self.setFixedSize(358, 591)

        self.player = player

        self.inventory_slots = [
            self.inventory_slot_1,
            self.inventory_slot_2,
            self.inventory_slot_3,
            self.inventory_slot_4,
            self.inventory_slot_5,
            self.inventory_slot_6,
            self.inventory_slot_7,
            self.inventory_slot_8,
            self.inventory_slot_9,
            self.inventory_slot_10,
            self.inventory_slot_11,
            self.inventory_slot_12,
            self.inventory_slot_13,
            self.inventory_slot_14,
            self.inventory_slot_15,
        ]
        self.inventory_value_label_slots = [
            self.inventory_value_label_1,
            self.inventory_value_label_2,
            self.inventory_value_label_3,
            self.inventory_value_label_4,
            self.inventory_value_label_5,
            self.inventory_value_label_6,
            self.inventory_value_label_7,
            self.inventory_value_label_8,
            self.inventory_value_label_9,
            self.inventory_value_label_10,
            self.inventory_value_label_11,
            self.inventory_value_label_12,
            self.inventory_value_label_13,
            self.inventory_value_label_14,
            self.inventory_value_label_15,
        ]

        self.skill_slots = [
            self.skill_slot_1,
            self.skill_slot_2,
            self.skill_slot_3,
            self.skill_slot_4,
            self.skill_slot_5,
        ]

        for i, val in enumerate(self.inventory_slots):
            val.clicked.connect(self.equip_connect(i))

        for i, val in enumerate(self.skill_slots):
            val.clicked.connect(self.unequip_connect("skill_"+str(i+1)))

        self.equipment_slot_hand.clicked.connect(self.unequip_connect("hand"))
        self.equipment_slot_body.clicked.connect(self.unequip_connect("body"))
        self.equipment_slot_legs.clicked.connect(self.unequip_connect("legs"))
        self.equipment_slot_head.clicked.connect(self.unequip_connect("head"))
        self.equipment_slot_acessory_1.clicked.connect(
            self.unequip_connect("acessory"))
        self.daily_loot_button.clicked.connect(self.daily_loot)

    def equip_connect(self, slot_index):
        return lambda x: self.equip_item(slot_index)

    def unequip_connect(self, bodyPart):
        return lambda x: self.unequip_item(bodyPart)

    def daily_loot(self):
        self.player.receive_loot(DailyLoot().getLoot())
        self.update_player()

    def unequip_item(self, bodyPart):
        self.player.unequip(bodyPart)
        self.update_player()
        return self

    def equip_item(self, index):
        if index < len(self.player.inventory.items):
            item = self.player.inventory.items[index]
            if item:
                if isinstance(item.item, TypeConsumableItem):
                    self.player.consume_item(item.item.id)
                else:
                    self.player.equip(item.item.id)

                self.update_player()

    def populate_info(self):
        stats = self.player.get_stats()
        self.nickname_value.setText(self.player.nickname)
        self.health_value.setText(
            str(stats["curr_hp"])+"/"+str(stats["max_hp"]))
        self.strength_value.setText(str(stats["strength"]))
        self.defense_value.setText(str(stats["defense"]))
        self.energy_value.setText(str(stats["energy"]))

        exp_to_next_level = self.player.calculate_exp_by_level(
            self.player.level+1)
        current_inital_exp = self.player.calculate_exp_by_level(
            self.player.level)
        self.exp_label.setText(str(current_inital_exp) +
                               "/"+str(exp_to_next_level)+" exp")
        percentageExp = current_inital_exp * 100 / exp_to_next_level * 1
        self.exp_progress_bar.setValue(percentageExp)

        self.level_value.setText(str(self.player.level))

    def clear_equipments(self):
        for key in self.player.equipments:
            if key == "head":
                self.put_imagem_button(
                    self.equipment_slot_head, None)
            if key == "hand":
                self.put_imagem_button(
                    self.equipment_slot_hand, None)
            if key == "body":
                self.put_imagem_button(
                    self.equipment_slot_body, None)
            if key == "legs":
                self.put_imagem_button(
                    self.equipment_slot_legs, None)
            if key == "acessory":
                self.put_imagem_button(
                    self.equipment_slot_acessory_1, None)
            if key == "skill_1":
                self.put_imagem_button(self.skill_slot_1, None)
            if key == "skill_2":
                self.put_imagem_button(
                    self.skill_slot_2, None)
            if key == "skill_3":
                self.put_imagem_button(
                    self.skill_slot_3, None)
            if key == "skill_4":
                self.put_imagem_button(
                    self.skill_slot_4, None)
            if key == "skill_5":
                self.put_imagem_button(
                    self.skill_slot_5, None)
        return self

    def populate_equipments(self):
        self.clear_equipments()
        for key in self.player.equipments:
            if self.player.equipments[key]:
                item = self.player.equipments[key]
                if key == "head":
                    self.put_imagem_button(
                        self.equipment_slot_head, item.inventory_icon)
                if key == "hand":
                    self.put_imagem_button(
                        self.equipment_slot_hand, item.inventory_icon)
                if key == "body":
                    self.put_imagem_button(
                        self.equipment_slot_body, item.inventory_icon)
                if key == "legs":
                    self.put_imagem_button(
                        self.equipment_slot_legs, item.inventory_icon)
                if key == "acessory":
                    self.put_imagem_button(
                        self.equipment_slot_acessory_1, item.inventory_icon)
                if key == "skill_1":
                    self.put_imagem_button(
                        self.skill_slot_1, item.inventory_icon)
                if key == "skill_2":
                    self.put_imagem_button(
                        self.skill_slot_2, item.inventory_icon)
                if key == "skill_3":
                    self.put_imagem_button(
                        self.skill_slot_3, item.inventory_icon)
                if key == "skill_4":
                    self.put_imagem_button(
                        self.skill_slot_4, item.inventory_icon)
                if key == "skill_5":
                    self.put_imagem_button(
                        self.skill_slot_5, item.inventory_icon)

                self.populate_info()

    def put_imagem_button(self, invetory_slot, inventory_icon_path):
        if inventory_icon_path == None:
            invetory_slot.setIcon(QIcon())
        else:
            pixmap = QPixmap(os.path.join(
                get_anki_media_folder(), "rpg_resources", inventory_icon_path))
            icon = QIcon()
            icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
            invetory_slot.setIcon(icon)
            invetory_slot.setIconSize(QSize(41, 41))

    def clear_inventory_slots(self):
        for val in self.inventory_value_label_slots:
            val.hide()
        for val in self.inventory_slots:
            val.setIcon(QIcon())

    def populate_inventory(self):
        self.clear_inventory_slots()
        for i, item in enumerate(self.player.inventory.items):
            invetory_slot = self.inventory_slots[i]
            invetory_slot_label = self.inventory_value_label_slots[i]

            invetory_slot_label.setText(str(item.amount))
            invetory_slot_label.show()
            self.put_imagem_button(invetory_slot, item.item.inventory_icon)
        return self

    def update_player(self):
        self.populate_inventory()
        self.populate_equipments()
        self.populate_info()
        return self
