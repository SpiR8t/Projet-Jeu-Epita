from isometric_motor import map_tiles, iso_to_cart_tile
import math

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

def manhattan(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start,target): #en cours de dev
    list = [start]
    currentpath = {}
    cost_since_start = {start: 0}
    estimated_cost = {start:  manhattan(start,target)}

    while list != []:
        pass