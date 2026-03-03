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


    def attack(self, player): # chaque ennemi aura sa fonction attack()
        pass


    def chase(self, player): # déplacement de l'ennemi
        # vecteurs directeurs vx et vy
        dx = player.x - self.x
        dy = player.y - self.y

        if dx == 0 and dy == 0:
            vx, vy = 0, 0
        else:
            distance = math.sqrt(dx**2 + dy**2)
            vx = dx * self.speed / distance
            vy = dy * self.speed / distance

        #déplacement de l'ennemi
        self.x += vx
        self.y += vy

        #déplacement de la hitbox
        self.hitbox.move_ip(vx, vy)



    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2) #distance entre le joueur et l'ennemi

        #mise à jour de l'état de l'IA de l'ennemi
        if distance <= self.attack_range:
            self.AI_state = "ATTACK"
        elif distance <= self.detection_range:
            self.AI_state = "CHASE"
        else:
            self.AI_state = "IDLE"

        #action de l'ennemi en fonction de son état
        if self.AI_state == "ATTACK":
            print("fonction qui attaque le joueur") #self.attack(player) : à dev !!
        elif self.AI_state == "CHASE":
            print("fonction qui déplace l'ennemi vers le joueur") #self.chase(player) : à dev !!





        

        

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
            detection_range = 200,
            attack_range = 50,
            AI_state = "IDLE",
            level = level
        )
        self.hitbox = pygame.Rect(x-20, y-20, 40, 40)
        self.weapon = "KNIFE"

    #attaque du slasher (couteau)   
    def attack(self, player):
        if self.weapon == "KNIFE":
            # ajouter animation ici
            # ajouter création zone d'attaque (Rect)
            pass
