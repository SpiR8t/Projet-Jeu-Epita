import pygame
import math
from player import Entity

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
        self.AI_state = AI_state #à l'apparition l'IA est en mode "inactif"
        self.level = level

        self.facing = "N" # directions possibles : N S E O NE NO SE SO


    def update_facing(self, vx, vy):
        #on peut aussi utiliser cette fonction pour changer la direction des images des ennemis sur la map

        seuil = 20 # seuil de sensibilité pour le changement de direction (MODIFIABLE)

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
        self.hitbox.x, self.hitbox.y = int(self.x), int(self.y)

        self.update_facing(vx, vy)


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

        # update du cooldown
        if self.current_attack_cooldown > 0:
            self.current_attack_cooldown -= 1

        #action de l'ennemi en fonction de son état
        if self.AI_state == "ATTACK":
            self.attack(player)
        elif self.AI_state == "CHASE":
            self.chase(player)



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
        self.hitbox = pygame.Rect(x, y, 40, 40)

    #attaque du slasher (couteau)   
    '''
    Pour attaquer le joueur, le Slasher crée une zone d'atteinte rectangulaire.
    La zone est créée en fonction de l'orientation du Slasher (pour que l'attaque se fasse dans la bonne direction)
    D'AILLEURS : on pourrait créer un type d'ennemi qui met des dégâts tout autour de lui (style Jackie dans Brawl Stars)
    Le joueur prend des dégâts seulement si sa hitbox touche la zone d'atteinte.
    '''
    def attack(self, player):
        if self.current_attack_cooldown <= 0:
            # ajouter animation ici aussi
            if self.facing == "E":
               damage_zone = pygame.Rect(self.x+40, self.y+10, self.attack_range, 60)
            elif self.facing == "SE":
                damage_zone = pygame.Rect(self.x+10, self.y+10, 30+self.attack_range, 30+self.attack_range)
            elif self.facing == "S":
                damage_zone = pygame.Rect(self.x-10, self.y+40, 60, self.attack_range)
            elif self.facing == "SO":
                damage_zone = pygame.Rect(self.x-self.attack_range, self.y+10, 30+self.attack_range, 30+self.attack_range)
            elif self.facing == "O":
                damage_zone = pygame.Rect(self.x-self.attack_range, self.y-10, self.attack_range, 60)
            elif self.facing == "NO":
                damage_zone = pygame.Rect(self.x-self.attack_range, self.y-self.attack_range, 30+self.attack_range, 30+self.attack_range)
            elif self.facing == "N":
                damage_zone = pygame.Rect(self.x-10,self.y-self.attack_range, 60, self.attack_range)
            else: #NE
                damage_zone = pygame.Rect(self.x+10, self.y-self.attack_range, 30+self.attack_range, 30+self.attack_range)
        
            if damage_zone.colliderect(player.hitbox): #player dans la zone
                print("Damage dealt from Slasher") #peut-être à retirer mais utile pour debug
                player.take_damage(self.damage)
            
            self.current_attack_cooldown = self.attack_cooldown #remise à l'état initial du cooldown


'''
ici prochainement : la classe Flinger, un ennemi qui tire de loin
'''


            
