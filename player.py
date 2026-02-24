import pygame


class Joueur:
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
    def __init__(self, x, y, duration=10):
        self.x = x
        self.y = y
        self.duration = duration
        self.timer = 0
        self.finished = False

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True

    def draw(self, screen, camera):
        # effet très simple : cercle blanc qui grandit
        radius = 5 + self.timer * 2
        
        screen_x, screen_y = camera.apply(self.x, self.y)
        
        pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), radius, 2)

class MeleeAction:

    def __init__(self, caster, range):
        self.caster = caster
        self.range = range

    def execute(self, game):
        print("Melee action")

        # position devant le joueur
        target_x = self.caster.x + self.caster.direction[0] * 32
        target_y = self.caster.y + self.caster.direction[1] * 32

        anim = SimpleSlashAnimation(target_x, target_y, duration=10)
        game.animations.append(anim)



