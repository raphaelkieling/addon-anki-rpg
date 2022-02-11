buildui:
	pyuic5 rpg_resources/player.ui -o ui_player.py

init:
	pip install -r requirements.txt

unit:
	pytest player_test.py