import random
from aqt.utils import showText
from .items import get_item_by_code, get_all_items_json


class Loot():
    def __init__(self, loots=None):
        self.loots = loots
        if self.loots is None:
            self.loots = []
            for item in get_all_items_json():
                loot_config = item["loot"]
                self.loots.append({
                    "code": item["code"],
                    "weight": loot_config["weight"],
                    "min": loot_config["min"],
                    "max": loot_config["max"]
                })
        self.index_loots = [[i] for i in range(len(self.loots))]

    def getLoot(self):
        total = 0
        for loot in self.loots:
            total += loot["weight"]

        draw = random.randint(0, total)
        dropList = []
        for index in range(len(self.index_loots)):
            loot = self.loots[index]
            if draw <= loot["weight"]:
                amount = 1
                if "min" in loot and "max" in loot:
                    amount = random.randint(loot["min"], loot["max"])
                item = get_item_by_code(loot["code"])
                if item:
                    dropList.append({
                        "item": item,
                        "amount": amount
                    })
            else:
                draw -= loot["weight"]

        return dropList


class StartLoot(Loot):
    def __init__(self):
        super().__init__()


class DailyLoot(Loot):
    def __init__(self):
        super().__init__()


class CardStudyLoot(Loot):
    def __init__(self):
        super().__init__()
