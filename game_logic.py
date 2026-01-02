import pygame
from moteurIso import *


def update_game(context, playerL, playerD):
    """
    Cette fonction correspond à ce qu'il se passe dans la boucle principale du jeu.
    playerL -> joueur local, playerD  -> joueur distant
    """

    # Gestion si on ferme la fenetre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            context.running = False

    # Gestion de la pression des touches
    keys = pygame.key.get_pressed()

    x_joueur1, y_joueur1 = playerL.get_pos()
    x_grid_joueur1, y_grid_joueur1 = iso_to_cart_tile(x_joueur1, y_joueur1)

    if keys[pygame.K_DOWN]:
        x_joueur1, y_joueur1 = playerL.get_pos()
        x_grid_joueur1, y_grid_joueur1 = iso_to_cart_tile(
            x_joueur1, y_joueur1 + playerL.vitesse
        )
        if map_tiles[x_grid_joueur1][y_grid_joueur1][1] == 0:
            playerL.y += playerL.vitesse

    if keys[pygame.K_UP]:
        x_joueur1, y_joueur1 = playerL.get_pos()
        x_grid_joueur1, y_grid_joueur1 = iso_to_cart_tile(
            x_joueur1, y_joueur1 - playerL.vitesse
        )
        if map_tiles[x_grid_joueur1][y_grid_joueur1][1] == 0:
            playerL.y -= playerL.vitesse
    if keys[pygame.K_LEFT]:
        x_joueur1, y_joueur1 = playerL.get_pos()
        x_grid_joueur1, y_grid_joueur1 = iso_to_cart_tile(
            x_joueur1 - playerL.vitesse, y_joueur1 + playerL.vitesse
        )
        if map_tiles[x_grid_joueur1][y_grid_joueur1][1] == 0:
            playerL.x -= playerL.vitesse
    if keys[pygame.K_RIGHT]:
        x_joueur1, y_joueur1 = playerL.get_pos()
        x_grid_joueur1, y_grid_joueur1 = iso_to_cart_tile(
            x_joueur1 + playerL.vitesse, y_joueur1 + playerL.vitesse
        )
        if map_tiles[x_grid_joueur1][y_grid_joueur1][1] == 0:
            playerL.x += playerL.vitesse

    # Fond
    context.screen.fill((50, 50, 60))

    # centre la caméro sur le joueur
    x_joueur1, y_joueur1 = playerL.get_pos()
    x_joueur2, y_joueur2 = playerD.get_pos()

    # print("Coords : x = ",x_joueur, "y = ", y_joueur)
    context.camera.follow(x_joueur1, y_joueur1, 0.05)
    # afficher la map, avec le décalage imposé par la caméra
    context.map.draw_map(
        context.camera,
        x_joueur1,
        y_joueur1,
        playerL.avatar,
        x_joueur2,
        y_joueur2,
        playerD.avatar,
    )

    pygame.display.flip()
    context.clock.tick(60)


def now():
    """Renvoie l'heure du jeu (en tick)"""
    return pygame.time.get_ticks()


def end_game():
    pygame.quit()
