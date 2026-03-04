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
        print("send")
        if self.host:
            game.action_created = True
            game.action_name_to_send.append(self.name)

    def execute(self, game_context):
        """
        À redéfinir dans les classes enfants.
        """
        raise NotImplementedError("execute() doit être implémentée.")

class LeverAction(Action):
    pass
    
class EditMapAction(Action):
    """
    Cette action permet de modifier la map, il suffit de lui donner un nom, les coordonnées x et y de la case
    à modifier, et les 3 numéro de tile qu'on veut appliquer du bas vers le haut.
    """
    def __init__(self, name, x, y, tile_nb0, tile_nb1, tile_nb2, host=True):
        super().__init__(name, host)
        # Coordonnées de la case
        self.x = x
        self.y = y
        self.tile_nb = (tile_nb0,tile_nb1,tile_nb2)

    def execute(self, game_context):
        print("Changement map")
        # gestion réseau commune
        self.send_to_network(game_context)

        game_context.map.tiles[self.x][self.y][0] = self.tile_nb[0]
        game_context.map.tiles[self.x][self.y][1] = self.tile_nb[1]
        game_context.map.tiles[self.x][self.y][2] = self.tile_nb[2]
