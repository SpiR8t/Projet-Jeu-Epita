import pygame
from isometric_motor import *
from menu_components import Button, TEXT, display_title

KEY_COOLDOWN = 300
CLICK_COOLDOWN = 300

last_key_pressed = 0

def update_game(context, playerL, playerD):
    """
    Cette fonction correspond à ce qu'il se passe dans la boucle principale du jeu.
    playerL -> player local, playerD  -> player distant
    """
    global last_key_pressed, last_click
    # Gestion si on ferme la fenetre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            context.running = False
            context.quitting = True

    # Gestion de la pression des touches
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    context.mouse_pressed_last = context.mouse_pressed
    context.mouse_pressed = pygame.mouse.get_pressed()[0]


    # ===== Controls =====
    
    if not context.pause:
        
        # Movements
        detect_player_movement(keys, playerL)
        playerL.update()

        # Skill
        if keys[pygame.K_SPACE]: # Sword attack
            action = playerL.try_use(0)
            
            if action:
                context.execute_action(action)

    if keys[pygame.K_ESCAPE]: # Activation du menu pause
        if now() - last_key_pressed >= KEY_COOLDOWN:
            context.pause_switch()
            last_key_pressed = now()

    # Fond
    context.screen.fill((50, 50, 60))

    # centre la caméro sur le player
    x_player1, y_player1 = playerL.get_pos()
    x_player2, y_player2 = playerD.get_pos()

    # print("Coords : x = ",x_player, "y = ", y_player)
    context.camera.follow(x_player1, y_player1, 0.05)
    # afficher la map, avec le décalage imposé par la caméra
    context.map.draw_map(
        context.camera,
        x_player1,
        y_player1,
        playerL.avatar,
        x_player2,
        y_player2,
        playerD.avatar,
    )

    if context.pause:
        display_menu_pause(context, mouse_pos)

    # animations des compétences
    context.update_animations()
    context.draw_animations()

    pygame.display.flip()
    context.clock.tick(60)


def now():
    """Renvoie l'heure du jeu (en tick)"""
    return pygame.time.get_ticks()

def display_menu_pause(context,mouse_pos):
    """ Affiche le menu pause pour quitter le jeu ou retourner au menu principale"""
    height = context.screen.get_height()
    width = context.screen.get_width()
    
    # Fond noir transparent
    menu_surface = pygame.Surface((width,height))
    menu_surface.set_alpha(128)
    menu_surface.fill((0,0,0))
    context.screen.blit(menu_surface,(0,0))
    # Affichage des boutons
    display_title(context,height//6,"title")
    # Bouton de retour au jeu
    btn_go_back_game = Button(TEXT[context.language]["back"],height//2,"go_back_game",context.screen)
    btn_go_back_game.draw(context.screen,mouse_pos)
    if btn_go_back_game.is_clicked(mouse_pos):
        if context.mouse_pressed and not context.mouse_pressed_last:
            context.pause_switch()
    # Bouton de retour au menu
    btn_go_menu = Button(TEXT[context.language]["main_menu"],4*height//6,"go_main_menu",context.screen)
    btn_go_menu.draw(context.screen,mouse_pos)
    if btn_go_menu.is_clicked(mouse_pos):
        if context.mouse_pressed and not context.mouse_pressed_last:
            context.running = False
            
    # Bouton pour fermer le jeu
    btn_quit = Button(TEXT[context.language]["quit"],5*height//6,"quit",context.screen)
    btn_quit.draw(context.screen,mouse_pos)
    if btn_quit.is_clicked(mouse_pos):
        if context.mouse_pressed and not context.mouse_pressed_last:
            context.running = False
            context.quitting = True

def detect_player_movement(keys, playerL):
    dx,dy = 0,0
    moved = False
    # récupération de la position du player pour vérifier les collisions durant le déplacement
    # les collisions sont gérées en regardant la position futur
    x_player1, y_player1 = playerL.get_pos()
    player1_leftfoot, player1_rightfoot = deduce_foots_from_iso_coords(
        x_player1, y_player1
    )

    if keys[pygame.K_DOWN]:
        dy += 1
        moved = True

        # left foot
        l_x_grid_player1, l_y_grid_player1 = iso_to_cart_tile(
            player1_leftfoot[0], player1_leftfoot[1] + playerL.speed
        )
        # right foot
        r_x_grid_player1, r_y_grid_player1 = iso_to_cart_tile(
            player1_rightfoot[0], player1_rightfoot[1] + playerL.speed
        )
        if (
            map_tiles[l_x_grid_player1][l_y_grid_player1][1] == 0
            and map_tiles[r_x_grid_player1][r_y_grid_player1][1] == 0
        ):
            playerL.y += playerL.speed
    
    if keys[pygame.K_UP]:
        dy -= 1
        moved = True

        # left foot
        l_x_grid_player1, l_y_grid_player1 = iso_to_cart_tile(
            player1_leftfoot[0], player1_leftfoot[1] - playerL.speed
        )
        # right foot
        r_x_grid_player1, r_y_grid_player1 = iso_to_cart_tile(
            player1_rightfoot[0], player1_rightfoot[1] - playerL.speed
        )

        if (
            map_tiles[l_x_grid_player1][l_y_grid_player1][1] == 0
            and map_tiles[r_x_grid_player1][r_y_grid_player1][1] == 0
        ):
            playerL.y -= playerL.speed

    if keys[pygame.K_LEFT]:
        dx -= 1
        moved = True

        # left foot
        l_x_grid_player1, l_y_grid_player1 = iso_to_cart_tile(
            player1_leftfoot[0] - playerL.speed, player1_leftfoot[1]
        )

        if map_tiles[l_x_grid_player1][l_y_grid_player1][1] == 0:
            playerL.x -= playerL.speed

    if keys[pygame.K_RIGHT]:
        dx += 1
        moved = True

        # right foot
        r_x_grid_player1, r_y_grid_player1 = iso_to_cart_tile(
            player1_rightfoot[0] + playerL.speed, player1_rightfoot[1]
        )

        if map_tiles[r_x_grid_player1][r_y_grid_player1][1] == 0:
            playerL.x += playerL.speed
    
    if moved: playerL.direction = (dx,dy)