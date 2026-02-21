import pygame


class Joueur:
    def __init__(self, x, y, vitesse, avatar_image, is_host):
        self.x_origine = x
        self.y_origine = y
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.avatar = avatar_image
        self.host = is_host
        # implémenter la taille de l'avatar pour les collisions ->
        # self.largeur =
        # self.hauteur =
        # self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

    # def update(self):
    #     """Met à jour le rect selon la position."""
    #     self.rect.topleft = (self.x, self.y)

    def get_pos(self):
        return (self.x, self.y)
    
    def reset(self):
        self.x = self.x_origine
        self.y = self.y_origine
