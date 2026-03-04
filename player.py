import pygame
import math
from isometric_motor import iso_to_cart_tile 

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
    def __init__(self, name, host=True):
        """
        Classe mère pour toutes les actions.

        """
        
        self.name = name
        self.host = host

    def send_to_network(self, context):
        """
        Gère l'envoi réseau si nécessaire.
        """
        print("send")
        if self.host:
            context.action_created = True
            context.action_name_to_send.append(self.name)

    def execute(self):
        """
        À redéfinir dans les classes enfants.
        """
        raise NotImplementedError("execute() doit être implémentée.")

class MeleeAction(Action):

    def __init__(self, caster, range, x=0, y=0, dx=0, dy=0, host=True):
        super().__init__("Melee", host)
        self.range = range

        # Cas 1 : action créée localement
        if caster is not None:
            self.direction = caster.direction
            self.position = caster.get_pos()
        # Cas 2 : action reçue via réseau
        else:
            self.position = (x, y)
            self.direction = (dx, dy)

    def execute(self, context):
        print("Melee action")

        # gestion réseau commune
        self.send_to_network(context)

        dx, dy = self.direction

        # position devant le joueur
        target_x = self.position[0] + 16 + dx * 32
        target_y = self.position[1] - 16 + dy * 32

        anim = SimpleSlashAnimation(target_x, target_y, (dx, dy))
        context.animations.append(anim)

class LeverAction(Action): # l'action pour switch un levier
    def __init__(self, id_group, id_lever, host=True):
        super().__init__("Lever Action", host)

        self.id_group = id_group
        self.id_lever = id_lever

    def send_to_network(self, context):
        super().send_to_network(context)
        context.add_info_lever_action(self.id_group, self.id_lever) # on ajoute une instruction pour envoyer les
                                                                    # infos du levier dans le multi 
    def execute(self, context, gameRegister, matrix):
        if gameRegister.levers[self.id_group][self.id_lever].locked != True:
            self.send_to_network(context)
            
            gameRegister.levers[self.id_group][self.id_lever].toggle(matrix)

class interactAction(Action):
    def __init__(self, x,y, host=True):
        super().__init__("Interact Action", host)
        self.x = x
        self.y = y

    def send_to_network(self, context, coords_carto): # on envoie les coordonnées de l'endroit de l'interaction avec
        super().send_to_network(context)
        context.add_info_interact_action(coords_carto)

    def leverVerif(self, gameRegister, x,y): # une méthode pour checker les levier, il en faudra d'autres pour les autres éléments
        for group in gameRegister.levers:
            for lever in gameRegister.levers[group]:
                if lever.position == (x,y):
                    return (lever.group, lever.id)

    def execute(self, context, gameRegister):
        
        carto = iso_to_cart_tile(self.x, self.y)
        self.send_to_network(context, carto)
        # vérif pour levier
        lever = self.leverVerif(gameRegister, carto[0],carto[1])
        if (lever) :
            context.add_action(LeverAction(lever[0], lever[1]))

        # vérif pour d'autres choses interactive par la suite
        # ->

        # if interact a fait qlq chose il faudra faire animation interaction