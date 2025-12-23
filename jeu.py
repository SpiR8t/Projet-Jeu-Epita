"""Ce fichier est le fichier de base qui permet de lancer le jeu : c'est le seule à lancer."""

import pygame
import sys

from game_context import GameContext
from player import *
from moteurIso import *
from network import start_network, network_ready, initiate_game

def main():
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    clock = pygame.time.Clock()

    map1 = Map(tilemap_test, TILE_WIDTH, TILE_HEIGHT, screen)
    camera = Camera(screen.get_width(), screen.get_height())


    # Joueur
    playerH = Joueur(400, 150, 2, "images/avatar.png",True) # joueur host 
    playerC = Joueur(400, 150, 2, "images/avatar2.png",False) # joueur client
    # ----

    context = GameContext(screen, clock,playerH,playerC,WIDTH,HEIGHT,map1,camera)

    # faire une fonction qui lance le menu
    # menuPrincipale()

    # Gestion du multijoueur
    # Faire en sorte que dans le menu on puisse choisir si on host ou si on rejoint une partie
    play_as_host = (input("En tant que host ? (T/F) ") == "T") # Temporaire en attendant le menu
    start_network(play_as_host,context)
    network_ready.wait()
    initiate_game()



if __name__ == "__main__":
    main()