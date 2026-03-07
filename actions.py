import animations
from isometric_motor import iso_to_cart_tile

class Action:
    def __init__(self, name, host=True):
        """
        Classe mère pour toutes les actions.

        """
        self.name = name
        self.host = host

    def send_to_network(self, game):
        """
        Gère l'envoi réseau si nécessaire.
        """
        if self.host:
            game.action_created = True
            game.action_name_to_send.append(self.name)

    def execute(self, game_context):
        """
        À redéfinir dans les classes enfants.
        """
        raise NotImplementedError("execute() doit être implémentée.")
    
class EditMapAction(Action):
    """
    Cette action permet de modifier la map, il suffit de lui donner un nom, les coordonnées x et y de la case
    à modifier, et les 3 numéro de tile qu'on veut appliquer du bas vers le haut.
    """
    def __init__(self, x, y, tile_nb0, tile_nb1, tile_nb2, host=True):
        super().__init__(f"Edit Map ({x},{y})", host)
        # Coordonnées de la case
        self.x = x
        self.y = y
        self.tile_nb = (tile_nb0,tile_nb1,tile_nb2)

    def execute(self, game_context):
        print("Changement map : x =", self.x,", y =", self.y, "->", self.tile_nb)
        # gestion réseau commune
        super().send_to_network(game_context)
        game_context.add_info_edit_map_action(self.x, self.y, self.tile_nb[0], self.tile_nb[1], self.tile_nb[2])

        game_context.map.tiles[self.y][self.x][0] = self.tile_nb[0]
        game_context.map.tiles[self.y][self.x][1] = self.tile_nb[1]
        game_context.map.tiles[self.y][self.x][2] = self.tile_nb[2]

class MeleeAction(Action):
    def __init__(self, caster, range, x=0, y=0, dx=0, dy=0, host=True):
        super().__init__("Melee", host)
        self.range = range

        # Cas 1 : action créée localement
        if caster is not None:
            self.direction = caster.direction
            self.position = caster.get_pos()
        # Cas 2 : action reçue via réseau
        else:
            self.position = (x, y)
            self.direction = (dx, dy)

    def execute(self, game_context):
        print("Melee action")

        # gestion réseau commune
        self.send_to_network(game_context)

        dx, dy = self.direction

        # position devant le joueur
        target_x = self.position[0] + 16 + dx * 32
        target_y = self.position[1] - 16 + dy * 32

        anim = animations.SimpleSlashAnimation(target_x, target_y, (dx, dy))
        game_context.animations.append(anim)

class LeverAction(Action): # l'action pour switch un levier
    def __init__(self, id_group, id_lever, host=True):
        super().__init__("Lever Action", host)

        self.id_group = id_group
        self.id_lever = id_lever

    def send_to_network(self, context):
        super().send_to_network(context)
        context.add_info_lever_action(self.id_group, self.id_lever) # on ajoute une instruction pour envoyer les
                                                                    # infos du levier dans le multi 
    def execute(self, context, gameRegister, matrix):
        if gameRegister.levers[self.id_group][self.id_lever].locked != True:
            self.send_to_network(context)
            
            gameRegister.levers[self.id_group][self.id_lever].toggle(matrix)

class interactAction(Action):
    def __init__(self, x,y, host=True):
        super().__init__("Interact Action", host)
        self.x = x
        self.y = y

    def send_to_network(self, context, coords_carto): # on envoie les coordonnées de l'endroit de l'interaction avec
        super().send_to_network(context)
        context.add_info_interact_action(coords_carto)

    def leverVerif(self, gameRegister, x,y): # une méthode pour checker les levier, il en faudra d'autres pour les autres éléments
        for group in gameRegister.levers:
            for lever in gameRegister.levers[group]:
                if lever.position == (x,y):
                    return (lever.group, lever.id)

    def execute(self, context, gameRegister):
        
        carto = iso_to_cart_tile(self.x, self.y)
        self.send_to_network(context, carto)
        # vérif pour levier
        lever = self.leverVerif(gameRegister, carto[0],carto[1])
        if (lever) :
            context.add_action(LeverAction(lever[0], lever[1]))

        # vérif pour d'autres choses interactive par la suite
        # ->

        # if interact a fait qlq chose il faudra faire animation interaction


class SlasherAttack(Action):
    def __init__(self, caster, range=50, x=0, y=0, facing="N", host=True):
        super().__init__("SlasherAttack", host)

        if caster:
            self.facing = caster.facing
        else: #si action provenant du réseau
            self.facing = facing

    def execute(self, game):
        print("Slasher attack executée")
        self.send_to_network(game)