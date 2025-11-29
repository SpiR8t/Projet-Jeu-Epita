import pygame


class Joueur:
    def __init__(self, x, y, vitesse, avatar_image):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.avatar = avatar_image
        # implémenter la taille de l'avatar pour les collisions ->
        # self.largeur =
        # self.hauteur =
        # self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

    def deplacer(self):
        """Écoute les touches et met à jour la position du joueur."""
        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            self.x -= self.vitesse
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            self.x += self.vitesse
        if touches[pygame.K_UP] or touches[pygame.K_z]:
            self.y -= self.vitesse
        if touches[pygame.K_DOWN] or touches[pygame.K_s]:
            self.y += self.vitesse

    # def update(self):
    #     """Met à jour le rect selon la position."""
    #     self.rect.topleft = (self.x, self.y)

    def get_pos(self):
        return (self.x, self.y)
