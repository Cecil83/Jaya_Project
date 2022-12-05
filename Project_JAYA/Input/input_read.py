import csv
import random as rd
from random import randint
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt
import math
import matplotlib.patches
from matplotlib.patches import Rectangle
import datetime


# cd PycharmProjects/Jaya/Git/Jaya_Project/Jaya_Project/Project_JAYA/
# Lis le fichier csv comme entrée du modèle
# Permet d'avoir les informations sur le potager (dimension en x et y, conditions PC, eventuellement localisation)
# ainsi que le nombre de plantes et leurs coordonnées dans le jardin

#Les dimensions/coordonnées dans le potager sont en cm, la maille de la grille fait 1cm.



def Read_csv_into_Data(path, filename):
    # Get in the right directory
    os.chdir(path)
    Data = []
    # reading csv file to get previous values
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            Data.append(row)
    print("Reading", filename, "in", path)
    print("Returning the following Data.csv")
    print(Data)
    return Data

path = 'C:/Users/gaeta/PycharmProjects/Jaya/Git/Jaya_Project/Project_JAYA/Input/'
filename = 'test_input'
Data = Read_csv_into_Data(path, filename + '.csv')

header_potager = Data[0]
header_plantes = Data[2]

dim_x_potager = float(Data[1][0])
dim_y_potager = float(Data[1][1])
eau_potager = float(Data[1][2])
temp_potager = float(Data[1][3])
soleil_potager = float(Data[1][4])
nutri_potager = float(Data[1][5])

nb_plantes = len(Data)-3

def assess_X_coord(x_val):
    if x_val < 0:
        x_val=0
    if x_val >dim_x_potager:
        x_val=dim_x_potager
    return x_val

def assess_Y_coord(y_val):
    if y_val < 0:
        y_val=0
    if y_val >dim_y_potager:
        y_val=dim_y_potager
    return y_val

Nom_plantes, X_plantes, Y_plantes, Rayons, Color_plantes = [], [], [], [], []
for i in range(nb_plantes):
    Nom_plantes.append((Data[i+3][0]))
    X_plantes.append(assess_X_coord(int(Data[i+3][1])))
    Y_plantes.append(assess_Y_coord(int(Data[i+3][2])))
    Rayons.append((int(Data[i+3][3])))
    Color_plantes.append((Data[i+3][4]))

def count_different_plants():
    noms, indexs = [Nom_plantes[0]], [0]
    i = 1; j = 0
    while i < nb_plantes:
        if noms[j] != Nom_plantes[i]:
            noms.append(Nom_plantes[i])
            indexs.append(i)
            j+=1
            print(i)
        i += 1
    return noms, indexs

Noms_plantes_unique, index_unique = count_different_plants()
print(Noms_plantes_unique, index_unique)

def visual():
    fig = plt.figure(figsize=(14, 6))

    ax = fig.add_subplot(121)
    for i in range(nb_plantes):
        ax.add_artist(matplotlib.patches.Circle((X_plantes[i], Y_plantes[i]), Rayons[i], color='lightgray', alpha=0.7))
    ax.scatter(X_plantes, Y_plantes, c=Color_plantes)

    for i in range(len(index_unique)):
        ax.scatter(X_plantes[index_unique[i]], Y_plantes[index_unique[i]], c=Color_plantes[index_unique[i]], label=Noms_plantes_unique[i])



    plt.title("Aperçu des plantes du potager ")
    ax.legend()
    plt.xlim(0, dim_x_potager)
    plt.ylim(0, dim_y_potager)
    plt.xlabel(" Largeur [cm]")
    plt.ylabel("Longueur [cm]")
    plt.grid()


    ax = fig.add_subplot(122)

    text_length = 0.2
    text = "Eau = " + str(Data[1][2])
    ax.add_patch(Rectangle((0.1, 0.9), text_length, -0.1, color="blue", alpha=0.3))
    plt.text(0.12, 0.85, text, horizontalalignment='left', size='medium', color='black')

    text = "Température = " + str(Data[1][3])
    ax.add_patch(Rectangle((0.5, 0.9), text_length + 0.1, -0.1, color="firebrick", alpha=0.3))
    plt.text(0.52, 0.85, text, horizontalalignment='left', size='medium', color='black')

    text = "Soleil = " + str(Data[1][4])
    ax.add_patch(Rectangle((0.1, 0.7), text_length, -0.1, color="gold", alpha=0.3))
    plt.text(0.12, 0.65, text, horizontalalignment='left', size='medium', color='black')

    text = "Nutriments = " + str(Data[1][5])
    ax.add_patch(Rectangle((0.5, 0.7), text_length + 0.1, -0.1, color="mediumpurple", alpha=0.3))
    plt.text(0.52, 0.65, text, horizontalalignment='left', size='medium', color='black')


    text = "Productivité = " + str(Data[1][6]) + " %"
    ax.add_patch(Rectangle((0.1, 0.3), text_length + 0.15, -0.1, color="tomato", alpha=0.5))
    plt.text(0.12, 0.25, text, horizontalalignment='left', size='medium', color='black')

    text = "TWSO = " + str(Data[1][7]) + " kg/ha"
    ax.add_patch(Rectangle((0.5, 0.3), text_length + 0.2, -0.1, color="tomato", alpha=0.5))
    plt.text(0.52, 0.25, text, horizontalalignment='left', size='medium', color='black')

    plt.axis("off")

    save_path = 'C:/Users/gaeta/PycharmProjects/Jaya/Git/Jaya_Project/Project_JAYA/Input/Visuals/'
    os.chdir(save_path)
    # save_fig = input('Do you want to save the figure ? (y or n) :')
    save_fig = 'y'
    if save_fig == 'y':
        fig.savefig(filename + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.png', bbox_inches='tight', dpi=150)
    plt.show()

visual()
def debug(arg):
    return arg
