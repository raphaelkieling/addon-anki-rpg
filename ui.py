from datetime import date
from aqt import QDialog, QIcon, QPixmap, QSize
from aqt.utils import showText
from .config import load_config_state, save_config_prop
from .loot import DailyLoot
from .items import TypeConsumableItem
from .player import Player
from .utils import get_anki_media_folder, get_file_from_resource
from .ui_player import Ui_Dialog as Ui_PlayerInformationDialog
import os
from PyQt5.QtMultimedia import QSound


class PlayerInformationDialog(QDialog, Ui_PlayerInformationDialog):
    def __init__(self, mw, player):
        super().__init__(mw)
        self.setupUi(self)
        self.setFixedSize(609, 591)

        self.player = player

        self.selected_item = None
        self.selected_item_to_equip = False

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
            val.clicked.connect(self.select_item_by_index_connect(i))

        for i, val in enumerate(self.skill_slots):
            val.clicked.connect(
                self.select_item_by_body_part_connect("skill_"+str(i+1)))

        self.equipment_slot_hand_left.clicked.connect(
            self.select_item_by_body_part_connect("left_hand"))
        self.equipment_slot_hand_right.clicked.connect(
            self.select_item_by_body_part_connect("right_hand"))
        self.equipment_slot_body.clicked.connect(
            self.select_item_by_body_part_connect("body"))
        self.equipment_slot_legs.clicked.connect(
            self.select_item_by_body_part_connect("legs"))
        self.equipment_slot_head.clicked.connect(
            self.select_item_by_body_part_connect("head"))
        self.equipment_slot_acessory_1.clicked.connect(
            self.select_item_by_body_part_connect("acessory"))
        self.daily_loot_button.clicked.connect(self.daily_loot)
        self.equip_button.clicked.connect(self.equip_item)
        self.unequip_button.clicked.connect(self.unequip_item)
        self.destroy_button.clicked.connect(self.destroy_item)

    def select_item_by_index_connect(self, slot_index):
        return lambda x: self.select_item_by_index(slot_index)

    def select_item_by_body_part_connect(self, body_part):
        return lambda x: self.select_item_by_body_part(body_part)

    def daily_loot(self):
        self.player.receive_loot(DailyLoot().getLoot())
        save_config_prop("last_daily_loot", date.today().strftime("%Y-%m-%d"))
        self.update_player()

    def destroy_item(self):
        if self.selected_item:
            self.player.destroy_item(self.selected_item)
            self.clear_selected_item()
        self.update_player()

    def clear_selected_item(self):
        self.selected_item = None
        self.selected_item_body_part = None

    def unequip_item(self):
        body_part = self.selected_item_body_part
        item = self.selected_item
        if body_part and item:
            self.player.unequip(body_part)
            index = self.player.inventory.get_index_by_item(item)
            self.select_item_by_index(index)
            self.update_player()
        return self

    def select_item_by_index(self, index):
        if index < len(self.player.inventory.items):
            item = self.player.inventory.items[index]
            self.selected_item = item.item
            self.selected_item_body_part = None
        else:
            self.selected_item = None
            self.selected_item_body_part = None
        self.update_player()

    def select_item_by_body_part(self, body_part):
        if not self.player.equipments[body_part] is None:
            self.selected_item = self.player.equipments[body_part]
            self.selected_item_body_part = body_part
        else:
            self.selected_item = None
            self.selected_item_body_part = None
        self.update_player()

    def equip_item(self):
        item = self.selected_item
        if item:
            if isinstance(item, TypeConsumableItem):
                self.player.consume_item(item.id)
            else:
                result = self.player.equip(item.id)
                self.select_item_by_body_part(result["body_part"])

            self.update_player()

    def populate_user_info(self):
        stats = self.player.get_stats()
        self.nickname_value.setText(self.player.nickname)
        self.health_value.setText(
            str(stats["curr_hp"])+"/"+str(stats["max_hp"]))
        self.strength_value.setText(str(stats["strength"]))
        self.defense_value.setText(str(stats["defense"]))
        self.energy_value.setText(
            str(stats["curr_energy"])+"/"+str(stats["max_energy"]))

        # calculate xp to show
        exp_to_next_level = self.player.calculate_exp_by_level(
            self.player.level+1)
        exp_to_curr_level = self.player.calculate_exp_by_level(
            self.player.level)
        current_exp = self.player.exp
        self.exp_label.setText(
            "{} / {} exp".format(str(current_exp), str(exp_to_next_level)))

        percentageExp = (current_exp-exp_to_curr_level) * \
            100 / (exp_to_next_level-exp_to_curr_level)
        self.exp_progress_bar.setValue(percentageExp)

        self.level_value.setText(str(self.player.level))

    def clear_equipments(self):
        for key in self.player.equipments:
            if key == "head":
                self.put_imagem_button(
                    self.equipment_slot_head, None)
            if key == "left_hand":
                self.put_imagem_button(
                    self.equipment_slot_hand_left, None)
            if key == "right_hand":
                self.put_imagem_button(
                    self.equipment_slot_hand_right, None)
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
                if key == "left_hand":
                    self.put_imagem_button(
                        self.equipment_slot_hand_left, item.inventory_icon)
                if key == "right_hand":
                    self.put_imagem_button(
                        self.equipment_slot_hand_right, item.inventory_icon)
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

                self.populate_user_info()

    def put_imagem_button(self, invetory_slot, inventory_icon_path):
        if inventory_icon_path == None:
            invetory_slot.setIcon(QIcon())
        else:
            pixmap = QPixmap(os.path.join(
                get_anki_media_folder(), "rpg_resources", "items", inventory_icon_path))
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

    def update_daily_loot(self):
        config = load_config_state()
        if "last_daily_loot" in config:
            last_daily_loot = config["last_daily_loot"]
            if last_daily_loot == date.today().strftime("%Y-%m-%d"):
                self.daily_loot_button.setDisabled(True)
            else:
                self.daily_loot_button.setDisabled(False)

    def show_info_item(self):
        if self.selected_item:
            modifierText = ""
            for modifier in self.selected_item.modifiers:
                iconOperator = "+"
                if modifier.operator == "mult":
                    iconOperator = "x"
                elif modifier.operator == "div":
                    iconOperator = "÷"
                elif modifier.operator == "sub":
                    iconOperator = "-"

                modifierText += "{} <span style=\"color:green;\">{}</span> <b>{}</b><br>".format(
                    modifier.attribute, iconOperator, str(modifier.value))
            self.populate_item_selected_info(self.selected_item.inventory_icon)
            self.name_value.setText(self.selected_item.name)
            self.description_value.setText(self.selected_item.description)
            self.modifiers_value.setText(modifierText)
            # Buttons
            if self.selected_item_body_part is None:
                self.equip_button.show()
                self.unequip_button.hide()
            else:
                self.equip_button.hide()
                self.unequip_button.show()
            self.empty_selected_item_label.hide()
            self.inventory_item_selected_frame.show()
        else:
            self.empty_selected_item_label.show()
            self.inventory_item_selected_frame.hide()
            self.populate_item_selected_info(None)
            self.name_value.setText("")
            self.description_value.setText("")
            self.modifiers_value.setText("")

    def populate_item_selected_info(self, inventory_icon_path):
        if inventory_icon_path == None:
            self.item_icon.setIcon(QIcon())
        else:
            pixmap = QPixmap(os.path.join(
                get_anki_media_folder(), "rpg_resources", "items", inventory_icon_path))
            icon = QIcon()
            icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
            self.item_icon.setIcon(icon)
            self.item_icon.setIconSize(QSize(41, 41))

    def update_selected_item_info(self):
        self.show_info_item()

    def update_player(self):
        self.populate_inventory()
        self.populate_equipments()
        self.populate_user_info()
        self.update_daily_loot()
        self.update_selected_item_info()
        return self
