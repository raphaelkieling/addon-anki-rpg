import random
from aqt.utils import showText
from .items import get_item_by_code


class Loot():
    def __init__(self, loots):
        self.loots = loots
        self.index_loots = [[i] for i in range(len(loots))]

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
        super().__init__([
            {
                "code": "wood_sword",
                "weight": 100
            },
            {
                "code": "leather_helm",
                "weight": 100
            },
            {
                "code": "leather_armor",
                "weight": 100
            },
            {
                "code": "leather_legs",
                "weight": 100
            },
            {
                "code": "bronze_ring",
                "weight": 100
            },
            {
                "code": "skill_blood_hit",
                "weight": 100
            },
            {
                "code": "potion",
                "weight": 100,
                "min": 4,
                "max": 5
            }
        ])


class DailyLoot(Loot):
    def __init__(self):
        super().__init__([
            {
                "code": "wood_sword",
                "weight": 30
            },
            {
                "code": "leather_helm",
                "weight": 30
            },
            {
                "code": "leather_armor",
                "weight": 30
            },
            {
                "code": "leather_legs",
                "weight": 30
            },
            {
                "code": "bronze_ring",
                "weight": 24
            },
            {
                "code": "skill_blood_hit",
                "weight": 13
            },
            {
                "code": "potion",
                "weight": 50,
                "min": 4,
                "max": 5
            },
            {
                "code": "chocolate_bar",
                "weight": 50,
                "min": 1,
                "max": 5
            },
            {
                "code": "coffee_cup",
                "weight": 80,
                "min": 1,
                "max": 2
            }
        ])


class CardStudyLoot(Loot):
    def __init__(self):
        super().__init__([
            {
                "code": "wood_sword",
                "weight": 30
            },
            {
                "code": "leather_helm",
                "weight": 30
            },
            {
                "code": "leather_armor",
                "weight": 30
            },
            {
                "code": "leather_legs",
                "weight": 30
            },
            {
                "code": "bronze_ring",
                "weight": 55
            },
            {
                "code": "skill_blood_hit",
                "weight": 70
            },
            {
                "code": "potion",
                "weight": 10,
                "min": 1,
                "max": 5
            },
            {
                "code": "chocolate_bar",
                "weight": 50,
                "min": 1,
                "max": 5
            },
            {
                "code": "coffee_cup",
                "weight": 80,
                "min": 1,
                "max": 2
            }
        ])
