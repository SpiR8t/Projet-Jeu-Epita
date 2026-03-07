import pygame
import math
from player import Entity
from actions import SlasherAttack
from game_context import GameContext

'''
On crée une classe globale Enemy, elle-même une sous-classe de Entity (dans player.py).
Cette classe regroupe toutes les fonctions et méthodes liées à un ennemi.
—> De cette manière on peut créer une classe par ennemi et leur associer des caractéristiques propres facilement.
'''
class Enemy(Entity):
    #les coordonnées x et y correspondent à la position du coin supérieur gauche de l'ennemi (important pour les hitbox)
    def __init__(self, x, y, max_hp, speed, damage, attack_cooldown, detection_range, attack_range, AI_state="IDLE", level=1):
        super().__init__(x, y, max_hp, speed)
        self.damage = damage
        self.attack_cooldown = attack_cooldown #nombre de frames entre chaque attaque d'un ennemi (pour la vitesse d'attaque)
        self.detection_range = detection_range #zone de détection du joueur
        self.attack_range = attack_range #portée de l'attaque (à cette distance l'ennemi s'arrête et attaque le joueur)
        self.current_attack_cooldown = attack_cooldown
        self.AI_state = AI_state # à l'apparition l'IA est en mode "inactif"
        self.level = level
        # offsets pour centrer les hitbox
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 0

        self.facing = "N" # directions possibles : N S E O NE NO SE SO
        self.direction = (0,1) #pas utilisé mais évite les problèmes de définition
        self.damage_zone = None #zone créée par un ennemi (ex : Slasher) infligeant des dégâts au joueur.
        #NB : on associe damage_zone directement à la classe pour la récupérer dans game_logic et ainsi pouvoir debug les combats plus facilement


    def update_facing(self, vx, vy):
        #on peut aussi utiliser cette fonction pour changer la direction des images des ennemis sur la map

        seuil = 0.1 # seuil de sensibilité pour le changement de direction (MODIFIABLE)

        if abs(vx) < seuil and abs(vy) < seuil: #déplacements négligeables
            return
        
        #calcul de l'angle de direction en degrés
        angle = math.atan2(vy, vx) * 180 / math.pi
        angle = (angle + 360) % 360 #cas d'angles négatifs

        if (angle >= 0 and angle < 22.5) or (angle <= 360 and angle >= 337.5):
            self.facing = "E"
        elif angle >= 22.5 and angle < 67.5:
            self.facing = "SE"
        elif angle >= 67.5 and angle < 112.5:
            self.facing = "S"
        elif angle >= 112.5 and angle < 157.5:
            self.facing = "SO"
        elif angle >= 157.5 and angle < 202.5:
            self.facing = "O"
        elif angle >= 202.5 and angle < 247.5:
            self.facing = "NO"
        elif angle >= 247.5 and angle < 292.5:
            self.facing = "N"
        else:
            self.facing = "NE"


    def attack(self, player): # chaque ennemi aura sa fonction attack()
        pass


    def chase(self, player): # déplacement de l'ennemi
        # vecteurs directeurs vx et vy
        #on prend le centre de la hitbox du joueur comme cible
        dx = player.hitbox.centerx - self.hitbox.centerx
        dy = player.hitbox.centery - self.hitbox.centery

        if dx == 0 and dy == 0:
            vx, vy = 0, 0
        else:
            distance = math.sqrt(dx**2 + dy**2)
            vx = dx * self.speed / distance
            vy = dy * self.speed / distance

        #mise à jour de la direction
        self.update_facing(vx, vy)

        #déplacement de l'ennemi
        if distance > self.attack_range + 10 and distance <= self.detection_range: #pour éviter que l'ennemi se rapproche trop du joueur
            self.x += vx
            self.y += vy

        #déplacement de la hitbox
        self.hitbox.x, self.hitbox.y = int(self.x + self.hitbox_offset_x), int(self.y + self.hitbox_offset_y)


    def update(self, player):
        dx = player.hitbox.centerx - self.hitbox.centerx
        dy = player.hitbox.centery - self.hitbox.centery
        distance = math.sqrt(dx**2 + dy**2) #distance entre le joueur et l'ennemi

        #mise à jour de l'état de l'IA de l'ennemi
        if distance <= self.attack_range + 10:
            self.AI_state = "ATTACK"
        elif distance <= self.detection_range:
            self.AI_state = "CHASE"
        else:
            self.AI_state = "IDLE"

        # update du cooldown
        if self.current_attack_cooldown > 0:
            self.current_attack_cooldown -= 1

        #action de l'ennemi en fonction de son état
        action = None
        if self.AI_state == "ATTACK":
            action = self.attack(player)
        elif self.AI_state == "CHASE":
            self.chase(player)

        return action



