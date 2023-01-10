from plante import *
from potager import *

from math import *
from random import *
def calc_dist_between_plants_and_minus_sun(list_of_plants):
    matrice_dist = []
    for plante_1 in list_of_plants:
        col = []
        for plante_2 in list_of_plants:
            if plante_1.name != plante_2.name :
                if plante_1.position_x == plante_2.position_x:
                    dist = abs(plante_1.position_y - plante_2.position_y)
                elif plante_1.position_y == plante_2.position_y:
                    dist = abs(plante_1.position_x - plante_2.position_x)
                else:
                    dist_x = abs(plante_1.position_x - plante_2.position_x)
                    dist_y = abs(plante_1.position_y - plante_2.position_y)
                    dist = abs(sqrt((dist_x**2) + dist_y**2))

                col.append(dist)

                if dist < (plante_1.rayon + plante_2.rayon):
                    plante_1.sun -= 1


        matrice_dist.append(col)

    return matrice_dist

def calc_dist_between_plants_and_minus_sun_2(list_of_plants):
    matrice_dist = []
    for plante_1 in list_of_plants:
        col = []
        for plante_2 in list_of_plants:
            if plante_1.name != plante_2.name :
                if plante_1.position_x == plante_2.position_x:
                    dist = abs(plante_1.position_y - plante_2.position_y)
                elif plante_1.position_y == plante_2.position_y:
                    dist = abs(plante_1.position_x - plante_2.position_x)
                else:
                    dist_x = abs(plante_1.position_x - plante_2.position_x)
                    dist_y = abs(plante_1.position_y - plante_2.position_y)
                    dist = abs(sqrt((dist_x**2) + dist_y**2))

                col.append(dist)

                if dist < (plante_1.rayon + plante_2.rayon):
                    plante_1.sun -= 1


        matrice_dist.append(col)

    return matrice_dist

def intersection_between_two_plants(r1, d1, r2, d2):
    return (r1**2 * arcos(d1/r1)) - (d1*sqrt(r1**2 - d1**2)) + (r2**2 * arcos(d2/r2)) - (d2* sqrt(r2**2 - d2**2))