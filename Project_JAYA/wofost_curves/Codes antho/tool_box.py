from plante import *
from potager import *

from math import *
from random import *
def calc_dist_between_plants(list_of_plants):
    matrice_dist = [[], []]
    for plante_1 in list_of_plants:
        for plante_2 in list_of_plants:
            if plante_1.position_x == plante_2.position.x:
                dist = abs(plante_1.position_y - plante_2.position_y)
            elif plante_1.position_y == plante_2.position.y:
                dist = abs(plante_1.position_x - plante_2.position_x)
            else:
                dist_x = abs(plante_1.position_x - plante_2.position_x)
                dist_y = abs(plante_1.position_y - plante_2.position_y)
                dist = abs(sqrt((dist_x**2) + dist_y**2))




