# Dans ce fichier on retrouve la classe GameStateRegistry correspondante au registre qui va stocker l'Etat du jeu

class GameStateRegistry:
    """
    Centralise l'intégralité de l'état du monde pour les interactions.
    
    Cette classe sera complétée plus tard pour :
        - Les systèmes d'énigmes avancées
        - La gestion complète des ennemis (IA, vagues, boss, etc.)
    """

    def __init__(self):

        self.levers = []                # Liste de listes de leviers (énigmes)

        self.enemies = []                # Tous les ennemis actifs

        self.doors = []                  # Portes interactives

        self.global_flags = {}           # Flags globaux (ex: {"artefact 1": True})


    # ==========================
    # LEVIERS
    # ==========================

    def add_lever(self, lever):
        self.levers.append(lever)

    def create_puzzle(self, lever_list):
        """Ajoute une nouvelle énigme (liste de leviers)."""
        self.puzzles.append(lever_list)

    def is_puzzle_solved(self, puzzle_index):
        """Vérifie si tous les leviers d'une énigme sont activés."""
        puzzle = self.puzzles[puzzle_index]
        return all(lever.state for lever in puzzle)


    # ==========================
    # FLAGS
    # ==========================

    def set_flag(self, key, value=True):
        self.global_flags[key] = value

    def get_flag(self, key):
        return self.global_flags.get(key, False)