# Dans ce fichier on retrouve la classe GameStateRegistry correspondante au registre qui va stocker l'Etat du jeu
import random # pour les énigmes


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

        self.doors = {}                  # Portes interactives

        self.global_flags = {}           # Flags globaux (ex: {"artefact 1": True})

    def setup(self, map):
        """ La fonction qui va mettre tous l'environnement interactif en place: les leviers mélangés pas exemple"""
        
        # génération des énigmes des leviers
        for lever_group_id in self.levers:
            self.generate_random_links(lever_group_id)
            self.scramble_levers(lever_group_id, map)

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
    
    def generate_random_links(self, group_id, seed=12345): # la version difficulté easy pour l'instant
        """Génère un lien par levier à """
        rng = random.Random(seed) # pour l'instant on va garder la meme seed pour les deux joueurs en hardcode

        shuffled = self.levers[group_id][:]
        rng.shuffle(shuffled)

        for i in range(len(shuffled)-1):
            a = shuffled[i]
            b = shuffled[i+1]
            a.add_link(b)
        
        # pour le dernier levier qui est seul on le chaine avec celui du début
        last = shuffled[len(shuffled)-1]
        last.add_link(shuffled[0]) # étant donné que la liste n'est pas censée être vide

        #possibilité d'augmenter la complexité des lien plus tard

    def scramble_levers(self, group_id, map, moves=30, seed=12345):
        """ Actionne des leviers au hasard pour setup les énigmes des leviers """

        rng = random.Random(seed)

        for _ in range(moves):
            lever = rng.choice(self.levers[group_id])
            lever.toggle(map)

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

    # ==========================
    # DOORS
    # ==========================

    def add_door(self,door):
        """
        Ajoute une porte dans le dictionnaire des portes,
        classé par group_id.
        """
        group_id = door.group

        if group_id not in self.doors:
            self.doors[group_id] = []

        door.id = len(self.doors[group_id]) # rajoute l'id dans l'instance (None avant)
        self.doors[group_id].append(door)


# création du registre pour l'importer partout
gameRegistry = GameStateRegistry()