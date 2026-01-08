import pygame

# --- Paramètres de base ---
TILE_WIDTH = 64
TILE_HEIGHT = 32

MAP_HEIGHT = 10
MAP_WIDTH = 15
MAP_LEVELS = 3

# --- Génération d'une carte simple ---
map_tiles = [
    [
        [
            (
                1
                if k == 0
                else (
                    2
                    if j == 0 or i == 0 or j == MAP_WIDTH - 1 or i == MAP_HEIGHT - 1
                    else 0
                )
            )
            for k in range(MAP_LEVELS)
        ]
        for j in range(MAP_WIDTH)
    ]
    for i in range(MAP_HEIGHT)
]


# --- Fonction de conversion cartésien <-> isométrique
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


def deduce_foots_from_iso_coords(player_x, player_y):
    return ((player_x - 32, player_y), (player_x + 1, player_y))


class Camera:
    # la classe qui permet de garder l'offset constant de l'affichage du joueur
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


def display_ranges(x_j1, y_j1):
    """
    Détermine la range de coordonnées de la matrice qui se trouve à l'écran, pour afficher seulement le nécessaire.
    La partie Z n'est pas renvoyé car elle est toujours affiché de 0 à 2 (pour une hauteur de 3)

    Param: x_j1 et y_j1 sont considérés déjà converti vers les coordonnées de la matrice
    """

    # il faudra adapter la marge à la taille de l'écran, peut être agrandir la taille de l'affichage pour les écran plus grand ?
    x_min = max(0, x_j1 - 16)
    x_max = min(len(map_tiles), x_j1 + 16)

    y_min = max(0, y_j1 - 16)
    y_max = min(len(map_tiles[0]), y_j1 + 16)

    return ((x_min, x_max), (y_min, y_max))


class Map:
    def __init__(self, tiles, tile_width, tile_height, screen):
        self.tiles = tiles
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.map_width = len(tiles[0])
        self.map_height = len(tiles)
        self.map_levels = len(tiles[0][0])
        self.screen = screen

    def draw_map(
        self, camera, x_j1, y_j1, avatar_j1, x_j2, y_j2, avatar_j2
    ):  # manque affichage joueur 2
        """fonction qui affiche la map (tiles)"""

        tile_wall = pygame.image.load("assets/images/game/tileset/tilesettestwall.png").convert_alpha()
        tile_floor = pygame.image.load("assets/images/game/tileset/tilesettestfloor.png").convert_alpha()
        avatar1 = pygame.image.load(avatar_j1).convert_alpha()
        avatar2 = pygame.image.load(avatar_j2).convert_alpha()

        j1_pos = iso_to_cart_tile(x_j1, y_j1)
        j2_pos = iso_to_cart_tile(x_j2, y_j2)

        ((x_min, x_max), (y_min, y_max)) = display_ranges(j1_pos[0], j1_pos[1])

        # dessine du fond vers devant
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):

                for z in range(self.map_levels):
                    if x == j1_pos[0] and y == j1_pos[1] and z == 1:

                        x_j1, y_j1 = camera.apply(x_j1, y_j1)
                        self.screen.blit(
                            avatar1, (x_j1, y_j1 - 64)
                        )  # pour le décalage par rapport à la hauteur du pixel art avatar
                    # print(j1_pos)
                    if x == j2_pos[0] and y == j2_pos[1] and z == 1:

                        x_j2, y_j2 = camera.apply(x_j2, y_j2)
                        self.screen.blit(
                            avatar2, (x_j2, y_j2 - 64)
                        )  # pour le décalage par rapport à la hauteur du pixel art avatar
                    # print(j1_pos)

                    tile_nb = self.tiles[x][y][z]
                    if tile_nb != 0:
                        # Chaque condition correspond à une tile différente
                        screen_x, screen_y = cart_to_iso(x, y, z)
                        screen_x, screen_y = camera.apply(screen_x, screen_y)
                        if tile_nb == 1:
                            self.screen.blit(tile_floor, (screen_x, screen_y))
                        elif tile_nb == 2:
                            self.screen.blit(tile_wall, (screen_x, screen_y))
