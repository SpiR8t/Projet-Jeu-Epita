"""Ce fichier contient une classe GameContext qui permet d'enregistrer les infos de la fenêtre 
pygame et de les partager avec tous les fichiers qui en ont besoin, sans nécessairement importer
la lib pygame. Il contient en fait toutes les infos qui doivent être partagé entre les fichiers """

class GameContext:
    def __init__(self, screen, clock, playerH, playerC, W, H,map,cam):
        self.screen = screen
        self.clock = clock
        self.host_player = playerH
        self.client_player = playerC
        self.running = True
        self.width = W
        self.height = H
        self.map = map
        self.camera = cam
