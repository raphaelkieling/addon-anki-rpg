

from .observer import Observable
from .utils import todict
from .items import Item, convert_item_from_json, convert_items_from_json
from aqt.utils import showText
import math


class InventoryItem():
    def __init__(self, item: Item, amount: int):
        self.item = item
        self.amount = amount


class Inventory():
    def __init__(self):
        self.items = []

    def receive_item(self, item: Item, amount: int):
        alreadyExist = False
        for inventory_item in self.items:
            if inventory_item.item.code == item.code:
                inventory_item.amount += 1
                alreadyExist = True

        if not alreadyExist:
            self.items.append(InventoryItem(item, amount))
        return self

    def get_inventory_item_by_id(self, id):
        for item in self.items:
            if item.item.id == id:
                return item.item
        return None

    def get_index_by_item(self, item: Item):
        for index, inventory_item in enumerate(self.items):
            if inventory_item.item.id == item.id:
                return index
        return -1

    def remove_item(self, item: Item):
        for inventory_item in self.items:
            if inventory_item.item.id == item.id:
                inventory_item.amount -= 1
                if inventory_item.amount <= 0:
                    self.items.remove(inventory_item)
                return True
        return False

    def fromJSON(self, data):
        for inventory_item in data["items"]:
            item = convert_item_from_json(inventory_item["item"])
            self.items.append(InventoryItem(item, inventory_item["amount"]))
        return self


class Player(Observable):
    def __init__(self, nickname="", level=1, exp=0, inventory: Inventory = Inventory(), stats=None):
        super().__init__()
        self.nickname = nickname
        self.level = level
        self.exp = exp
        self.inventory = inventory

        if stats is None:
            self.stats = {
                "curr_hp": 10,
                "max_hp": 10,
                "strength": 2,
                "defense": 2,
                "curr_energy": 10,
                "max_energy": 10,
            }
        else:
            self.stats = stats

        self.equipments = {
            "left_hand": None,
            "right_hand": None,
            "head": None,
            "body": None,
            "legs": None,
            "acessory": None,
            "skill_1": None,
            "skill_2": None,
            "skill_3": None,
            "skill_4": None,
            "skill_5": None,
        }

    # return the exp necessary to a level
    # https://bulbapedia.bulbagarden.net/wiki/Experience
    # Function https://www.wolframalpha.com/input?i=4+*+pow%28x%2C+3%29+%2F+5
    def calculate_exp_by_level(self, level: int) -> float:
        return 4 * pow(level, 3) / 5

    # just inverse the function above
    def calculate_level_by_exp(self, exp: float) -> int:
        return math.floor(((5 * exp) / 4)**(1/3))

    def update_level(self):
        levelByExp = self.calculate_level_by_exp(self.exp)
        self.level = levelByExp
        self.emit("change")
        return self

    def increase_exp_by_ease(self, ease: int):
        self.increase_exp(7 * (ease * 1.1))

    def increase_exp(self, value):
        self.exp += value
        self.update_level()
        return self

    def decrease_exp(self, value):
        if self.exp - value <= 0:
            self.exp = 0
        else:
            self.exp -= value

        self.update_level()
        return self

    def equip(self, id):
        item = self.inventory.get_inventory_item_by_id(id)
        if len(item.body_parts) > 0:
            empty = []
            for bodyPart in item.body_parts:
                if not self.equipments[bodyPart]:
                    empty.append(bodyPart)

            firstBodyPartToUse = item.body_parts[0]
            if len(empty) > 0:
                firstBodyPartToUse = empty[0]

            self.unequip(firstBodyPartToUse)
            self.equipments[firstBodyPartToUse] = item
            self.inventory.remove_item(item)
            return {
                "body_part": firstBodyPartToUse,
                "item": item
            }
        return None

    def unequip(self, bodyPart):
        item = self.equipments[bodyPart]
        if item:
            self.inventory.receive_item(item, 1)
            self.equipments[bodyPart] = None
            self.emit("change")
            return item
        return None

    def destroy_item(self, item):
        for key in self.equipments:
            if self.equipments[key] == item:
                self.equipments[key] = None
                break
        self.inventory.remove_item(item)
        self.emit("change")
        self.emit("destroy_item")
        return self

    def receive_loot(self, items):
        for loot in items:
            self.receive_item(loot["item"], loot["amount"])
        self.emit("change")
        return self

    def get_stats(self):
        stats = self.stats.copy()
        for key in self.equipments:
            if self.equipments[key]:
                stats = self.equipments[key].apply_each_modifier(stats)
        return stats

    def resolve_hp_value(self, value):
        finalValue = self.stats["curr_hp"] + value
        if finalValue > self.stats["max_hp"]:
            return self.stats["max_hp"]
        elif finalValue < 0:
            return 0
        else:
            return finalValue

    def consume_item(self, id):
        item = self.inventory.get_inventory_item_by_id(id)
        stats = self.stats.copy()
        newStats = item.apply_each_modifier(stats)
        self.set_stats(newStats)
        self.inventory.remove_item(item)
        self.emit("change")
        return self

    def receive_item(self, item, amount):
        self.inventory.receive_item(item, amount)
        self.emit("change")
        return self

    def get_items(self):
        return self.inventory.items

    def set_stats(self, stats):
        self.stats = {
            "curr_hp": self.resolve_hp_value(stats["curr_hp"]),
            "max_hp": stats["max_hp"],
            "strength": stats["strength"],
            "defense": stats["defense"],
            "curr_energy": stats["curr_energy"],
            "max_energy": stats["max_energy"],
        }
        self.emit("change")
        return self

    def toJSON(self):
        return todict(self)

    def fromJSON(self, data):
        self.nickname = data["nickname"]
        self.level = data["level"]
        self.exp = data["exp"]
        self.inventory = Inventory().fromJSON(data["inventory"])
        self.stats = data["stats"]
        self.equipments = {
            "left_hand": convert_item_from_json(data["equipments"]["left_hand"]),
            "right_hand": convert_item_from_json(data["equipments"]["right_hand"]),
            "head": convert_item_from_json(data["equipments"]["head"]),
            "body": convert_item_from_json(data["equipments"]["body"]),
            "legs": convert_item_from_json(data["equipments"]["legs"]),
            "acessory": convert_item_from_json(data["equipments"]["acessory"]),
            "skill_1": convert_item_from_json(data["equipments"]["skill_1"]),
            "skill_2": convert_item_from_json(data["equipments"]["skill_2"]),
            "skill_3": convert_item_from_json(data["equipments"]["skill_3"]),
            "skill_4": convert_item_from_json(data["equipments"]["skill_4"]),
            "skill_5": convert_item_from_json(data["equipments"]["skill_5"]),
        }
        self.update_level()
        return self
