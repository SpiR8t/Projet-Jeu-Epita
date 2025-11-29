# il faut rajouter l'affichage du joueur dans la fonction draw_map

import pygame

# --- Paramètres de base ---
TILE_WIDTH = 64
TILE_HEIGHT = 32

MAP_HEIGHT = 8
MAP_WIDTH = 5
MAP_LEVELS = 3

# --- Génération d'une carte simple ---
tilemap = [
    [[0 for _ in range(MAP_LEVELS)] for _ in range(MAP_WIDTH)]
    for _ in range(MAP_HEIGHT)
]
tilemap_test = [
    [
        [1 if k == 0 else 2 if j == 0 or i == 0 else 0 for k in range(3)]
        for j in range(5)
    ]
    for i in range(8)
]


def cart_to_iso(x, y, z=0):
    screen_x = (x - y) * (TILE_WIDTH // 2) + 400
    screen_y = (x + y) * (TILE_HEIGHT // 2) - z * TILE_HEIGHT
    return screen_x, screen_y


def iso_to_cart_tile(screen_x, screen_y, z=0):
    # enlever l'offset de la caméra
    iso_x = screen_x - 400
    iso_y = screen_y + z * TILE_HEIGHT

    # inverser la matrice isométrique
    cart_x = (iso_y / (TILE_HEIGHT / 2) + iso_x / (TILE_WIDTH / 2)) / 2
    cart_y = (iso_y / (TILE_HEIGHT / 2) - iso_x / (TILE_WIDTH / 2)) / 2

    # renvoyer les tuiles arrondies
    return int(cart_x), int(cart_y)


class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = screen_width
        self.height = screen_height

    def center_on(self, x, y):
        self.offset_x = x - self.width / 2
        self.offset_y = y - self.height / 2

    def follow(self, x, y, smooth_factor=0.1):
        desired_x = x - self.width // 2
        desired_y = y - self.height // 2
        self.offset_x += (desired_x - self.offset_x) * smooth_factor
        self.offset_y += (desired_y - self.offset_y) * smooth_factor

    def apply(self, x, y):
        return x - self.offset_x, y - self.offset_y


class Map:
    def __init__(self, tiles, tile_width, tile_height, screen):
        self.tiles = tiles
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map_width = len(tiles[0])
        self.map_height = len(tiles)
        self.map_levels = len(tiles[0][0])
        self.screen = screen

    def draw_map(self, camera, x_j, y_j, avatar_j1):  # manque affichage joueur 2
        """fonction qui affiche la map (tiles)"""

        tile_wall = pygame.image.load("images/tilesettestwall.png").convert_alpha()
        tile_floor = pygame.image.load("images/tilesettestfloor.png").convert_alpha()
        avatar1 = pygame.image.load(avatar_j1).convert_alpha()

        j1_pos = iso_to_cart_tile(x_j, y_j)
        # dessine du fond vers devant
        for x in range(self.map_height):
            for y in range(self.map_width):

                for z in range(self.map_levels):
                    if x == j1_pos[0] and y == j1_pos[1] and z == 1:

                        x_j, y_j = camera.apply(x_j, y_j)
                        self.screen.blit(
                            avatar1, (x_j, y_j - 64)
                        )  # pour le décalage par rapport à la hauteur du pixel art avatar
                    print(j1_pos)

                    tile_nb = self.tiles[x][y][z]
                    if tile_nb != 0:
                        # Chaque condition correspond à une tile différente
                        screen_x, screen_y = cart_to_iso(x, y, z)
                        screen_x, screen_y = camera.apply(screen_x, screen_y)
                        if tile_nb == 1:
                            self.screen.blit(tile_floor, (screen_x, screen_y))
                        elif tile_nb == 2:
                            self.screen.blit(tile_wall, (screen_x, screen_y))
