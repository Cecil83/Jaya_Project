import csv
import random as rd
from random import randint
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
#path = 'C:/Users/gaeta/PycharmProjects/Jaya/Git/Jaya_Project/Jaya_Project/Project_JAYA/Input/'
path = '.'
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

Nom_plantes, X_plantes, Y_plantes, Color_plantes = [], [], [], []
for i in range(nb_plantes):
    Nom_plantes.append((Data[i+3][0]))
    X_plantes.append(assess_X_coord(int(Data[i+3][1])))
    Y_plantes.append(assess_Y_coord(int(Data[i+3][2])))
    Color_plantes.append((Data[i+3][3]))



def visual():
    fig = plt.figure(figsize=(17, 8))

    ax = fig.add_subplot(111)
    im = ax.scatter(X_plantes, Y_plantes, c=Color_plantes)


    plt.title("Aperçu des plantes du potager ")
    plt.xlim(0, dim_x_potager)
    plt.ylim(0, dim_y_potager)
    plt.xlabel(" Largeur [cm]")
    plt.ylabel("Longueur [cm]")
    plt.grid()

    #    save_path = 'C:/Users/gaeta/PycharmProjects/Jaya/Git/Jaya_Project/Jaya_Project/Project_JAYA/Input/Visuals/'
    save_path = 'Visuals/'
    os.chdir(save_path)
    save_fig = input('Do you want to save the figure ? (y or n) :')
    if save_fig == 'y':
        fig.savefig(filename + '.png', bbox_inches='tight', dpi=150)
    plt.show()

visual()

def debug(arg):
    return arg
