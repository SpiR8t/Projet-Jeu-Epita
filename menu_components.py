import pygame

WHITE = (255, 255, 255)
LIGHT_GREY = (210, 210, 210)
DARK_GREY = (90, 90, 90)
BLACK = (0, 0, 0)

BUTTON_BG = (255, 255, 255, 200)
BUTTON_HOVER = (120, 120, 120, 230)

pygame.font.init()

TEXT = {
    "FR": {
        "title": "Echoes of Lights",
        "new": "Nouvelle Partie",
        "join": "Rejoindre une Partie",
        "options": "Options",
        "quit": "Quitter",
        "show_code": "Le code de partie va s'afficher, partagez le avec l'autre joueur :",
        "enter_code": "Entrez le code multijoueur :",
        "wrong_code":"Veuillez entrer un code valide (5 lettre majuscules)",
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
        "show_code": "The game code will be displayed, share it to the other player :",
        "enter_code": "Enter game code:",
        "wrong_code":"Please enter a valid code (5 uppercase letters)",
        "language": "Language",
        "change_language": "Change language",
        "volume": "Music volume",
        "back": "Back",
        "continue": "Continue",
        "loading": "Loading..."
    }
}

class Button:
    def __init__(self, text, center_y, action,screen):
        self.text = text
        self.action = action
        # dimension écran
        self.s_width = screen.get_width()
        self.s_height = screen.get_height()
        # dimension bouton
        self.b_width = 21 * self.s_width // 64
        self.b_height = self.s_height // 9
        self.rect = pygame.Rect(0, 0, self.b_width, self.b_height)
        self.rect.center = (self.s_width // 2, center_y)
        self.font = pygame.font.SysFont("arial", self.s_height//20)

    def draw(self, win, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = BUTTON_HOVER if hovered else BUTTON_BG
        surface = pygame.Surface((self.b_width, self.b_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect(), border_radius=9*self.b_height//40)
        win.blit(surface, self.rect)
        shadow = self.font.render(self.text, True, BLACK)
        text = self.font.render(self.text, True, DARK_GREY)
        shadow_rect = shadow.get_rect(center=(self.rect.centerx + max(1,self.b_height//40), self.rect.centery + max(1,self.b_height//40)))
        text_rect = text.get_rect(center=self.rect.center)
        win.blit(shadow, shadow_rect)
        win.blit(text, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]
    
def display_title(context,h,text):
    FONT_TITLE = pygame.font.Font("assets/fonts/Darksoul.otf", context.screen.get_height()//10)
    title = FONT_TITLE.render(TEXT[context.language][text], True, WHITE)
    shadow = FONT_TITLE.render(TEXT[context.language][text], True, BLACK)
    context.screen.blit(shadow, shadow.get_rect(center=(context.screen.get_width() // 2 + max(2,context.screen.get_height()//240), h + max(2,context.screen.get_height()//240))))
    context.screen.blit(title, title.get_rect(center=(context.screen.get_width() // 2, h)))