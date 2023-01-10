# -*- coding: utf-8 -*-

import sys, os
import matplotlib

matplotlib.use
import matplotlib.pyplot as plt

plt.style.use('ggplot')

import csv
from plante import *

def what_is_in_my_garden(garden):
    #os.chdir(path)
    list_vegetables = []
    # reading csv file to get previous values
    with open(garden, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        i = 1
        for row in csvreader:
            if i > 3:
                list_vegetables.append(row[0])
            else:
                i+=1


    return list_vegetables

def create_list_plant(garden):
    # os.chdir(path)
    list_plant = []
    # reading csv file to get previous values
    j = 0
    with open(garden, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        i = 1
        for row in csvreader:
            if i == 2:
                sun = row[4]
            if i > 3:
                name = "plante_" + str(j)
                Plant1 = Plante(name, row[0], row[1], row[2], row[3], row[4], sun)
                list_plant.append(Plant1)
                j += 1
            else:
                i += 1
    return list_plant

def which_plant_are_in_my_garden(list_plant):
    for plant in list_plant:
        plant.identify_me()

#def interact




