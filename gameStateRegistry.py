# Dans ce fichier on retrouve la classe GameStateRegistry correspondante au registre qui va stocker l'Etat du jeu

class GameStateRegistry:
    """
    Centralise l'intégralité de l'état du monde pour les interactions.
    
    Cette classe sera complétée plus tard pour :
        - Les systèmes d'énigmes avancées
        - La gestion complète des ennemis (IA, vagues, boss, etc.)
    """

    def __init__(self):

        self.levers = {}               # Dictionnaire de listes de leviers (énigmes)

        self.enemies = []                # Tous les ennemis actifs

        self.doors = []                  # Portes interactives

        self.global_flags = {}           # Flags globaux (ex: {"artefact 1": True})


    # ==========================
    # LEVIERS
    # ==========================

    def add_lever(self, lever):
        """
        Ajoute un levier dans le dictionnaire des leviers,
        classé par group_id.
        """

        group_id = lever.group

        if group_id not in self.levers:
            self.levers[group_id] = []

        lever.id = len(self.levers[group_id]) # rajoute l'id dans l'instance (None avant)
        self.levers[group_id].append(lever)


    def is_group_active(self, group_id): #vérifier si un groupe est actif
        if group_id not in self.levers:
            return False
        
        return all(lever.state for lever in self.levers[group_id])


    # ==========================
    # FLAGS
    # ==========================

    def set_flag(self, key, value=True):
        self.global_flags[key] = value

    def get_flag(self, key):
        return self.global_flags.get(key, False)
    
    def json_save():
        pass
        # pour sauvegarder plus tard on pourra se servir du registre avec un gros json


# création du registre pour l'importer partout
gameRegistry = GameStateRegistry()
print(gameRegistry.levers)