# PREMIER ENNEMI : le Slasher

class Slasher(Enemy):
    def __init__(self, x, y, level=1): # niveaux possibles : 1, 2 ou 3
        super().__init__(
            x = x,
            y = y,
            #remplacer les valeurs actuelles par des valeurs plus cohérentes lors des tests !!!
            max_hp = 50 + (50*level),
            speed = 1 * level, #à remodifier probablement
            damage = 5 * level,
            attack_cooldown = 60,
            detection_range = 300,
            attack_range = 25,
            AI_state = "IDLE",
            level = level
        )
        self.hitbox = pygame.Rect(x, y, 20, 20) #taille de la hitbox à adapter au pixel art (NB : il faut aussi réadapter les zones d'attaque en conséquence)
        #POUR TEST : offsets pour centrer la hitbox du Slasher
        self.hitbox_offset_x = 5
        self.hitbox_offset_y = -60

    #attaque du slasher (couteau)   
    '''
    Pour attaquer le joueur, le Slasher crée une zone d'atteinte rectangulaire.
    La zone est créée en fonction de l'orientation du Slasher (pour que l'attaque se fasse dans la bonne direction)
    D'AILLEURS : on pourrait créer un type d'ennemi qui met des dégâts tout autour de lui (style Jackie dans Brawl Stars)
    Le joueur prend des dégâts seulement si sa hitbox touche la zone d'atteinte.
    '''
    def attack(self, player):
        self.damage_zone = None #MISE A JOUR DE LA DAMAGE ZONE (pas indispensable mais plus propre)
        if self.current_attack_cooldown <= 0:
            # ajouter animation ici aussi
            if self.facing == "E":
               self.damage_zone = pygame.Rect(self.hitbox.x+20, self.hitbox.y-5, self.attack_range, 30)
            elif self.facing == "SE":
                self.damage_zone = pygame.Rect(self.hitbox.x+5, self.hitbox.y+5, 10+self.attack_range, 10+self.attack_range)
            elif self.facing == "S":
                self.damage_zone = pygame.Rect(self.hitbox.x-5, self.hitbox.y+20, 30, self.attack_range)
            elif self.facing == "SO":
                self.damage_zone = pygame.Rect(self.hitbox.x-self.attack_range, self.hitbox.y+5, 10+self.attack_range, 10+self.attack_range)
            elif self.facing == "O":
                self.damage_zone = pygame.Rect(self.hitbox.x-self.attack_range, self.hitbox.y-5, self.attack_range, 30)
            elif self.facing == "NO":
                self.damage_zone = pygame.Rect(self.hitbox.x-self.attack_range+5, self.hitbox.y-self.attack_range+5, 10+self.attack_range, 10+self.attack_range)
            elif self.facing == "N":
                self.damage_zone = pygame.Rect(self.hitbox.x-5,self.hitbox.y-self.attack_range, 30, self.attack_range)
            else: #NE
                self.damage_zone = pygame.Rect(self.hitbox.x+10, self.hitbox.y-self.attack_range+5, 10+self.attack_range, 10+self.attack_range)
        
            if self.damage_zone.colliderect(player.hitbox): #player dans la zone
                print("Damage dealt from Slasher") #peut-être à retirer mais utile pour debug
                player.take_damage(self.damage)
            
            self.current_attack_cooldown = self.attack_cooldown #remise à l'état initial du cooldown

            self.chase(player) #mise à jour de la direction de l'attaque au cas où le joueur aurait bougé

            return SlasherAttack(self, self.attack_range) #on retourne l'action pour le réseau
        return None #si cooldown pas terminé


'''
ici prochainement : la classe Flinger, un ennemi qui tire de loin
'''


            
