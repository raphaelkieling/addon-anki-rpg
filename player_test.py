# from .items import FlawedPotionItem, SimpleLeatherHelm, SimpleSwordItem, ItemAttributeModifier
# from .player import Player


# def test_should_increase_exp():
#     player = Player()
#     player.increase_exp(3).increase_exp(3)
#     assert player.exp == 6


# def test_should_decrease_exp():
#     player = Player()
#     player.decrease_exp(3).decrease_exp(3)
#     assert player.exp == 0


# def test_should_calculate_level():
#     player = Player()
#     result = player.calculate_exp_by_level(0)
#     assert result == 0

#     result = player.calculate_exp_by_level(1)
#     assert result == 0.8

#     result = player.calculate_exp_by_level(2)
#     assert result == 6.4

#     result = player.calculate_exp_by_level(3)
#     assert result == 21.6


# def test_should_calculate_level_by_exp():
#     player = Player()
#     result = player.calculate_level_by_exp(6.4)
#     assert result == 2

#     result = player.calculate_level_by_exp(21.6)
#     assert result == 3


# def test_should_level_up_to_correct_level():
#     player = Player()
#     assert player.increase_exp(21.6).level == 3


# def test_should_receive_inventory_item():
#     player = Player()
#     player.receive_item(SimpleSwordItem())
#     assert len(player.get_items()) == 1


# def test_should_equip_and_unequip_item_and_apply_modifiers():
#     player = Player(
#         inventory=Inventory([]),
#         stats={
#             "curr_hp": 0,
#             "max_hp": 10,
#             "strength": 0,
#             "defense": 0,
#         })

#     swordItem = SimpleSwordItem()
#     leatherItem = SimpleLeatherHelm()
#     player.receive_item(swordItem)
#     player.receive_item(leatherItem)

#     assert len(player.get_items()) == 2

#     player.equip(swordItem.id)
#     player.equip(leatherItem.id)

#     assert len(player.get_items()) == 0
#     assert player.equipments[swordItem.bodyPart] == swordItem
#     assert player.get_stats() == {
#         "curr_hp": 0,
#         "max_hp": 10,
#         "strength": 1,
#         "defense": 1,
#     }

#     player.unequip(swordItem.bodyPart)
#     assert player.equipments[swordItem.bodyPart] == None
#     assert player.get_stats() == {
#         "curr_hp": 0,
#         "max_hp": 10,
#         "strength": 0,
#         "defense": 1,
#     }


# def test_should_use_consumable_item():
#     player = Player(
#         inventory=Inventory([]),
#         stats={
#             "curr_hp": 5,
#             "max_hp": 10,
#             "strength": 0,
#             "defense": 0,
#         })

#     potion = FlawedPotionItem()
#     player.receive_item(potion).consume_item(potion.id)

#     assert len(player.get_items()) == 0
#     assert player.get_stats() == {
#         "curr_hp": 10,
#         "max_hp": 10,
#         "strength": 0,
#         "defense": 0,
#     }
