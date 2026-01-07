"""Ce fichier est le fichier de base qui permet de lancer le jeu : c'est le seule à lancer."""

import pygame
import sys
import time

from game_context import GameContext
from player import *
from moteurIso import *
from network import initiate_game
from menu import display_menu

def main():
    pygame.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Echoes of Lights")
    clock = pygame.time.Clock()

    # Activation du multijoueur
    MULTIPLAYER = True

    map1 = Map(map_tiles, TILE_WIDTH, TILE_HEIGHT, screen)
    camera = Camera(screen.get_width(), screen.get_height())

    # Joueur
    playerH = Joueur(400, 150, 2, "assets/images/game/players/avatar.png", True)  # joueur host
    playerC = Joueur(400, 150, 2, "assets/images/game/players/avatar2.png", False)  # joueur client
    # ----

    context = GameContext(
        screen, clock, playerH, playerC, WIDTH, HEIGHT, map1, camera, MULTIPLAYER
    )

    # Menu
    display_menu(context)

    # Gestion du multijoueur
    # Faire en sorte que dans le menu on puisse choisir si on host ou si on rejoint une partie
    
    initiate_game()


if __name__ == "__main__":
    main()
