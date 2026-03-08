import pygame

from animations import SpriteSheet
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
        self.skills = [SwordAttack(), Interact()]
        self.hitbox = pygame.Rect(self.x, self.y, 40, 40)

        # Gestion de la spritesheet
        FRAME_W, FRAME_H = 57, 57
        SCALE = 1.5 #64/57
        if is_host:
            walk_sheet = SpriteSheet("assets\images\game\players\sprite_sheet_Aeden_walk_temp.png")
            idle_sheet = SpriteSheet("assets\images\game\players\sprite_sheet_Aeden_still_temp.png")
        else:
            walk_sheet = SpriteSheet("assets\images\game\players\sprite_sheet_Lyra_walk.png")
            idle_sheet = SpriteSheet("assets\images\game\players\sprite_sheet_Lyra_still.png")

        # Walk animation
        self.walk_animations = {
            "walk_NE": walk_sheet.get_animation(row=0, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
            "walk_N":  walk_sheet.get_animation(row=1, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
            "walk_NW": walk_sheet.get_animation(row=2, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
            "walk_E":  walk_sheet.get_animation(row=3, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
            "walk_SE": walk_sheet.get_animation(row=4, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
            "walk_S":  walk_sheet.get_animation(row=5, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
            "walk_SW": walk_sheet.get_animation(row=6, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
            "walk_W":  walk_sheet.get_animation(row=7, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE),
        }

        # Idle sheet
        idle_frames = idle_sheet.get_animation(row=0, num_frames=8, frame_width=FRAME_W, frame_height=FRAME_H,scale=SCALE)
        self.idle_frames = {
            "walk_NE": idle_frames[2],
            "walk_N":  idle_frames[1],
            "walk_NW": idle_frames[3],
            "walk_E":  idle_frames[0],
            "walk_SE": idle_frames[4],
            "walk_S":  idle_frames[7],
            "walk_SW": idle_frames[5],
            "walk_W":  idle_frames[6],
        }

        self.direction = (0,1) # Orienté vers le sud à la base
        self.current_anim = "walk_S"
        self.last_direction = "walk_S"  # dernière direction mémorisée
        self.frame_index = 0
        self.animation_speed = 0.15
        self.is_moving = False
        self.image = self.idle_frames[self.last_direction]

    def update_animation(self):
        ANIM_MAP = {
            ( 1,  0): "walk_E",  (-1,  0): "walk_W",
            ( 0,  1): "walk_S",  ( 0, -1): "walk_N",
            ( 1,  1): "walk_SE", (-1,  1): "walk_SW",
            ( 1, -1): "walk_NE", (-1, -1): "walk_NW",
        }

        if self.is_moving and self.direction in ANIM_MAP:
            anim = ANIM_MAP[self.direction]
            if anim != self.current_anim:
                self.current_anim = anim
                self.frame_index = 0
            self.last_direction = anim
            self.frame_index = (self.frame_index + self.animation_speed) % len(self.walk_animations[self.current_anim])
            self.image = self.walk_animations[self.current_anim][int(self.frame_index)]
        else:
            self.image = self.idle_frames[self.last_direction]

    def try_use(self, index):
        if index < len(self.skills):
            return self.skills[index].try_use(self)
        return None
    
    def update(self):
        for skill in self.skills:
            skill.update()

    def get_infos(self):
        return {
            "position": self.get_pos(),
            "direction": self.direction,
            "is_moving": self.is_moving
        }


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