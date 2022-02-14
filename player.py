from .observer import Observable
from .utils import todict
from .items import Item, convert_item_from_json, convert_items_from_json
from aqt.utils import showText
import math
import datetime


class InventoryItem():
    def __init__(self, item: Item, amount: int, position: int):
        self.item = item
        self.amount = amount
        self.position = position


class Inventory():
    MAX_INVENTORY_SIZE = 20

    def __init__(self):
        self.items = list([])

    def is_full(self):
        return len(self.items) >= Inventory.MAX_INVENTORY_SIZE

    def receive_item(self, item: Item, amount: int, force_index = None):
        if self.is_full():
            return self
        
        empty_slot = self.get_empty_slot()

        if force_index is not None:
            empty_slot = force_index

        if item.groupable is False:
            self.items.append(InventoryItem(item, 1, empty_slot))
            return self

        alreadyExist = False
        for inventory_item in self.items:
            if inventory_item is not None and inventory_item.item.code == item.code:
                inventory_item.amount += 1
                alreadyExist = True

        if not alreadyExist:
            self.items.append(InventoryItem(item, amount, empty_slot))
        return self

    def get_empty_slot(self) -> int:
        for i in range(Inventory.MAX_INVENTORY_SIZE):
            item = self.get_item_by_index(i)
            if item is None:
                return i

        return None

    def get_inventory_item_by_id(self, id):
        for item in self.items:
            if item is not None and item.item.id == id:
                return item.item
        return None

    def get_item_by_index(self, index: int):
        items = list(filter(lambda i: i.position == index, self.items))
        if len(items) > 0:
            return items[0]
        return  None

    def get_index_by_item(self, item: Item):
        for index, inventory_item in enumerate(self.items):
            if inventory_item.item.id == item.id:
                return index
        return -1

    def remove_item(self, item: Item):
        for index, inventory_item in enumerate(self.items):
            if inventory_item is not None and inventory_item.item.id == item.id:
                inventory_item.amount -= 1
                if inventory_item.amount <= 0:
                    del self.items[index]
                return True
        return False

    def fromJSON(self, data):
        for inventory_item in data["items"]:
            if inventory_item is not None:
                item = convert_item_from_json(inventory_item["item"])
                self.items.append(InventoryItem(item, inventory_item["amount"], inventory_item["position"]))
        return self

class Player(Observable):
    MAX_STREAK = 36
    STREAK_DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, nickname="", level=1, exp=0, inventory: Inventory = Inventory(), stats=None):
        super().__init__()
        self.nickname = nickname
        self.level = level
        self.exp = exp
        self.inventory = inventory
        self.streak_history = []
        self.available_points_to_distribute = 0

        if stats is None:
            self.stats = {
                "curr_hp": 10,
                "max_hp": 10,
                "strength": 2,
                "defense": 2,
                "curr_energy": 10,
                "max_energy": 10,
                "bonus_xp": 0,
                "streak": 0
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

    def calculate_percentage_exp_to_next_level(self) -> float:
        exp_to_next_level = self.calculate_exp_by_level(self.level+1)
        exp_to_curr_level = self.calculate_exp_by_level(self.level)
        current_exp = self.exp
        return (current_exp-exp_to_curr_level) * 100 / (exp_to_next_level-exp_to_curr_level)

    def get_daily_streak_status(self, date: datetime.date) -> str:
        if len(self.streak_history) == 0:
            return "ok"

        last = datetime.datetime.strptime(
            self.streak_history[-1], Player.STREAK_DATE_FORMAT).date()
        today = date
        yesterday = today - datetime.timedelta(days=1)

        if today == last:
            return "ignore"
        elif yesterday == last:
            return "ok"
        else:
            return "break"

    def update_daily_streak(self, today_reference: datetime.date):
        status = self.get_daily_streak_status(today_reference)

        if status == "ok":
            self.daily_streak()
        elif status == "break":
            self.reset_daily_streak()
        elif status == "ignore":
            pass

        self.streak_history.append(
            today_reference.strftime(Player.STREAK_DATE_FORMAT))

        self.emit("change")

    def daily_streak(self):
        self.stats["streak"] += 1
        if self.stats["streak"] > Player.MAX_STREAK:
            self.stats["streak"] = Player.MAX_STREAK
        self.stats["bonus_xp"] = self.stats["streak"] * 0.2
        self.emit("change")
        return self

    def reset_daily_streak(self):
        self.stats["streak"] = 0
        self.stats["bonus_xp"] = 0
        self.streak_history = []
        self.emit("change")
        return self

    # just inverse the function above
    def calculate_level_by_exp(self, exp: float) -> int:
        return math.floor(((5 * exp) / 4)**(1/3))

    def update_level(self):
        levelByExp = self.calculate_level_by_exp(self.exp)
        # if levelByExp is not the same as the current level, update
        # the available_points_to_distribute with the difference
        if levelByExp != self.level and levelByExp > self.level:
            self.available_points_to_distribute += levelByExp - self.level
        self.level = levelByExp
        self.emit("change")
        return self

    def increase_exp_by_ease(self, ease: int):
        self.increase_exp((7 * (ease * 1.1)) * (1 + self.stats["bonus_xp"]))

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
            self.emit("change")
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
            self.inventory.receive_item(loot["item"], loot["amount"])
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
        return list(filter(lambda i: i is not None, self.inventory.items))

    def set_stats(self, stats):
        self.stats = {
            "curr_hp": self.resolve_hp_value(stats["curr_hp"]),
            "max_hp": stats["max_hp"],
            "strength": stats["strength"],
            "defense": stats["defense"],
            "curr_energy": stats["curr_energy"],
            "max_energy": stats["max_energy"],
            "bonus_xp": stats["bonus_xp"],
            "streak": stats["streak"],
        }
        self.emit("change")
        return self

    def set_stats_by_points(self,stats, used_points):
        self.available_points_to_distribute -= used_points
        self.set_stats(stats)
        self.emit("change")

    def receive_damage(self, damage):
        self.stats["curr_hp"] = self.resolve_hp_value(-damage)
        self.emit("change")
        return self

    def toJSON(self):
        return todict(self)

    def fromJSON(self, data):
        self.nickname = data["nickname"]
        self.level = data["level"]
        self.exp = data["exp"]
        self.available_points_to_distribute = data["available_points_to_distribute"]
        self.inventory = Inventory().fromJSON(data["inventory"])
        self.stats = data["stats"]
        self.streak_history = data["streak_history"]
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
