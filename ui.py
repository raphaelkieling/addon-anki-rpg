from datetime import date, timedelta
from aqt import QDialog, QIcon, QPixmap, QSize
from aqt.utils import showText
from .config import load_config_state, save_config_prop
from .loot import DailyLoot
from .items import TypeConsumableItem
from .player import Player
from .utils import get_anki_media_folder, get_file_from_resource
from .ui_player import Ui_Dialog as Ui_PlayerInformationDialog
from .ui_stats_distribute import Ui_Dialog as Ui_PlayerStatsDistributeDialog
import os
from PyQt5.QtMultimedia import QSound


class PlayerInformationDialog(QDialog, Ui_PlayerInformationDialog):
    def __init__(self, mw, player):
        super().__init__(mw)
        self.setupUi(self)
        self.setFixedSize(804, 591)

        self.player = player

        self.dialogPlayerStatsDistribution = PlayerStatsDistributeDialog(mw, player)

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
        self.daily_loot_button.clicked.connect(self.daily_check)
        self.equip_button.clicked.connect(self.equip_item)
        self.unequip_button.clicked.connect(self.unequip_item)
        self.destroy_button.clicked.connect(self.destroy_item)
        self.distribute_poits_button.clicked.connect(self.dialogPlayerStatsDistribution.show)

        self.player.subscribe("change", lambda x, y: self.update_player())

    def select_item_by_index_connect(self, slot_index):
        return lambda x: self.select_item_by_index(slot_index)

    def select_item_by_body_part_connect(self, body_part):
        return lambda x: self.select_item_by_body_part(body_part)

    def daily_check(self):
        today = date.today()
        self.player.receive_loot(DailyLoot().getLoot())
        self.player.update_daily_streak(today)
        save_config_prop("last_daily_check", today.strftime("%Y-%m-%d"))
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
        item = self.player.inventory.get_item_by_index(index)
        if item is not None:
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
                self.clear_selected_item()
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
        self.bonus_xp_value.setText("{:.2f}".format(stats["bonus_xp"]))
        self.energy_value.setText(
            str(stats["curr_energy"])+"/"+str(stats["max_energy"]))

        # calculate xp to show
        exp_to_next_level = self.player.calculate_exp_by_level(
            self.player.level+1)
        current_exp = self.player.exp
        self.exp_label.setText(
            "{:.2f} / {:.2f} exp".format(current_exp, exp_to_next_level))

        self.exp_progress_bar.setValue(
            self.player.calculate_percentage_exp_to_next_level())

        self.level_value.setText(str(self.player.level))

        # go to each streak an fill the check box
        for i in range(Player.MAX_STREAK):
            item = getattr(self, "streak_check_"+str(i+1))
            if i <= stats["streak"]:
                item.setChecked(True)
            else:
                item.setChecked(False)

    def clear_equipments(self):
        for key in self.player.equipments:
            slot = self.resolve_body_part_to_slot(key)
            self.put_imagem_button(slot, None)
            self.populate_user_info()
        return self

    def resolve_body_part_to_slot(self, body_part):
        if body_part == "head":
            return self.equipment_slot_head
        if body_part == "left_hand":
            return self.equipment_slot_hand_left
        if body_part == "right_hand":
            return self.equipment_slot_hand_right
        if body_part == "body":
            return self.equipment_slot_body
        if body_part == "legs":
            return self.equipment_slot_legs
        if body_part == "acessory":
            return self.equipment_slot_acessory_1
        if body_part == "skill_1":
            return self.skill_slot_1
        if body_part == "skill_2":
            return self.skill_slot_2
        if body_part == "skill_3":
            return self.skill_slot_3
        if body_part == "skill_4":
            return self.skill_slot_4
        if body_part == "skill_5":
            return self.skill_slot_5
        return None

    def populate_equipments(self):
        self.clear_equipments()
        for key in self.player.equipments:
            if self.player.equipments[key]:
                item = self.player.equipments[key]
                slot = self.resolve_body_part_to_slot(key)
                self.put_imagem_button(slot, item.inventory_icon)
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
        for item in self.player.get_items():
            invetory_slot = self.inventory_slots[item.position]
            invetory_slot_label = self.inventory_value_label_slots[item.position]
            invetory_slot_label.setText(str(item.amount))

            if item.amount > 1:
                invetory_slot_label.show()
            else:
                invetory_slot_label.hide()
            self.put_imagem_button(invetory_slot, item.item.inventory_icon)
        return self

    def update_daily_check(self):
        config = load_config_state()
        last_daily_check = config["last_daily_check"]
        if last_daily_check is not None and last_daily_check.date() == date.today():
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

    def update_fight(self):
        self.empty_fight.show()
        self.fight_frame.hide()

    def update_distribute_points(self):
        self.distribute_poits_button.hide()
        if self.player.available_points_to_distribute > 0:
            self.distribute_poits_button.show()
            self.distribute_poits_button.setText("Distribute {} points".format(self.player.available_points_to_distribute))

    def update_player(self):
        self.populate_inventory()
        self.populate_equipments()
        self.populate_user_info()
        self.update_daily_check()
        self.update_selected_item_info()
        self.update_distribute_points()
        self.update_fight()
        return self

class PlayerStatsDistributeDialog(QDialog,Ui_PlayerStatsDistributeDialog):
    def __init__(self, mw, player):
        super().__init__(mw)
        self.setupUi(self)
        self.setFixedSize(238, 220)
        self.player = player
        self.stats = None
        self.current_stats = None
        self.current_used = 0
        self.stats_to_update = [
            "max_hp",
            "strength",
            "defense",
            "max_energy",
        ]
        self.update()

        for stat in self.stats_to_update:
            getattr(self, "{}_add".format(stat)).clicked.connect(self.add_stat_connect(stat))
        
        for stat in self.stats_to_update:
            getattr(self, "{}_sub".format(stat)).clicked.connect(self.sub_stat_connect(stat))

        self.done_button.clicked.connect(self.done_handle)

    def done_handle(self, x):
        self.player.set_stats_by_points(self.current_stats, self.current_used)
        self.close()
        self.current_used = 0

    def cancel(self):
        self.close()
        self.current_used = 0

    def add_stat_connect(self, stat):
        return lambda x: self.add_stat(stat)

    def add_stat(self, stat):
        if self.current_used < self.player.available_points_to_distribute:
            self.current_stats[stat] += 1
            self.current_used += 1
        self.update()

    def sub_stat_connect(self, stat):
        return lambda x: self.sub_stat(stat)

    def sub_stat(self, stat):
        if self.current_used > 0 and self.current_stats[stat] > self.stats[stat]:
            self.current_stats[stat] -= 1
            self.current_used -= 1
        self.update()

    def show(self):
        self.stats = self.player.stats.copy()
        self.current_stats = self.player.stats.copy()

        self.update()
        super().show()
        
    def update(self):
        current_remaining_points = self.player.available_points_to_distribute - self.current_used
        if self.current_stats is not None and self.stats is not None:
            for stat in self.stats_to_update:
                value = self.current_stats[stat]
                getattr(self, "{}_value".format(stat)).setText(str(value))
                getattr(self, "{}_add".format(stat)).setDisabled(current_remaining_points <= 0)
                getattr(self, "{}_sub".format(stat)).setDisabled(value <= self.stats[stat])

        self.available_value.setText(str(current_remaining_points))
        