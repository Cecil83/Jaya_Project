#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 16:17:25 2022

@author: user
"""

import pandas as pd
import numpy as np


import sys, os, csv
import matplotlib.pyplot as plt
import pandas as pd
import datetime,yaml, time

from itertools import product
from tqdm import tqdm


data_dir = os.path.join(os.getcwd(), '10gran_3crop_1soil_2022_12_06_00_25_09')

data_dict = dict()

for run_type in os.listdir(data_dir):
    data_dict[run_type] = pd.read_csv(os.path.join(data_dir,run_type, 'Data'))
    data_dict[run_type] = data_dict[run_type].sort_values(by=['Irradiation', 'Temperature', 'Wind', 'Rain'])



# A faire, trouver automatiquement la shape à faire !!!
def reshape_to_numpy(dataframe):
    a = dataframe.to_numpy()
    
    for i in range(3):
        a = np.expand_dims(a, axis=0)
    
    a = a.reshape((10,10,10,10,5))
    
    return a

"""

df = pd.read_csv("Data.csv")

df = df.sort_values(by=['Irradiation', 'Temperature', 'Wind', 'Rain'])

a = df.to_numpy().astype(int)

print("a avant reshape")
print(a)

for i in range(3):
    a = np.expand_dims(a, axis=0)

a = a.reshape((2,2,2,2,5))

