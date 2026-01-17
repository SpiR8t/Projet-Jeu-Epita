"""Ce fichier est le fichier de base qui permet de lancer le jeu : c'est le seule à lancer."""

import pygame
import sys
import time

from game_context import GameContext
from player import *
from isometric_motor import *
from network import initiate_game,share_context_multi
from menu import display_menu

def main():
    pygame.init()
    WIDTH, HEIGHT = 1920,1080 #640, 360
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Echoes of Lights")
    clock = pygame.time.Clock()

    # Activation du multijoueur
    MULTIPLAYER = False

    map1 = Map(map_tiles, TILE_WIDTH, TILE_HEIGHT, screen)
    camera = Camera(screen.get_width(), screen.get_height())

    # Joueur
    playerH = Joueur(400, 150, 2, "assets/images/game/players/avatar.png", True)  # joueur host
    playerC = Joueur(400, 150, 2, "assets/images/game/players/avatar2.png", False)  # joueur client
    # ----

    context = GameContext(
        screen, clock, playerH, playerC, map1, camera, MULTIPLAYER
    )

    # Menu
    if MULTIPLAYER:
        display_menu(context)
    else:
        share_context_multi(context)
    
    initiate_game()


if __name__ == "__main__":
    main()
