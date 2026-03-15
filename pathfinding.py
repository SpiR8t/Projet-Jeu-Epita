from isometric_motor import map_tiles, iso_to_cart_tile
import math
import heapq

def bresenham(a,b): # renvoie la liste des tuiles traversées par la ligne imaginaire entre 2 points a et b
    x0,y0 = iso_to_cart_tile(a[0], a[1])
    x1,y1 = iso_to_cart_tile(b[0], b[1])

    dx = abs(x0 - x1)
    dy = abs(y0 - y1)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy
    tiles = []
    x,y = x0, y0

    while True:
        tiles.append((x,y))

        if x == x1 and y == y1:
            break

        if 2*err > -dy:
            err -= dy
            x += sx
        if 2*err < dx:
            err += dx
            y += sy
    
    return tiles


def iswalkable(x,y): # vérifie si on peut marcher sur la case aux coordonnées cartésiennes (x,y)
    if x < 0 or y < 0 or x >= len(map_tiles) or y >= len(map_tiles[0]):
        return False
    tile = map_tiles[x][y]
    return (tile[0] == 1 and tile[1] == 0 and tile[2] == 0)

# distance de Tchebychev multipliée par 10 pour correspondre aux costs des tuiles
def heuristic(a,b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) * 10

class Node:
    def __init__(self, position, cost, heuristic):
        self.position = position
        self.cost = cost
        self.heuristic = heuristic
        self.parent = None
    
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)



def astar(start,target,iteration_limit=800): #prend directement les coordonnées cartésiennes des tuiles
    open_set = [] # liste des tuiles voisines
    closed_set = set() # liste des tuiles sur lesquelles on est déjà passé

    start_node = Node(start, 0, heuristic(start, target))
    heapq.heappush(open_set, start_node)

    g = {start: 0} # coût total depuis le départ

    iterations = 0

    while open_set:
        iterations += 1
        if iterations >= iteration_limit: # sécurité pour éviter des calculs inutiles (iteration_limit est modifiable)
            return None
        if not iswalkable(target[0],target[1]): # sécurité pour éviter les longs calculs infinis
            return None
        current_node = heapq.heappop(open_set) # on récupère le meilleur Node (celui avec le plus petit f (= g + heuristic(Node, target)))
        current_pos = current_node.position

        # si on a atteint la cible : on renvoie le chemin parcouru
        if current_pos == target:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        closed_set.add(current_pos)

        # on étudie les 8 voisins de la tuile (dont les diagonales)
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1),(-1,1),(-1,-1)]:
            neighbor_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if not iswalkable(neighbor_pos[0], neighbor_pos[1]): #si c'est un obstacle
                continue
            if abs(dx) == 1 and abs(dy) == 1: #vérification des cases adjacentes si c'est une diagonale (si ce sont des obstacles l'ennemi ne pourra pas atteindre directement la tuile diagonale)
                if not iswalkable(current_pos[0] + dx, current_pos[1]) or not iswalkable(current_pos[0], current_pos[1] + dy):
                    continue
                cost_to_add = 14 # coût d'une diagonale légèrement plus élevé
            else:
                cost_to_add = 10
            if neighbor_pos in closed_set: #si on est déjà passé sur cette tuile
                continue

            potential_new_g = current_node.cost + cost_to_add # nouveau coût du parcours réalisé avec ce nouveau noeud (théorique)

            if potential_new_g < g.get(neighbor_pos, float('inf')):
                g[neighbor_pos] = potential_new_g

                neighbor_node = Node(neighbor_pos, potential_new_g, heuristic(neighbor_pos, target))
                neighbor_node.parent = current_node
                heapq.heappush(open_set, neighbor_node)
        
    return None #si aucun chemin trouvé (ne devrait pas arriver)


