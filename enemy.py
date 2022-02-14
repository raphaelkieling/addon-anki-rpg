class Enemy():
    def __init__(self, name, health, strength, defense, icon):
        self.name = name
        self.health = health
        self.curr_health = self.health
        self.strength = strength
        self.defense = defense
        self.icon = icon

    def attack(self, target):
        #TODO change the calculation
        damage = self.strength - target.defense
        if damage < 0:
            damage = 0
        target.receive_damage(damage)

    def receive_damage(self, damage):
        self.curr_health -= damage
        if self.curr_health < 0:
            self.curr_health = 0

    def is_alive(self):
        return self.curr_health > 0