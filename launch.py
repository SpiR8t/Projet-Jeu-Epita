"""Ce fichier est le fichier de base qui permet de lancer le jeu : c'est le seule à lancer."""

import pygame
import sys
import time

from game_context import GameContext
from player import *
from isometric_motor import *
from network import initiate_game,share_context_multi,reset_network
from menu import display_menu, reset_menu

def main():
    pygame.init()
    WIDTH, HEIGHT = 1280,720 #640, 360
    
    # Paramètres pour le dev :
    FULLSCREEN = False # Fenêtre ou fullscreen
    MULTIPLAYER = True # Activation du multijoueur
    
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Echoes of Lights")
    clock = pygame.time.Clock()

    map1 = Map(map_tiles, TILE_WIDTH, TILE_HEIGHT, screen)
    camera = Camera(screen.get_width(), screen.get_height())

    # Joueur
    playerH = Joueur(400, 150, 2, "assets/images/game/players/avatar.png", True)  # joueur host
    playerC = Joueur(400, 150, 2, "assets/images/game/players/avatar2.png", False)  # joueur client
    # ----

    context = GameContext(
        screen, clock, playerH, playerC, map1, camera, MULTIPLAYER
    )

    if not MULTIPLAYER:
        share_context_multi(context)

    while not context.quitting:
        # Menu
        if MULTIPLAYER:
            print("lancement menu")
            display_menu(context)

        initiate_game()
        reset_game(context)

    pygame.quit()
    sys.exit()

def reset_game(context):
    """Cette fonction reset tout ce qu'il faut reset pour recommencer une nouvelle partie après en avoir quitté une"""
    context.host_player.reset()
    context.client_player.reset()
    context.reset()
    reset_network()
    reset_menu()


if __name__ == "__main__":
    main()

