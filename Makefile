buildui:
	pyuic5 rpg_resources/player.ui -o ui_player.py
	pyuic5 rpg_resources/item_information.ui -o ui_item_information.py

init:
	pip install -r requirements.txt

unit:
	pytest player_test.py