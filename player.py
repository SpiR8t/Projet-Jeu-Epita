import pygame

from actions import MeleeAction, interactAction

class Entity():
    def __init__(self,x,y,max_hp,speed):
        self.x_spawn = x
        self.y_spawn = y
        self.x = x
        self.y = y
        self.hp = max_hp
        self.max_hp = max_hp
        self.speed = speed

    def get_pos(self):
        return (self.x, self.y)
    
    def take_damage(self,amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def respawn(self):
        self.x = self.x_spawn
        self.y = self.y_spawn
        self.hp = self.max_hp

    

class Player(Entity):
    def __init__(self, x, y, avatar_image, is_host):
        super().__init__(x, y, 100,2)
        self.avatar = avatar_image
        self.host = is_host
        self.direction = (0,-1)

        self.skills = [SwordAttack(), Interact()]
        self.hitbox = pygame.Rect(x, y, 30, 50)
        # offset pour centrer la hitbox des joueurs (variables modifiables)
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = -50

        
    def try_use(self, index):
        if index < len(self.skills):
            return self.skills[index].try_use(self)
        return None
    
    def update(self):
        for skill in self.skills:
            skill.update()


"""Partie sur les skills et les compétences """


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

    def try_use(self, caster):
        if not self.can_use():
            return None
        else:
            self.current_cd = self.cooldown
            print('can use')
            return self.create_action(caster)

    def create_action(self, caster):
        raise NotImplementedError("create_action must be overridden")

class Interact(Skill):
    def __init__(self):
        super().__init__(cooldown=40, range=1)

    def try_use(self, caster):
        if not self.can_use():
            return None
        else:
            self.current_cd = self.cooldown
            print('can use')
            return self.create_action(caster)

    def create_action(self, caster):
        return interactAction(caster.x, caster.y)

class SwordAttack(Skill):
    def __init__(self):
        super().__init__(cooldown=100, range=1)

    def create_action(self, caster):
        return MeleeAction(caster, self.range)