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

    def deduce_foots_from_iso_coords(self, player_x, player_y):
        """
        Fonction qui déduit la position des pieds gauches et droits à partir des coordonnées du joueur (déjà en isométrique)

        Param: player_x et player_y sont les coordonnées représentant la position du joueur gardé dans l'objet Player
        """

        return ((player_x - 32, player_y), (player_x + 1, player_y))

    def detect_movement(self, keys, map_tiles):
        from isometric_motor import iso_to_cart_tile # pour éviter import circulaire au chargement
        dx,dy = 0,0
        moved = False
        # récupération de la position du player pour vérifier les collisions durant le déplacement
        # les collisions sont gérées en regardant la position futur
        x_player1, y_player1 = self.get_pos()
        player1_leftfoot, player1_rightfoot = self.deduce_foots_from_iso_coords(
            x_player1, y_player1
        )

        if keys[pygame.K_DOWN]:
            dy += 1
            moved = True

            # left foot
            l_x_grid_player1, l_y_grid_player1 = iso_to_cart_tile(
                player1_leftfoot[0], player1_leftfoot[1] + self.speed
            )
            # right foot
            r_x_grid_player1, r_y_grid_player1 = iso_to_cart_tile(
                player1_rightfoot[0], player1_rightfoot[1] + self.speed
            )
            if (
                (map_tiles[l_x_grid_player1][l_y_grid_player1][1] == 0
                and map_tiles[r_x_grid_player1][r_y_grid_player1][1] == 0)
                or (24 <= map_tiles[l_x_grid_player1][l_y_grid_player1][1] <= 27
                and 24 <= map_tiles[r_x_grid_player1][r_y_grid_player1][1] <= 27)
            ):
                self.y += self.speed
        
        if keys[pygame.K_UP]:
            dy -= 1
            moved = True

            # left foot
            l_x_grid_player1, l_y_grid_player1 = iso_to_cart_tile(
                player1_leftfoot[0], player1_leftfoot[1] - self.speed
            )
            # right foot
            r_x_grid_player1, r_y_grid_player1 = iso_to_cart_tile(
                player1_rightfoot[0], player1_rightfoot[1] - self.speed
            )

            if (
                (map_tiles[l_x_grid_player1][l_y_grid_player1][1] == 0
                and map_tiles[r_x_grid_player1][r_y_grid_player1][1] == 0)
                or (24 <= map_tiles[l_x_grid_player1][l_y_grid_player1][1] <= 27
                and 24 <= map_tiles[r_x_grid_player1][r_y_grid_player1][1] <= 27)
            ):
                self.y -= self.speed

        if keys[pygame.K_LEFT]:
            dx -= 1
            moved = True

            # left foot
            l_x_grid_player1, l_y_grid_player1 = iso_to_cart_tile(
                player1_leftfoot[0] - self.speed, player1_leftfoot[1]
            )

            if (
                map_tiles[l_x_grid_player1][l_y_grid_player1][1] == 0
                or 24 <= map_tiles[l_x_grid_player1][l_y_grid_player1][1] <= 27
            ):
                self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            dx += 1
            moved = True

            # right foot
            r_x_grid_player1, r_y_grid_player1 = iso_to_cart_tile(
                player1_rightfoot[0] + self.speed, player1_rightfoot[1]
            )


            if (
                map_tiles[r_x_grid_player1][r_y_grid_player1][1] == 0
                or 24 <= map_tiles[r_x_grid_player1][r_y_grid_player1][1] <= 27
            ):
                self.x += self.speed
        
        if moved: self.direction = (dx,dy)


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