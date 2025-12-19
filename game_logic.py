import pygame

def update_game(context,playerL,playerD):
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
    if keys[pygame.K_DOWN]:
        playerL.y -= playerL.vitesse
    if keys[pygame.K_UP]:
        playerL.y += playerL.vitesse
    if keys[pygame.K_LEFT]:
        playerL.x -= playerL.vitesse
    if keys[pygame.K_RIGHT]:
        playerL.x += playerL.vitesse

    # Fond
    context.screen.fill((50, 50, 60))

    # centre la caméro sur le joueur
    x_joueur, y_joueur = playerL.get_pos()
    context.camera.follow(x_joueur, y_joueur, 0.05)
    # afficher la map, avec le décalage imposé par la caméra
    context.map.draw_map(context.camera, x_joueur, y_joueur, playerL.avatar)

    pygame.display.flip()
    context.clock.tick(60)

def now():
    return pygame.time.get_ticks()