print("a après reshape")
for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                print(a[i][j][k][l])"""


numpy_dict = dict()

for run_type in data_dict.keys():
    numpy_dict[run_type] = reshape_to_numpy(data_dict[run_type])


for run_type in data_dict.keys():
    irrad_list = numpy_dict[run_type][:,1,1,1][:,0]
    temp_list = numpy_dict[run_type][1,:,1,1][:,1]
    wind_list = numpy_dict[run_type][1,1,:,1][:,2]
    rain_list = numpy_dict[run_type][1,1,1,:][:,3]
    break


"""
def get_slices(irrad,temp,wind,rain):
    
    #Spécifie par paramètre, soit l'indice du paramètre concerné, soit False pour avoir tout

    if not irrad:
        irrad_numpy = 
    else:"""

def print_irrad(temp,wind,rain):
    fig, ax = plt.subplots()
    for run_type in data_dict.keys():
        ax.plot(numpy_dict[run_type][:,temp,wind,rain][:,0],
                numpy_dict[run_type][:,temp,wind,rain][:,4], '-',
                label=run_type)
        
    ax.legend()
    ax.set_title(f"Temp = {temp_list[temp]:.1f}, Wind = {wind_list[wind]:.1f}, Rain = {rain_list[rain]:.1f}")
    fig.suptitle("TWSO (kg ha-1) en fonction de l'irradiation (unité ??)", fontsize=14, fontweight='bold')
    fig.savefig(os.path.join(os.getcwd(), 'irradiation_plot.png'))
    fig.show()
    
def print_temp(irrad,wind,rain):
    fig, ax = plt.subplots()
    for run_type in data_dict.keys():
        ax.plot(numpy_dict[run_type][irrad,:,wind,rain][:,1],
                numpy_dict[run_type][irrad,:,wind,rain][:,4], '-',
                label=run_type)
        
    ax.legend()
    ax.set_title(f"Irrad = {irrad_list[irrad]:.1f}, Wind = {wind_list[wind]:.1f}, Rain = {rain_list[rain]:.1f}")
    fig.suptitle('TWSO (kg ha-1) en fonction de la température (°C)', fontsize=14, fontweight='bold')
    fig.savefig(os.path.join(os.getcwd(), 'temperature_plot.png'))
    fig.show()
    
def print_wind(irrad,temp,rain):
    fig, ax = plt.subplots()
    for run_type in data_dict.keys():
        ax.plot(numpy_dict[run_type][irrad,temp,:,rain][:,2],
                numpy_dict[run_type][irrad,temp,:,rain][:,4], '-',
                label=run_type)
        
    ax.legend()
    ax.set_title(f"Irrad = {irrad_list[irrad]:.1f}, Temp = {temp_list[temp]:.1f}, Rain = {rain_list[rain]:.1f}")
    fig.suptitle('TWSO (kg ha-1) en fonction du vent (unité ??)', fontsize=14, fontweight='bold')
    fig.savefig(os.path.join(os.getcwd(), 'wind_plot.png'))
    fig.show()
    
def print_rain(irrad,temp,wind):
    fig, ax = plt.subplots()
    for run_type in data_dict.keys():
        ax.plot(numpy_dict[run_type][irrad,temp,wind,:][:,3],
                numpy_dict[run_type][irrad,temp,wind,:][:,4], '-',
                label=run_type)
        
    ax.legend()
    ax.set_title(f"Irrad = {irrad_list[irrad]:.1f}, Temp = {temp_list[temp]:.1f}, Wind = {wind_list[wind]:.1f}")
    fig.suptitle('TWSO (kg ha-1) en fonction de la pluie (unité ??)', fontsize=14, fontweight='bold')
    fig.savefig(os.path.join(os.getcwd(), 'rain_plot.png'))
    fig.show()
    

def get_integer_related_to_value(irrad,temp,wind,rain):
    """
    Récupère l'indice le plus proche associé aux valeurs données
    """
    closest_irrad = min(irrad_list, key=lambda x:abs(x-irrad))
    closest_temp = min(temp_list, key=lambda x:abs(x-temp))
    closest_wind = min(wind_list, key=lambda x:abs(x-wind))
    closest_rain = min(rain_list, key=lambda x:abs(x-rain))
    irrad_indice = list(irrad_list).index(closest_irrad)
    temp_indice = list(temp_list).index(closest_temp)
    wind_indice = list(wind_list).index(closest_wind)
    rain_indice = list(rain_list).index(closest_rain)
    return irrad_indice,temp_indice,wind_indice,rain_indice


irrad_indice,temp_indice,wind_indice,rain_indice = get_integer_related_to_value(27000, 15., 4., 10.)
print_irrad(temp_indice, wind_indice, rain_indice)
print_temp(irrad_indice, wind_indice, rain_indice)
print_wind(irrad_indice, temp_indice, rain_indice)
print_rain(irrad_indice, temp_indice, wind_indice)


# 2D irrad et température
for run_type in data_dict.keys():
    fig, ax = plt.subplots()
    CS = ax.contourf(numpy_dict[run_type][irrad_indice,:,wind_indice,rain_indice][:,1],
                     numpy_dict[run_type][:,temp_indice,wind_indice,rain_indice][:,0],
                     numpy_dict[run_type][:,:,wind_indice,rain_indice][:,:,4], 100,
                     cmap='inferno')
    ax.set_title(f"Wind = {wind_list[wind_indice]:.1f}, Rain = {rain_list[rain_indice]:.1f}")
    ax.set_ylabel("Irrad")
    ax.set_xlabel("Temp")
    fig.colorbar(CS,label="TWSO (kg ha-1)")
    fig.suptitle(run_type, fontsize=14, fontweight='bold')
    fig.savefig(os.path.join(os.getcwd(), f'{run_type}_contourf_plot.png'))
    fig.show()


# 3D irrad, temp et rain
    
for run_type in data_dict.keys():
    data = numpy_dict[run_type][:,:,wind_indice,:][:,:,:,4]
    x = numpy_dict[run_type][irrad_indice,:,wind_indice,rain_indice][:,1]
    y = numpy_dict[run_type][irrad_indice,temp_indice,wind_indice,:][:,3]
    z = numpy_dict[run_type][:,temp_indice,wind_indice,rain_indice][:,0]
    X,Y,Z = np.meshgrid(x, y, z)
    
    # Creating figure
    fig = plt.figure(figsize=(12.,5.))
    ax = plt.axes(projection="3d")
    
    #Creating plot
    
    CS = ax.scatter3D(X, Y, Z, c=data, alpha = 0.7, marker='o', cmap='inferno')
    ax.set_title(f"Wind = {wind_list[wind_indice]:.1f}")
    ax.set_xlabel("Temp")
    ax.set_ylabel("Rain")
    ax.set_zlabel("Irrad")
    fig.colorbar(CS,ax=ax,label="TWSO (kg ha-1)", location="right")
    fig.suptitle(run_type, fontsize=14, fontweight='bold')
    fig.savefig(os.path.join(os.getcwd(), f'{run_type}_contourf_plot.png'))
    fig.show()