import pygame
import math

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
        self.skills = [SwordAttack()]
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

class Action:
    def __init__(self, caster, range, name, x=0, y=0, dx=0, dy=0, host=True):
        """
        Classe mère pour toutes les actions.

        :param caster: Entité qui lance l'action (None si reçu du réseau)
        :param range: Portée de l'action
        :param name: Nom de l'action
        :param x, y: Position si action recréée via réseau
        :param dx, dy: Direction si action recréée via réseau
        :param host: True si action créée localement
        """

        self.range = range
        self.name = name
        self.host = host

        # Cas 1 : action créée localement
        if caster is not None:
            self.direction = caster.direction
            self.position = caster.get_pos()
        # Cas 2 : action reçue via réseau
        else:
            self.position = (x, y)
            self.direction = (dx, dy)

    def send_to_network(self, game):
        """
        Gère l'envoi réseau si nécessaire.
        """
        print("send")
        if self.host:
            game.action_created = True
            game.action_name_to_send.append(self.name)

    def execute(self, game):
        """
        À redéfinir dans les classes enfants.
        """
        raise NotImplementedError("execute() doit être implémentée.")

class MeleeAction(Action):

    def __init__(self, caster, range, x=0, y=0, dx=0, dy=0, host=True):
        super().__init__(caster, range, "Melee", x, y, dx, dy, host)

    def execute(self, game):
        print("Melee action")

        # gestion réseau commune
        self.send_to_network(game)

        dx, dy = self.direction

        # position devant le joueur
        target_x = self.position[0] + 16 + dx * 32
        target_y = self.position[1] - 16 + dy * 32

        anim = SimpleSlashAnimation(target_x, target_y, (dx, dy))
        game.animations.append(anim)



