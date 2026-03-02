# dans ce fichier on retrouve les classes qui servent à définir les objets 
# affiché notamment pour les énigmes

class Lever:
    def __init__(self, lever_id, group=None, initial_state=False):
        self.id = lever_id                  # Identifiant unique
        self.group = group                  # Groupe logique (optionnel)
        self.state = initial_state          # True = activé, False = désactivé
        self.links = []                     # Leviers liés
        self.locked = False                 # Empêche interaction si True

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