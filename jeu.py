import pygame
import sys

from player import *
from moteurIso import *

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.SCALED)
clock = pygame.time.Clock()


map1 = Map(tilemap_test, TILE_WIDTH, TILE_HEIGHT, screen)
camera1 = Camera(screen.get_width(), screen.get_height())

# Joueur
joueur1 = Joueur(400, 150, 2, "images/avatar2.png")
joueur2 = Joueur(400, 300, 2, "images/avatar2.png") # joueur qui est connecté en ligne
# ----

# faire une fonction qui lance le menu
# menuPrincipale()


# --- Boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((50, 50, 60))

    # simulation du mouvement du joueur
    joueur1.deplacer()

    # centre la caméro sur le joueur
    x_joueur, y_joueur = joueur1.get_pos()
    camera1.follow(x_joueur, y_joueur, 0.05)
    # afficher la map, avec le décalage imposé par la caméra
    map1.draw_map(camera1, x_joueur, y_joueur, joueur1.avatar)

    pygame.display.flip()
    clock.tick(60)
