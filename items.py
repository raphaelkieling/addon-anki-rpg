from asyncio.windows_events import NULL
import string
import uuid

import json

from .utils import get_file_from_resource, todict
from aqt.utils import showText


class ItemAttributeModifier():
    def __init__(self, attribute: string = "", value: float = 0, operator: string = ""):
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

    def toJSON(self):
        return todict(self)

    def fromJSON(self, data):
        return ItemAttributeModifier(
            attribute=data["attribute"],
            value=data["value"],
            operator=data["operator"]
        )


class Item():
    def __init__(self, type, code, name, description, inventory_icon, modifiers):
        self.id = str(uuid.uuid4())
        self.code = code
        self.type = type
        self.name = name
        self.description = description
        self.modifiers = modifiers
        self.inventory_icon = inventory_icon

    def apply_each_modifier(self, stats):
        for modifier in self.modifiers:
            stats[modifier.attribute] = modifier.apply_modifier(
                stats[modifier.attribute])
        return stats

    def toJSON(self):
        return todict(self)

    def fromJSON(self, data):
        return Item(
            type=data["type"],
            code=data["code"],
            name=data["name"],
            description=data["description"],
            inventory_icon=data["inventory_icon"],
            modifiers=data["modifiers"]
        )

# Category


class TypeEquippableItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers, body_parts):
        super().__init__("equippable", code, name,
                         description, inventory_icon, modifiers)
        self.body_parts = body_parts


class TypeConsumableItem(Item):
    def __init__(self, code, name, description, inventory_icon, modifiers):
        super().__init__("consumable", code, name, description, inventory_icon, modifiers)
        self.body_parts = None


class TypeSkillItem(Item):
    def __init__(self, code, name, description, inventory_icon):
        super().__init__("skill", code, name, description, inventory_icon, [])
        self.body_parts = ["skill_1", "skill_2",
                          "skill_3", "skill_4", "skill_5"]


# read items.json file and map to a item
def get_all_items():
    items = []
    with open(get_file_from_resource("items.json"), "r") as f:
        item_list = json.load(f)
        items = convert_items_from_json(item_list)
    return items


def convert_item_from_json(item):
    if item is None or item is NULL or "type" not in item:
        return None

    modifiers = []
    if "modifiers" in item:
        for modifier in item["modifiers"]:
            modifiers.append(ItemAttributeModifier().fromJSON(modifier))

    body_parts = []
    if "body_parts" in item:
        body_parts = item["body_parts"]

    if item["type"] == "equippable":
        return TypeEquippableItem(
            item["code"], item["name"], item["description"],
            item["inventory_icon"], modifiers, body_parts)
    elif item["type"] == "skill":
        return TypeSkillItem(
            item["code"], item["name"], item["description"],
            item["inventory_icon"])
    elif item["type"] == "consumable":
        TypeConsumableItem(
            item["code"], item["name"], item["description"], item["inventory_icon"], modifiers)
    return None


def convert_items_from_json(item_json):
    if item_json is None or item_json is NULL:
        return []

    items = []
    for item in item_json:
        mapped_item = convert_item_from_json(item)
        if mapped_item is not None:
            items.append(mapped_item)
    return items


def get_item_by_code(code):
    for item in get_all_items():
        if item.code == code:
            return item
    return None
