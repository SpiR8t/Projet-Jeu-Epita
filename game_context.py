"""Ce fichier contient une classe GameContext qui permet d'enregistrer les infos de la fenêtre 
pygame et de les partager avec tous les fichiers qui en ont besoin, sans nécessairement importer
la lib pygame. Il contient en fait toutes les infos qui doivent être partagé entre les fichiers """

class GameContext:
    def __init__(self, screen, clock, playerH, playerC,map,cam,multi):
        # Fenetre pygame
        self.screen = screen
        self.clock = clock

        # Joueurs
        self.host_player = playerH
        self.client_player = playerC

        # Jeu
        self.game_code = ""
        self.is_host = True
        self.multiplayer = multi
        self.language = "FR"
        self.running = False
        self.pause = False
        self.map = map
        self.camera = cam
        self.mouse_pressed = False #cooldown général pour les cliques
        self.mouse_pressed_last = False

        self.quitting = False # ferme le jeu

    def edit_game_code(self,newcode):
        self.game_code=newcode

    def set_host(self):
        self.is_host = True

    def set_client(self):
        self.is_host = False

    def pause_switch(self):
        self.pause = not self.pause

    def reset(self):
        "Méthode pour reset tou le contexte pour relancer une partie"
        self.game_code = ""
        self.is_host = True
        self.running = False
        self.pause = False