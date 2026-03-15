# dans ce fichier on retrouve les classes qui servent à définir les objets 
# affiché notamment pour les énigmes

import actions

class Lever:
    def __init__(self, x, y, group, lever_id=None, initial_state=True):
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

    def update_matrix(self, map):
        if self.state == True:
            map.tiles[self.position[0]][self.position[1]][2] = 10
        else:
            map.tiles[self.position[0]][self.position[1]][2] = 11


    def toggle(self, map, initial=True):
        """Inverse l'état du levier."""
        if self.locked:
            return
        
        self.state = not self.state
        self.on_toggle(map, initial)

    # -------------------------
    # Logique de propagation
    # -------------------------

    def propagate(self,map):
        """Applique l'état aux leviers liés."""
        for lever in self.links:
            lever.toggle(map, False)

    # -------------------------
    # Événement déclenché
    # -------------------------

    def on_toggle(self, map, initial):
        print(f"Lever {self.id} -> {'ON' if self.state else 'OFF'}")
        if initial:
            self.propagate(map)
        self.update_matrix(map)

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
        # 20 = NE, 21 = SW, 22 = NW, 23 = SE  en étant fermée
        # 24 = NE, 25 = SW, 26 = NW, 27 = SE  en étant ouverte
        # C'est une liste de 2 valeurs : la première correspond à l'orientation quand la porte est fermée et la 2e quand elle est ouverte
        self.position = (x,y)             #coordonnées dans la matrice de la map
        self.id = door_id                  # Identifiant unique
        self.group = group 

    def open_close(self):
        """
        Cette méthode inverse l'état de la porte, l'ouvre ou la ferme et renvoie l'action pour modifier la map pour le faire
        """
        self.state = not self.state
        # Générer un action qui permet de faire passer la porte de son 
        # apparence d'ouverture à son apparence de fermeture en modifiant la matrice de la map
        if self.state:
            tile_nb = self.orientation[1]
        else:
            tile_nb = self.orientation[0]
        action = actions.EditMapAction(
            self.position[0],
            self.position[1],
            1,tile_nb,tile_nb
        )
        return action
