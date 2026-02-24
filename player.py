import pygame

class Entity():
    def __init__(self,x,y,max_hp,speed):
        self.x_origine = x
        self.y_origine = y
        self.x = x
        self.y = y
        self.hp = max_hp
        self.max_hp = max_hp
        self.speed = speed

class Player(Entity):
    def __init__(self, x, y, avatar_image, is_host):
        super().__init__(x, y, 20,2)
        self.avatar = avatar_image
        self.host = is_host
        
        self.skills = []

    def get_pos(self):
        return (self.x, self.y)
    
    def reset(self):
        self.x = self.x_origine
        self.y = self.y_origine
        
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
