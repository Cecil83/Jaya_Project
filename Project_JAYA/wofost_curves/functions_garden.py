# -*- coding: utf-8 -*-

import sys, os
import matplotlib

matplotlib.use
import matplotlib.pyplot as plt

plt.style.use('ggplot')

import csv


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

def interact




