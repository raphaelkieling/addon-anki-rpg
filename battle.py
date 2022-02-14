from .enemy import Enemy

class BattleManager():
    def __init__(self, player):
        self.enemy = None
        self.player = player
        self.queue_turn = []
        self.current_turn = 0
        self.count_turns = 0
        self.is_running = False

    def get_enemy(self):
        return self.enemy

    def find_single_fight(self):
        self.enemy = Enemy("Skeleton", 10, 5, 3, "skeleton.png")
        self.is_running = True

    def reset(self):
        self.enemy = None
        self.queue_turn = []
        self.current_turn = 0
        self.count_turns = 0
        self.is_running = False
