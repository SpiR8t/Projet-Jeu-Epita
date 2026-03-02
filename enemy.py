import pygame
import math
from player import Entity

'''
On crée une classe globale Enemy, elle-même une sous-classe de Entity (dans player.py).
Cette classe regroupe toutes les fonctions et méthodes liées à un ennemi.
—> De cette manière on peut créer une classe par ennemi et leur associer des caractéristiques propres facilement.
'''
class Enemy(Entity):
    def __init__(self, x, y, max_hp, speed, damage, attack_cooldown, detection_range, attack_range, AI_state="IDLE", level=1):
        super().__init__(x, y, max_hp, speed)
        self.damage = damage
        self.attack_cooldown = attack_cooldown #nombre de frames entre chaque attaque d'un ennemi (pour la vitesse d'attaque)
        self.detection_range = detection_range #zone de détection du joueur
        self.attack_range = attack_range #portée de l'attaque (à cette distance l'ennemi s'arrête et attaque le joueur)
        self.AI_state = AI_state #à l'apparition l'IA est en mode "inactif"
        self.level = level


# PREMIER ENNEMI : le Slasher

class Slasher(Enemy):
    def __init__(self, x, y, level=1): # niveaux possibles : 1, 2 ou 3
        super().__init__(
            x = x,
            y = y,
            #remplacer les valeurs actuelles par des valeurs plus cohérentes lors des tests !!!
            max_hp = 50 + (50*level),
            speed = 5 * level, 
            damage = 5 * level,
            attack_cooldown = 60,
            detection_range = 50,
            attack_range = 5,
            AI_state = "IDLE",
            level = level
        )
        self.weapon = "KNIFE"
        


