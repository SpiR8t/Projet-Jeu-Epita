import pygame
from isometric_motor import *
from menu_components import Button, TEXT, display_title
from gameStateRegistry import gameRegistry

import actions

KEY_COOLDOWN = 300

last_key_pressed = 0

HEIGHT, WIDTH = 0,0
context = None

# Images HUD :
full_heart = pygame.image.load("assets/images/game/HUD/full_heart.png")

def share_info(gamecontext):
    """Partage les informations globales nécéssaires au fichier game_logic.py"""
    global context, HEIGHT,WIDTH,full_heart,half_heart,empty_heart
    context = gamecontext
    HEIGHT = context.screen.get_height()
    WIDTH = context.screen.get_width()

    # Scale les images :
    full_heart = pygame.transform.smoothscale(full_heart,(HEIGHT//20,HEIGHT//20))

def update_game(playerL, playerD,):
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
        playerL.detect_movement(keys, map_tiles)
        playerL.update()
        

        # Skill
        if keys[pygame.K_SPACE]: # Sword attack
            action = playerL.try_use(0)
            if action:
                context.add_action(action)
        # interact
        if keys[pygame.K_e]: # Sword attack
            action = playerL.try_use(1)
            if action:
                context.add_action(action)

        # ========= Temporaire pour tester degats ==============
        if keys[pygame.K_c]: # Changement de la map : ouvre/ferme toutes les portes du groupe 255
            if now() - last_key_pressed >= KEY_COOLDOWN:
                for door in gameRegistry.doors[255]:
                    action = door.open_close()
                    if action:
                        context.add_action(action)
                last_key_pressed = now()
        # ======================================================

        # ========= Temporaire pour tester degats ==============
        if keys[pygame.K_k]: # Retrait de PV au joueur local
            if now() - last_key_pressed >= KEY_COOLDOWN-200:
                playerL.take_damage(1)
                last_key_pressed = now()

        # ========= Temporaire pour débug ======================
        if keys[pygame.K_g]: # affichage des leviers
            if now() - last_key_pressed >= KEY_COOLDOWN-200:
                print(gameRegistry.levers)
                last_key_pressed = now()

        # ========= Temporaire pour tester levier ======================
        if keys[pygame.K_h]: 
            if now() - last_key_pressed >= KEY_COOLDOWN:
                action = actions.LeverAction(46,2)
                action.execute(context, gameRegistry, context.map)
                last_key_pressed = now()
        # ======================================================


    # Mise à jour des ennemis
    if playerL.host:
        for ennemy in context.ennemies:
            action = ennemy.update(playerL)
            if action:
                context.add_action(action)

    if keys[pygame.K_ESCAPE]: # Activation du menu pause
        if now() - last_key_pressed >= KEY_COOLDOWN:
            context.pause_switch()
            last_key_pressed = now()

    # Fond
    context.screen.fill((50, 50, 60))

    # centre la caméra sur le player
    x_player1, y_player1 = playerL.get_pos()
    x_player2, y_player2 = playerD.get_pos()

    playerL.update_animation()
    playerD.update_animation()

    context.camera.follow(x_player1, y_player1, 0.05)
    # afficher la map, avec le décalage imposé par la caméra
    context.map.draw_map(
        context.camera,
        x_player1,
        y_player1,
        playerL.image,
        x_player2,
        y_player2,
        playerD.image,
    )
    # Affichage des ennemis (À integrer dans le code du moteur isométique plus tard)
    for e in context.ennemies:
        # affichage de l'ennemi
        pos_ecran = context.camera.apply(e.x, e.y)
        context.screen.blit(e.image, (pos_ecran[0], pos_ecran[1] - 64))

    if context.hitboxs:
        draw_hitboxs(playerL,playerD)

    # Draw du HUD
    if context.hud:
        draw_HUD(playerL)

    if context.pause:
        display_menu_pause(mouse_pos)


    check_player_life_state(playerL)

    # animations des compétences
    context.execute_actions(gameRegistry)
    context.update_animations()
    context.draw_animations()
    # pygame.draw.circle(context.screen, (255, 0, 0), (context.camera.apply(playerL.get_pos()[0], playerL.get_pos()[1])), 4) #débug
    pygame.display.flip()
    context.clock.tick(60)

def now():
    """Renvoie l'heure du jeu (en tick)"""
    return pygame.time.get_ticks()

def draw_hitboxs(playerL,playerD):
    for e in context.ennemies:
        # affichage de l'ennemi
        pos_ecran = context.camera.apply(e.x, e.y)
        context.screen.blit(e.image, (int(pos_ecran[0]), int(pos_ecran[1]) - 64))

        #affichage de la hitbox de l'ennemi
        e_x, e_y = context.camera.apply(e.hitbox.x, e.hitbox.y)
        pygame.draw.rect(context.screen, (255,125,0), (e_x, e_y, e.hitbox.width, e.hitbox.height), 2)

        #CREATION DU RECTANGLE ROUGE
        if e.damage_zone != None: # si une zone d'attaque existe
            # conversion map -> écran via la caméra
            rect_pos = context.camera.apply(e.damage_zone.x, e.damage_zone.y)

            # on crée le rectangle à afficher
            draw_rect = pygame.Rect(rect_pos[0], rect_pos[1], e.damage_zone.width, e.damage_zone.height)

            # rectangle rouge
            pygame.draw.rect(context.screen, (255, 0, 0), draw_rect, 2)

    #MÊME CHOSE POUR LES JOUEURS :
    p_x, p_y = context.camera.apply(playerL.hitbox.x, playerL.hitbox.y)
    pygame.draw.rect(context.screen, (0, 0, 255), (p_x, p_y, playerL.hitbox.width, playerL.hitbox.height), 2)
    p_x, p_y = context.camera.apply(playerD.hitbox.x, playerD.hitbox.y)
    pygame.draw.rect(context.screen, (255, 0, 255), (p_x, p_y, playerD.hitbox.width, playerD.hitbox.height), 2)

def display_menu_pause(mouse_pos):
    """ Affiche le menu pause pour quitter le jeu ou retourner au menu principale"""
    
    # Fond noir transparent
    menu_surface = pygame.Surface((WIDTH,HEIGHT))
    menu_surface.set_alpha(128)
    menu_surface.fill((0,0,0))
    context.screen.blit(menu_surface,(0,0))
    # Affichage des boutons
    display_title(context,HEIGHT//6,"title",(255,255,255))
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
    draw_health_bar(playerL,HUD_surface)
    context.screen.blit(HUD_surface,(0,0))

def draw_health_bar(playerL,HUD_surface):
    global full_heart
    HUD_surface.blit(full_heart, (HEIGHT//40, HEIGHT//40))
    
    ratio = playerL.hp / playerL.max_hp
    ratio = max(0, min(1, ratio))

    bar_height = HEIGHT//30
    bar_width = WIDTH//3
    x_pos, y_pos = HEIGHT//10, HEIGHT//30
    bar_color = (100+(100*ratio),0,0)

    # Fond (barre vide)
    pygame.draw.rect(HUD_surface, (50, 0, 0), (x_pos, y_pos, bar_width, bar_height))
    # Vie actuelle
    pygame.draw.rect(HUD_surface, bar_color, (x_pos, y_pos, bar_width * ratio, bar_height))
    # Bordure
    pygame.draw.rect(HUD_surface, (0, 0, 0), (x_pos, y_pos, bar_width, bar_height), 2)

def check_player_life_state(playerL):
    if playerL.hp == 0:
        playerL.respawn()