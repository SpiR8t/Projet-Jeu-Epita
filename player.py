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
        self.skills = [SwordAttack(), Interact()]
        
    def try_use(self, index):
        if index < len(self.skills):
            return self.skills[index].try_use(self)
        return None
    
    def update(self):
        for skill in self.skills:
            skill.update()


    # ====== Méthodes pour le déplacement

    def deduce_foots_from_iso_coords(self, player_x, player_y):
        """
        Fonction qui déduit la position des pieds gauches et droits à partir des coordonnées du joueur (déjà en isométrique)

        Param: player_x et player_y sont les coordonnées représentant la position du joueur gardé dans l'objet Player
        """

        return ((player_x - 32, player_y), (player_x + 1, player_y))

    def is_walkable(self, map_tiles, x, y):
        tile = map_tiles[x][y][1]
        return tile == 0 or 24 <= tile <= 27
    
    def foot_can_move(self, map_tiles, x, y):
        from isometric_motor import iso_to_cart_tile # pour éviter import circulaire au chargement

        grid_x, grid_y = iso_to_cart_tile(x,y)

        return self.is_walkable(map_tiles, grid_x, grid_y)

    def detect_movement(self, keys, map_tiles):
        dx, dy = 0, 0
        moved = False

        x_player, y_player = self.get_pos()

        left_foot, right_foot = self.deduce_foots_from_iso_coords(x_player, y_player)

        # directions clavier
        if keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1

        if dx == 0 and dy == 0:
            return

        moved = True

        # positions futures des pieds
        left_future = (
            left_foot[0] + dx * self.speed,
            left_foot[1] + dy * self.speed,
        )

        right_future = (
            right_foot[0] + dx * self.speed,
            right_foot[1] + dy * self.speed,
        )

        if (
            self.foot_can_move(map_tiles, *left_future)
            and self.foot_can_move(map_tiles, *right_future)
        ):
            self.x += dx * self.speed
            self.y += dy * self.speed

        if moved:
            self.direction = (dx, dy)


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