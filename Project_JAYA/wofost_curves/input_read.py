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
    print("Returning the following Data")
    print(Data)
    return Data


def assess_X_coord(x_val, dim_x_potager):
    if x_val < 0:
        x_val=0
    if x_val >dim_x_potager:
        x_val=dim_x_potager
    return x_val

def assess_Y_coord(y_val, dim_y_potager):
    if y_val < 0:
        y_val=0
    if y_val >dim_y_potager:
        y_val=dim_y_potager
    return y_val




def count_different_plants(Nom_plantes, nb_plantes):
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



def visual(nb_plantes, X_plantes, Y_plantes, Rayons, Color_plantes, index_unique, Noms_plantes_unique, dim_x_potager, dim_y_potager, Data, productivity, twso, filename):
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


    text = f"Productivité = {productivity:.2f} %"
    ax.add_patch(Rectangle((0.1, 0.3), text_length + 0.15, -0.1, color="tomato", alpha=0.5))
    plt.text(0.12, 0.25, text, horizontalalignment='left', size='medium', color='black')

    text = f"TWSO = {twso:.2f} kg/ha"
    ax.add_patch(Rectangle((0.5, 0.3), text_length + 0.2, -0.1, color="tomato", alpha=0.5))
    plt.text(0.52, 0.25, text, horizontalalignment='left', size='medium', color='black')

    plt.axis("off")

    save_path = './Visual'
    os.chdir(save_path)
    # save_fig = input('Do you want to save the figure ? (y or n) :')
    save_fig = 'y'
    if save_fig == 'y':
        fig.savefig(filename + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.png', bbox_inches='tight', dpi=150)
    plt.show()


def debug(arg):
    return arg
