import pygame
import sys

from menu_components import Button, WHITE,BLACK,LIGHT_GREY,BUTTON_BG,DARK_GREY,TEXT
from network import start_network, network_ready, share_context_multi

WIDTH, HEIGHT = 1280,720

background = pygame.image.load("assets/images/menu/menu_bg.png")

volume = 0.5
pygame.mixer.init()
pygame.mixer.music.load("assets/audio/musics/musique_val.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

COOLDOWN_TIME = 200  

page = "menu"
language = "FR"
code_multi = ""

def display_menu(context):
    global language,code_multi,page,volume,WIDTH,HEIGHT,background,FONT_BUTTON
    screen = context.screen
    

    click_cooldown = 0
    asked_network = False
    
    share_context_multi(context)

    while not network_ready.is_set():
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()

        FONT_TITLE = pygame.font.Font("assets/fonts/Darksoul.otf", HEIGHT//10)
        FONT_BUTTON = pygame.font.SysFont("arial", HEIGHT//20)

        dt = context.clock.tick(60)
        if click_cooldown > 0:
            click_cooldown -= dt

        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        T = TEXT[language]

        if context.game_code == "wrong_code":
            page = "join_wrong_code"
            code_multi = ""
            context.edit_game_code("")

        if page == "menu":
            title = FONT_TITLE.render(T["title"], True, WHITE)
            shadow = FONT_TITLE.render(T["title"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + max(2,HEIGHT//240), HEIGHT//6 + max(2,HEIGHT//240))))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT//6)))

            buttons = [
                Button(T["new"], 4*HEIGHT//9, "new",screen),
                Button(T["join"], 41*HEIGHT//72, "join",screen),
                Button(T["options"], 25*HEIGHT//36, "options",screen),
                Button(T["quit"], 59*HEIGHT//72, "quit",screen)
            ]

            for btn in buttons:
                btn.draw(screen, mouse_pos)
                if btn.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                    click_cooldown = COOLDOWN_TIME
                    pygame.time.delay(180)
                    if btn.action == "quit":
                        pygame.quit()
                        sys.exit()
                    else:
                        page = btn.action
                        code_multi = ""
        elif page == "new":
            title = FONT_TITLE.render(T["title"], True, WHITE)
            shadow = FONT_TITLE.render(T["title"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + max(2,HEIGHT//240), HEIGHT//6 + max(2,HEIGHT//240))))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT//6)))

            info = FONT_BUTTON.render(T["show_code"], True, LIGHT_GREY)
            screen.blit(info, info.get_rect(center=(WIDTH // 2, 13*HEIGHT//36)))

            # Affichage du champ de texte
            input_rect = pygame.Rect(WIDTH // 2 - (11*WIDTH//64), 5*HEIGHT//12, 11*WIDTH//32, 13*HEIGHT//144)
            pygame.draw.rect(screen, BUTTON_BG, input_rect, border_radius=HEIGHT//60)
            pygame.draw.rect(screen, WHITE, input_rect, 2, border_radius=HEIGHT//60)

            # Affichage contenu champ de texte
            txt = FONT_BUTTON.render(context.game_code, True, DARK_GREY)
            screen.blit(txt, (input_rect.x + HEIGHT//48, input_rect.y + HEIGHT//48))

            # Demande de creation du code de partie
            if not asked_network:
                context.set_host()
                asked_network = True
                start_network(context.is_host)

        elif page in ("join","join_wrong_code"):
            title = FONT_TITLE.render(T["title"], True, WHITE)
            shadow = FONT_TITLE.render(T["title"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + max(2,HEIGHT//240), HEIGHT//6 + max(2,HEIGHT//240))))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT//6)))

            if page == "join":
                info = FONT_BUTTON.render(T["enter_code"], True, LIGHT_GREY)
            else:
                info = FONT_BUTTON.render(T["wrong_code"], True, LIGHT_GREY)
            screen.blit(info, info.get_rect(center=(WIDTH // 2, 13*HEIGHT//36)))

            # Affichage du champ de texte
            input_rect = pygame.Rect(WIDTH // 2 - (11*WIDTH//64), 5*HEIGHT//12, 11*WIDTH//32, 13*HEIGHT//144)
            pygame.draw.rect(screen, BUTTON_BG, input_rect, border_radius=HEIGHT//60)
            pygame.draw.rect(screen, WHITE, input_rect, 2, border_radius=HEIGHT//60)

            # Affichage contenu champ de texte
            txt = FONT_BUTTON.render(code_multi, True, DARK_GREY)
            screen.blit(txt, (input_rect.x + HEIGHT//48, input_rect.y + HEIGHT//48))

            continue_btn = Button(T["continue"], 7*HEIGHT//12, "continue",screen)
            continue_btn.draw(screen, mouse_pos)
            if continue_btn.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page = "loading"
                # envoi du code de partie :
                if not asked_network:
                    asked_network = True
                    context.set_client()
                    context.edit_game_code(code_multi.upper())
                    start_network(context.is_host)
                else:
                    context.edit_game_code(code_multi.upper())

            back = Button(T["back"], 5*HEIGHT//6, "menu",screen)
            back.draw(screen, mouse_pos)
            if back.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page = "menu"

        elif page == "loading":
            title = FONT_TITLE.render(T["loading"], True, WHITE)
            shadow = FONT_TITLE.render(T["loading"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + max(2,HEIGHT//240), HEIGHT//6 + max(2,HEIGHT//240))))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT//6)))

            back = Button(T["back"], 5*HEIGHT//6, "menu",screen)
            back.draw(screen, mouse_pos)
            if back.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page = "menu"
                code_multi = ""

        elif page == "options":
            title = FONT_TITLE.render(T["title"], True, WHITE)
            shadow = FONT_TITLE.render(T["title"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + max(2,HEIGHT//240), HEIGHT//6 + max(2,HEIGHT//240))))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT//6)))

            lang_txt = FONT_BUTTON.render(f"{T['language']} : {language}", True, LIGHT_GREY)
            screen.blit(lang_txt, lang_txt.get_rect(center=(WIDTH // 2, 7*HEIGHT//18)))

            lang_btn = Button(T["change_language"], 35*HEIGHT//72, "lang",screen)
            lang_btn.draw(screen, mouse_pos)
            if lang_btn.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                language = "EN" if language == "FR" else "FR"

            vol_txt = FONT_BUTTON.render(f"{T['volume']} : {int(volume*100)}%", True, LIGHT_GREY)
            screen.blit(vol_txt, vol_txt.get_rect(center=(WIDTH // 2, 7*HEIGHT//12)))

            bar_x, bar_y, bar_w = 25*WIDTH//64, 5*HEIGHT//8, 7*WIDTH//32
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, HEIGHT//120))
            pygame.draw.circle(screen, WHITE, (bar_x + int(volume * bar_w), bar_y + HEIGHT//240), 11*HEIGHT//720)

            if mouse_pressed[0]:
                mx, my = mouse_pos
                if bar_x <= mx <= bar_x + bar_w and bar_y - HEIGHT//60 <= my <= bar_y + HEIGHT//60:
                    volume = max(0, min(1, (mx - bar_x) / bar_w))
                    pygame.mixer.music.set_volume(volume)

            back = Button(T["back"], 5*HEIGHT//6, "menu",screen)
            back.draw(screen, mouse_pos)
            if back.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page = "menu"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and page in ("join","join_wrong_code"):
                if event.key == pygame.K_BACKSPACE:
                    code_multi = code_multi[:-1]
                elif len(code_multi) < 12 and event.unicode.isprintable():
                    code_multi += event.unicode

        pygame.display.flip()
