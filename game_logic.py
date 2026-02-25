import pygame
from isometric_motor import *
from menu_components import Button, TEXT, display_title

KEY_COOLDOWN = 300
CLICK_COOLDOWN = 300

last_key_pressed = 0

HEIGHT, WIDTH = 0,0
context = None

# Images HUD :
full_heart = pygame.image.load("assets/images/game/HUD/full_heart.png")
half_heart = pygame.image.load("assets/images/game/HUD/half_heart.png")
empty_heart = pygame.image.load("assets/images/game/HUD/empty_heart.png")

def share_info(gamecontext):
    """Partage les informations globales nécéssaires au fichier game_logic.py"""
    global context,HEIGHT,WIDTH,full_heart,half_heart,empty_heart
    context = gamecontext
    HEIGHT = context.screen.get_height()
    WIDTH = context.screen.get_width()

    # Scale les images :
    full_heart = pygame.transform.smoothscale(full_heart,(HEIGHT//20,HEIGHT//20))
    half_heart = pygame.transform.smoothscale(half_heart,(HEIGHT//20,HEIGHT//20))
    empty_heart = pygame.transform.smoothscale(empty_heart,(HEIGHT//20,HEIGHT//20))

def update_game(playerL, playerD):
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

    # récupération de la position du player pour vérifier les collisions durant le déplacement
    # les collisions sont gérées en regardant la position futur
    x_player1, y_player1 = playerL.get_pos()
    player1_leftfoot, player1_rightfoot = deduce_foots_from_iso_coords(
        x_player1, y_player1
    )

    # ===== Controls =====
    
    if not context.pause:
        if keys[pygame.K_DOWN]:
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
            # left foot
            l_x_grid_player1, l_y_grid_player1 = iso_to_cart_tile(
                player1_leftfoot[0] - playerL.speed, player1_leftfoot[1]
            )
    
            if map_tiles[l_x_grid_player1][l_y_grid_player1][1] == 0:
                playerL.x -= playerL.speed
    
        if keys[pygame.K_RIGHT]:
            # right foot
            r_x_grid_player1, r_y_grid_player1 = iso_to_cart_tile(
                player1_rightfoot[0] + playerL.speed, player1_rightfoot[1]
            )
    
            if map_tiles[r_x_grid_player1][r_y_grid_player1][1] == 0:
                playerL.x += playerL.speed

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

    draw_HUD(playerL)

    if context.pause:
        display_menu_pause(mouse_pos)

    pygame.display.flip()
    context.clock.tick(60)


def now():
    """Renvoie l'heure du jeu (en tick)"""
    return pygame.time.get_ticks()

def display_menu_pause(mouse_pos):
    """ Affiche le menu pause pour quitter le jeu ou retourner au menu principale"""
    
    # Fond noir transparent
    menu_surface = pygame.Surface((WIDTH,HEIGHT))
    menu_surface.set_alpha(128)
    menu_surface.fill((0,0,0))
    context.screen.blit(menu_surface,(0,0))
    # Affichage des boutons
    display_title(context,HEIGHT//6,"title")
    # Bouton de retour au jeu
    btn_go_back_game = Button(TEXT[context.language]["back"],HEIGHT//2,"go_back_game",context.screen)
    btn_go_back_game.draw(context.screen,mouse_pos)
    if btn_go_back_game.is_clicked(mouse_pos):
        if context.mouse_pressed and not context.mouse_pressed_last:
            context.pause_switch()
    # Bouton de retour au menu
    btn_go_menu = Button(TEXT[context.language]["main_menu"],4*HEIGHT//6,"go_main_menu",context.screen)
    btn_go_menu.draw(context.screen,mouse_pos)
    if btn_go_menu.is_clicked(mouse_pos):
        if context.mouse_pressed and not context.mouse_pressed_last:
            context.running = False
            
    # Bouton pour fermer le jeu
    btn_quit = Button(TEXT[context.language]["quit"],5*HEIGHT//6,"quit",context.screen)
    btn_quit.draw(context.screen,mouse_pos)
    if btn_quit.is_clicked(mouse_pos):
        if context.mouse_pressed and not context.mouse_pressed_last:
            context.running = False
            context.quitting = True

def draw_HUD(playerL):
    HUD_surface = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    HUD_surface.fill((0, 0, 0, 0))
    draw_health(playerL,HUD_surface)
    context.screen.blit(HUD_surface,(0,0))

def draw_health(playerL,HUD_surface):
    global full_heart,half_heart,empty_heart

    nb_full_hearts = playerL.hp // 2
    nb_half_hearts = playerL.hp % 2
    total_hearts = playerL.max_hp // 2
    y_pos = HEIGHT//40
    x_pos = HEIGHT//40
    
    for i in range(total_hearts):
        if i < nb_full_hearts:
            HUD_surface.blit(full_heart, (x_pos, y_pos))
        elif i == nb_full_hearts and nb_half_hearts == 1:
            HUD_surface.blit(half_heart, (x_pos, y_pos))
        else:
            HUD_surface.blit(empty_heart, (x_pos, y_pos))
        x_pos += 5*HEIGHT//80

