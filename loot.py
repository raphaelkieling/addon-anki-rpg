import random
from aqt.utils import showText 
from .items import get_item_by_code


class Loot():
    def __init__(self, loots):
        self.loots = loots

    def getLoot(self):
        draw = random.randint(0, 100)
        dropList = []
        for loot in self.loots:
            if draw <= loot["chance"]:
                amount = 1
                if "min" in loot and "max" in loot:
                    amount = random.randint(loot["min"], loot["max"])
                item = get_item_by_code(loot["code"])
                if item:
                    dropList.append({
                        "item": item,
                        "amount": amount
                    })
        return dropList


class StartLoot(Loot):
    def __init__(self):
        super().__init__([
            {
                "code": "wood_sword",
                "chance": 100
            },
            {
                "code": "leather_helm",
                "chance": 100
            },
            {
                "code": "leather_armor",
                "chance": 100
            },
            {
                "code": "leather_legs",
                "chance": 100
            },
            {
                "code": "bronze_ring",
                "chance": 100
            },
            {
                "code": "skill_blood_hit",
                "chance": 100
            },
            {
                "code": "potion",
                "chance": 100,
                "min": 4,
                "max": 5
            }
        ])
