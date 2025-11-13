import pygame
import sys

from moteurIso import *

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.SCALED)
clock = pygame.time.Clock()


map1 = Map(tilemap_test, TILE_WIDTH, TILE_HEIGHT, screen)
camera1 = Camera(screen.get_width(), screen.get_height())


# simulation des coordonées d'un joueur
x_joueur, y_joueur = 400, 300
speed = 10
# ----


# --- Boucle principale ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((50, 50, 60))

    # simulation du mouvement du joueur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_joueur -= speed
    if keys[pygame.K_RIGHT]:
        x_joueur += speed
    if keys[pygame.K_UP]:
        y_joueur -= speed
    if keys[pygame.K_DOWN]:
        y_joueur += speed

    # centre la caméro sur le joueur
    camera1.follow(x_joueur, y_joueur, 0.05)
    # afficher la map, avec le décalage imposé par la caméra
    map1.draw_map(camera1)

    pygame.display.flip()
    clock.tick(60)
