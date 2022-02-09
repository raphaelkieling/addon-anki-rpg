import string
import uuid

import json

from .utils import get_file_from_resource
from aqt.utils import showText


class ItemAttributeModifier():
    def __init__(self, attribute: string, value: float, operator: string):
        self.attribute = attribute
        self.value = value
        self.operator = operator

    def apply_modifier(self, stats_value):
        if self.operator == "add":
            return stats_value + self.value
        elif self.operator == "sub":
            return stats_value - self.value
        elif self.operator == "mult":
            return stats_value * self.value
        elif self.operator == "div":
            return stats_value / self.value
        else:
            return stats_value


class Item():
    def __init__(self, code, name, description, inventory_icon, modifiers):
        self.id = uuid.uuid4()
        self.code = code
        self.name = name
        self.description = description
        self.modifiers = modifiers
        self.inventory_icon = inventory_icon

    def apply_each_modifier(self, stats):
        for modifier in self.modifiers:
            stats[modifier.attribute] = modifier.apply_modifier(
                stats[modifier.attribute])
        return stats


# Category
class TypeWeaponItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers):
        super().__init__(code, name, description, inventory_icon, modifiers)
        self.bodyParts = ["hand"]


class TypeHelmItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers):
        super().__init__(code, name, description, inventory_icon, modifiers)
        self.bodyParts = ["head"]


class TypeBodyItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers):
        super().__init__(code, name, description, inventory_icon, modifiers)
        self.bodyParts = ["body"]


class TypeLegsItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers):
        super().__init__(code, name, description, inventory_icon, modifiers)
        self.bodyParts = ["legs"]


class TypeAcessoryItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers):
        super().__init__(code, name, description, inventory_icon, modifiers)
        self.bodyParts = ["acessory"]


class TypeConsumableItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers):
        super().__init__(code, name, description, inventory_icon, modifiers)
        self.bodyParts = None


class TypeSkillItem(Item):
    def __init__(self, code, name, description, inventory_icon):
        super().__init__(code, name, description, inventory_icon, [])
        self.bodyParts = ["skill_1", "skill_2", "skill_3", "skill_4", "skill_5"]


# read items.json file and map to a item
def get_all_items():
    items = []
    with open(get_file_from_resource("items.json"), "r") as f:
        item_list = json.load(f)
        for item in item_list:
            modifiers = []
            for modifier in item["modifiers"]:
                modifiers.append(ItemAttributeModifier(
                    modifier["attribute"], modifier["value"], modifier["operator"]))

            if item["type"] == "weapon":
                items.append(TypeWeaponItem(
                    item["code"], item["name"], item["description"],
                    item["inventory_icon"], modifiers))
            elif item["type"] == "helm":
                items.append(TypeHelmItem(
                    item["code"], item["name"], item["description"],
                    item["inventory_icon"], modifiers))
            elif item["type"] == "body":
                items.append(TypeBodyItem(
                    item["code"], item["name"], item["description"],
                    item["inventory_icon"], modifiers))
            elif item["type"] == "legs":
                items.append(TypeLegsItem(
                    item["code"], item["name"], item["description"],
                    item["inventory_icon"], modifiers))
            elif item["type"] == "skill":
                items.append(TypeSkillItem(
                    item["code"], item["name"], item["description"],
                    item["inventory_icon"]))
            elif item["type"] == "acessory":
                items.append(TypeAcessoryItem(
                    item["code"], item["name"], item["description"],
                    item["inventory_icon"], modifiers))
                items.append(TypeConsumableItem(
                    item["code"], item["name"], item["description"], item["inventory_icon"], modifiers))
    return items


def get_item_by_code(code):
    for item in get_all_items():
        if item.code == code:
            return item
    return None
