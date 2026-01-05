import pygame
import sys

WIDTH, HEIGHT = 1280, 720

background = pygame.image.load("assets/images/menu/menu_bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

volume = 0.5
pygame.mixer.init()
pygame.mixer.music.load("assets/audio/musics/menu_music.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

WHITE = (255, 255, 255)
LIGHT_GREY = (210, 210, 210)
DARK_GREY = (90, 90, 90)
BLACK = (0, 0, 0)

BUTTON_BG = (255, 255, 255, 200)
BUTTON_HOVER = (120, 120, 120, 230)

pygame.font.init()
FONT_TITLE = pygame.font.Font("assets/fonts/Darksoul.otf", 72)
FONT_BUTTON = pygame.font.SysFont("arial", 36)

TEXT = {
    "FR": {
        "title": "Echoes of Lights",
        "new": "Nouvelle Partie",
        "join": "Rejoindre une Partie",
        "options": "Options",
        "quit": "Quitter",
        "enter_code": "Entrez le code multijoueur :",
        "language": "Langue",
        "change_language": "Changer la langue",
        "volume": "Volume musique",
        "back": "Retour",
        "continue": "Continuer",
        "loading": "Chargement..."
    },
    "EN": {
        "title": "Echoes of Lights",
        "new": "New Game",
        "join": "Join a Game",
        "options": "Options",
        "quit": "Quit",
        "enter_code": "Enter multiplayer code:",
        "language": "Language",
        "change_language": "Change language",
        "volume": "Music volume",
        "back": "Back",
        "continue": "Continue",
        "loading": "Loading..."
    }
}

BUTTON_WIDTH = 420
BUTTON_HEIGHT = 80


COOLDOWN_TIME = 200  

class Button:
    def __init__(self, text, center_y, action):
        self.text = text
        self.action = action
        self.rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.rect.center = (WIDTH // 2, center_y)

    def draw(self, win, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = BUTTON_HOVER if hovered else BUTTON_BG
        surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=18)
        win.blit(surface, self.rect)
        shadow = FONT_BUTTON.render(self.text, True, BLACK)
        text = FONT_BUTTON.render(self.text, True, DARK_GREY)
        shadow_rect = shadow.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        text_rect = text.get_rect(center=self.rect.center)
        win.blit(shadow, shadow_rect)
        win.blit(text, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

page = "menu"
language = "FR"
code_multi = ""

def display_menu(context):
    global language,code_multi,page,volume
    screen = context.screen
    click_cooldown = 0

    page_next = ""
    while context.game_code == "" or page_next != "":
        if page_next != "":
            page = page_next
            page_next = ""
        dt = context.clock.tick(60)
        if click_cooldown > 0:
            click_cooldown -= dt

        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        T = TEXT[language]

        if page == "menu":
            title = FONT_TITLE.render(T["title"], True, WHITE)
            shadow = FONT_TITLE.render(T["title"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + 3, 123)))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

            buttons = [
                Button(T["new"], 320, "new"),
                Button(T["join"], 410, "join"),
                Button(T["options"], 500, "options"),
                Button(T["quit"], 590, "quit")
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

        elif page in ("new", "join"):
            title = FONT_TITLE.render(T["title"], True, WHITE)
            shadow = FONT_TITLE.render(T["title"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + 3, 123)))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

            info = FONT_BUTTON.render(T["enter_code"], True, LIGHT_GREY)
            screen.blit(info, info.get_rect(center=(WIDTH // 2, 260)))

            # Affichage du champ de texte
            input_rect = pygame.Rect(WIDTH // 2 - 220, 300, 440, 65)
            pygame.draw.rect(screen, BUTTON_BG, input_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, input_rect, 2, border_radius=12)

            # Affichage contenu champ de texte
            txt = FONT_BUTTON.render(code_multi, True, DARK_GREY)
            screen.blit(txt, (input_rect.x + 15, input_rect.y + 15))

            continue_btn = Button(T["continue"], 420, "continue")
            continue_btn.draw(screen, mouse_pos)
            if continue_btn.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page_next = "loading"
                # envoi du code de partie :
                context.is_host = False
                context.game_code = code_multi.upper()

            back = Button(T["back"], 600, "menu")
            back.draw(screen, mouse_pos)
            if back.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page = "menu"

        elif page == "loading":
            title = FONT_TITLE.render(T["loading"], True, WHITE)
            shadow = FONT_TITLE.render(T["loading"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + 3, 123)))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

            back = Button(T["back"], 600, "menu")
            back.draw(screen, mouse_pos)
            if back.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page = "menu"
                code_multi = ""

        elif page == "options":
            title = FONT_TITLE.render(T["options"], True, WHITE)
            shadow = FONT_TITLE.render(T["options"], True, BLACK)
            screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + 3, 123)))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

            lang_txt = FONT_BUTTON.render(f"{T['language']} : {language}", True, LIGHT_GREY)
            screen.blit(lang_txt, lang_txt.get_rect(center=(WIDTH // 2, 280)))

            lang_btn = Button(T["change_language"], 350, "lang")
            lang_btn.draw(screen, mouse_pos)
            if lang_btn.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                language = "EN" if language == "FR" else "FR"

            vol_txt = FONT_BUTTON.render(f"{T['volume']} : {int(volume*100)}%", True, LIGHT_GREY)
            screen.blit(vol_txt, vol_txt.get_rect(center=(WIDTH // 2, 420)))

            bar_x, bar_y, bar_w = 500, 450, 280
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, 6))
            pygame.draw.circle(screen, WHITE, (bar_x + int(volume * bar_w), bar_y + 3), 11)

            if mouse_pressed[0]:
                mx, my = mouse_pos
                if bar_x <= mx <= bar_x + bar_w and bar_y - 12 <= my <= bar_y + 12:
                    volume = max(0, min(1, (mx - bar_x) / bar_w))
                    pygame.mixer.music.set_volume(volume)

            back = Button(T["back"], 600, "menu")
            back.draw(screen, mouse_pos)
            if back.is_clicked(mouse_pos, mouse_pressed) and click_cooldown <= 0:
                click_cooldown = COOLDOWN_TIME
                pygame.time.delay(180)
                page = "menu"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and page in ("new", "join"):
                if event.key == pygame.K_BACKSPACE:
                    code_multi = code_multi[:-1]
                elif len(code_multi) < 12 and event.unicode.isprintable():
                    code_multi += event.unicode

        pygame.display.flip()
