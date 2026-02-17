import pygame


class Joueur:
    def __init__(self, x, y, vitesse, avatar_image, is_host):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.avatar = avatar_image
        self.host = is_host
        
        self.skills = []

    def get_pos(self):
        return (self.x, self.y)
    
    def attack(self):
        pass


class Skill:
    def __init__(self, cooldown, range):
        self.cooldown = cooldown
        self.current_cd = 0
        self.range = range

    def update(self):
        if self.current_cd > 0:
            self.current_cd -= 1

    def can_use(self):
        return self.current_cd <= 0

    def use(self, caster):
        pass


class Projectile:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed

    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

class SwordAttack(Skill):
    def __init__(self):
        super().__init__(cooldown=30, range=1)

    def use(self, caster):
        if not self.can_use():
            return

        self.current_cd = self.cooldown

class Flash(Skill):
    def __init__(self):
        super().__init__(cooldown=60, range=6)

    def use(self, caster):
        if not self.can_use():
            return

        projectile = Projectile(caster.x, caster.y, (1,0), 5)
        self.current_cd = self.cooldown