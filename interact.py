# dans ce fichier on retrouve les classes qui servent à définir les objets 
# affiché notamment pour les énigmes

class Lever:
    def __init__(self, x, y, group, lever_id=None, initial_state=False):
        self.id = lever_id                  # Identifiant unique
        self.group = group                  # Groupe logique (optionnel)
        self.state = initial_state          # True = activé, False = désactivé
        self.links = []                     # Leviers liés
        self.locked = False                 # Empêche interaction si True
        self.position = (x,y)

    # -------------------------
    # Gestion des liens
    # -------------------------

    def add_link(self, other_lever):
        """Lie un autre levier à celui-ci."""
        if other_lever not in self.links:
            self.links.append(other_lever)

    def remove_link(self, other_lever):
        """Supprime un lien."""
        if other_lever in self.links:
            self.links.remove(other_lever)

    # -------------------------
    # Interaction
    # -------------------------

    def toggle(self):
        """Inverse l'état du levier."""
        if self.locked:
            return
        
        self.state = not self.state
        self.on_toggle()

    # -------------------------
    # Logique de propagation
    # -------------------------

    def propagate(self):
        """Applique l'état aux leviers liés."""
        for lever in self.links:
            lever.toggle()

    # -------------------------
    # Événement déclenché
    # -------------------------

    def on_toggle(self):
        """
        Méthode appelée à chaque changement d'état.
        Tu peux la modifier selon ton gameplay.
        """
        print(f"Lever {self.id} -> {'ON' if self.state else 'OFF'}")
        self.propagate()

    # -------------------------
    # Utilitaires
    # -------------------------

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def is_active(self):
        return self.state

    def __repr__(self):
        return f"<Lever id={self.id} state={self.state} group={self.group}>"
    

class Door:
    def __init__(self, x, y, orientation, group, door_id=None, initial_state = False,):
        self.state = initial_state        # True = ouverte, False = Fermée
        self.orientation = orientation   
        # 20 = NE, 21 = SW, 22 = NW, 23 = SE
        # C'est une liste de 2 valeurs : la première correspond à l'orientation quand la porte est ouverte et la 2e quand elle est fermée
        self.position = (x,y)
        self.id = door_id                  # Identifiant unique
        self.group = group 

    def open_door(self):
        if not self.state:
            self.state = True
            # Générer un action qui permet de faire passer la porte de son 
            # apparence d'ouverture à son apparence de fermeture en modifiant la matrice de la map