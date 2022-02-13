buildui:
	pyuic5 rpg_resources/player.ui -o ui_player.py
	pyuic5 rpg_resources/stats_distribute.ui -o ui_stats_distribute.py

init:
	pip install -r requirements.txt

unit:
	pytest player_test.py