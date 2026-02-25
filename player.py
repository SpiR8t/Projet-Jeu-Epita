import pygame
import math

class Player:
    def __init__(self, x, y, vitesse, avatar_image, is_host):
        self.x_origine = x
        self.y_origine = y
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.avatar = avatar_image
        self.host = is_host
        self.direction = (-1,-1) # pour les compétences
        
        self.skills = [SwordAttack()] # hardcodé pour l'instant

    def get_pos(self):
        return (self.x, self.y)
    
    def reset(self):
        self.x = self.x_origine
        self.y = self.y_origine
        
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
            return self.create_action(caster)

    def create_action(self, caster):
        raise NotImplementedError("create_action must be overridden")

class SwordAttack(Skill):
    def __init__(self):
        super().__init__(cooldown=100, range=1)

    def create_action(self, caster):
        return MeleeAction(caster, self.range)

class SimpleSlashAnimation:
    def __init__(self, x, y, direction, duration=8):
        self.x = x
        self.y = y
        self.direction = direction
        self.duration = duration
        self.timer = 0
        self.finished = False

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True

    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)

        size = 40
        rect = pygame.Rect(
            screen_x - size//2,
            screen_y - size//2,
            size,
            size
        )

        dx, dy = self.direction

        # angles en radians
        if (dx, dy) == (0, -1):  # haut
            start_angle = math.radians(200)
            end_angle = math.radians(340)

        elif (dx, dy) == (0, 1):  # bas
            start_angle = math.radians(20)
            end_angle = math.radians(160)

        elif (dx, dy) == (-1, 0):  # gauche
            start_angle = math.radians(110)
            end_angle = math.radians(250)

        elif (dx, dy) == (1, 0):  # droite
            start_angle = math.radians(-70)
            end_angle = math.radians(70)

        else:
            start_angle = 0
            end_angle = math.pi

        pygame.draw.arc(screen, (255, 255, 255), rect, start_angle, end_angle, 4)

class MeleeAction:

    def __init__(self, caster, range):
        self.caster = caster
        self.range = range

    def execute(self, game):
        print("Melee action")

        dx,dy = self.caster.direction

        # position devant le joueur
        target_x = self.caster.x+16 + dx * 32
        target_y = self.caster.y-16 + dy * 32
        anim = SimpleSlashAnimation(target_x, target_y, (dx, dy))
        game.animations.append(anim)



