"""Ce fichier contient une classe GameContext qui permet d'enregistrer les infos de la fenêtre 
pygame et de les partager avec tous les fichiers qui en ont besoin, sans nécessairement importer
la lib pygame. Il contient en fait toutes les infos qui doivent être partagé entre les fichiers """

class GameContext:
    def __init__(self, screen, clock, playerH, playerC,map,cam):
        # Fenetre pygame
        self.screen = screen
        self.clock = clock

        # Joueurs
        self.host_player = playerH
        self.client_player = playerC

        # Animations et compétences
        self.animations = []
        self.action = []
        # Pour envoyer au multi
        self.action_created = False
        self.action_name_to_send = []

        # Ennemis
        self.ennemies = [] # contient les objets ennemies


        self.info_action = {} # pour l'instant ça contient les infos des levier
                              # mais on pourra rajouter bien d'autres choses

        # Parametres dev
        self.multiplayer = True
        self.hud = True

        # Jeu
        self.game_code = ""
        self.is_host = True
        self.language = "FR"
        self.running = False
        self.pause = False
        self.map = map
        self.camera = cam
        self.mouse_pressed = False #cooldown général pour les cliques
        self.mouse_pressed_last = False

        self.quitting = False # ferme le jeu

    def set_dev_params(self,multi,hud):
        """Méthode pour définir les paramètres servant au dev"""
        self.multiplayer = multi
        self.hud = hud

    def edit_game_code(self,newcode):
        self.game_code=newcode

    def set_host(self):
        self.is_host = True

    def set_client(self):
        self.is_host = False

    def pause_switch(self):
        self.pause = not self.pause

    def reset(self):
        "Méthode pour reset tout le contexte pour relancer une partie"
        self.game_code = ""
        self.is_host = True
        self.running = False
        self.pause = False

    # animation et compétence / actions

    def add_action(self, action):
        self.action.append(action)

    def execute_actions(self, gameRegister):
        for action in self.action:
            if action.name == "Lever Action":
                action.execute(self, gameRegister, self.map)
            elif action.name == "Interact Action":
                action.execute(self, gameRegister)
            else:
                action.execute(self)
        self.action = []

    def update_animations(self):
        for anim in self.animations:
            anim.update()
        
        self.animations = [a for a in self.animations if not a.finished]
    
    def draw_animations(self):
        for anim in self.animations:
            anim.draw(self.screen, self.camera)

    # actions interaction / c'est pour ajouter les infos nécessaire à l'envoi de l'action à l'autre joueur
    def add_info_lever_action(self, lever_group, lever_id):
        self.info_action["Lever Toggle"] = [lever_group, lever_id]

    def add_info_interact_action(self, coords):
        self.info_action["Interact coords"] = coords

    def add_info_edit_map_action(self, x, y, tile_nb0, tile_nb1, tile_nb2):
        self.info_action[f"Edit Map ({x},{y})"] = [x, y, tile_nb0, tile_nb1, tile_nb2]
    