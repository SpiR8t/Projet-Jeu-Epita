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
        self.hitbox.x, self.hitbox.y = int(self.x + self.hitbox_offset_x), int(self.y + self.hitbox_offset_y)

    

class Player(Entity):
    def __init__(self, x, y, avatar_image, is_host):
        super().__init__(x, y, 100,2)
        self.avatar = avatar_image
        self.host = is_host
        self.direction = (0,-1)

        self.skills = [SwordAttack(), Interact()]
        
        # offset pour centrer la hitbox des joueurs (variables modifiables)
        self.hitbox_offset_x = -3
        self.hitbox_offset_y = -54
        self.hitbox = pygame.Rect(self.x+self.hitbox_offset_x, self.y+self.hitbox_offset_y, 23, 57)
        self.direction = (-1,-1)

        # Gestion de la spritesheet
        FRAME_W, FRAME_H = 57, 57
        SCALE = 1.5
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
            "is_moving": self.is_moving,
            "hitbox": [self.hitbox.x,self.hitbox.y,self.hitbox.width,self.hitbox.height],
        }


    # ====== Méthodes pour le déplacement

    def deduce_foots_from_iso_coords(self, player_x, player_y):
        """
        Fonction qui déduit la position des pieds gauches et droits à partir des coordonnées du joueur (déjà en isométrique)

        Param: player_x et player_y sont les coordonnées représentant la position du joueur gardé dans l'objet Player
        """

        return ((player_x - 32, player_y), (player_x + 1, player_y))  # il va falloir adapter au sprite du joueur

    def is_walkable(self, map_tiles, x, y, x_float, y_float):
        tile = map_tiles[x][y][1]
        # print(tile)
        walkable = False
        if tile == 0:
            walkable = True
        elif 24 == tile and y_float % 1 >= 0.2: # le but est de comparer l'endroit sur la tile
            walkable = True
        elif 25 == tile and y_float % 1 <= 0.8: # pareil
            walkable = True
        elif 26 == tile and x_float % 1 >= 0.2:
            walkable = True
        elif 27 == tile and x_float % 1 <= 0.8:
            walkable = True

        return walkable
    def foot_can_move(self, map_tiles, x, y):
        from isometric_motor import iso_to_cart_tile # pour éviter import circulaire au chargement

        grid_x, grid_y = iso_to_cart_tile(x,y, decimals=True)
        # print(grid_x, grid_y)
        return self.is_walkable(map_tiles, int(grid_x), int(grid_y), grid_x, grid_y)

    def detect_movement(self, keys, map_tiles):
        dx, dy = 0, 0

        x_player, y_player = self.get_pos()
        
        left_foot, right_foot = self.deduce_foots_from_iso_coords(x_player, y_player)

        # directions clavier
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_z]:
            dy = -1
        if keys[pygame.K_q]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1

        if dx == 0 and dy == 0:
            self.is_moving = False
            return

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

        self.hitbox.x, self.hitbox.y = int(self.x + self.hitbox_offset_x), int(self.y + self.hitbox_offset_y)

        self.direction = (dx, dy)
        self.is_moving = True


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