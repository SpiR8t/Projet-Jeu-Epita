"""Ce fichier contient une classe GameContext qui permet d'enregistrer les infos de la fenêtre 
pygame et de les partager avec tous les fichiers qui en ont besoin, sans nécessairement importer
la lib pygame. Il contient en fait toutes les infos qui doivent être partagé entre les fichiers """

class GameContext:
    def __init__(self, screen, clock, playerH, playerC, W, H,map,cam,multi):
        # Fenetre pygame
        self.screen = screen
        self.clock = clock
        self.width = W
        self.height = H

        # Joueurs
        self.host_player = playerH
        self.client_player = playerC

        # Jeu
        self.game_code = ""
        self.is_host = True
        self.multiplayer = multi
        self.running = True
        self.map = map
        self.camera = cam
