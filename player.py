

from typing import List
from .items import Item
from aqt.utils import showText


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

    def remove_item(self, item: Item):
        for inventory_item in self.items:
            if inventory_item.item.id == item.id:
                inventory_item.amount -= 1
                if inventory_item.amount <= 0:
                    self.items.remove(inventory_item)
                return True
        return False


class Player():
    def __init__(self, nickname="", level=1, exp=0, inventory: Inventory = Inventory(), stats=None):
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
                "energy": 10,
            }
        else:
            self.stats = stats

        self.equipments = {
            "hand": None,
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
        return round((5 * exp / 4)**(1./3.))

    def update_level(self):
        levelByExp = self.calculate_level_by_exp(self.exp)
        self.level = levelByExp
        return self

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
        if len(item.bodyParts) > 0:
            empty = []
            for bodyPart in item.bodyParts:
                if not self.equipments[bodyPart]:
                    empty.append(bodyPart)

            firstBodyPartToUse = item.bodyParts[0]
            if len(empty) > 0:
                firstBodyPartToUse = empty[0]
                
            self.unequip(firstBodyPartToUse)
            self.equipments[firstBodyPartToUse] = item
            self.inventory.remove_item(item)
        return self

    def unequip(self, bodyPart):
        item = self.equipments[bodyPart]
        if item:
            self.inventory.receive_item(item, 1)
            self.equipments[bodyPart] = None
        return self

    def receive_loot(self, items):
        for loot in items:
            self.receive_item(loot["item"], loot["amount"])
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
        return self

    def receive_item(self, item, amount):
        self.inventory.receive_item(item, amount)
        return self

    def get_items(self):
        return self.inventory.items

    def set_stats(self, stats):
        self.stats = {
            "curr_hp": self.resolve_hp_value(stats["curr_hp"]),
            "max_hp": stats["max_hp"],
            "strength": stats["strength"],
            "defense": stats["defense"],
            "energy": stats["energy"],
        }
        return self
