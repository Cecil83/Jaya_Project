import sys, os

# sys.path.insert(1, '/home/user/Documents/imag/Manintec/Jaya/code/pcse')
import matplotlib
# matplotlib.style.use("ggplot")
import matplotlib.pyplot as plt
import pandas as pd
import datetime, yaml, time
import csv


data_dir = os.path.join(os.getcwd(), 'data')
results_dir = os.path.join(os.getcwd(), 'results')
dir_analyze = os.path.join(os.getcwd(), '2022_12_05_14_44_51')
print("python version: %s " % sys.version)

sys.path.insert(1,dir_analyze)
import config as c


def Write_csv_from_Data(filename, path, Data_W):
    os.chdir(path)
    f = open(filename, 'w')
    # create the csv writer
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    # writer.writerow(header)
    for row in Data_W:
        writer.writerow(row)
    f.close()

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

var_dict = { 'irrad': c.suns,
             'temp': c.temps,
             'wind': c.wind,
             'rain': c.rain}

analyze_dict = {'irrad': list(),
             'temp': list(),
             'wind': list(),
             'rain': list()}


for soil in c.soils:
    for crop in c.crops:
        results_dir_now = os.path.join(dir_analyze, f"{soil}_{crop.name}")
        Data_raw = Read_csv_into_Data(results_dir_now, 'Data.csv')

        Vars = ['temp', 'irrad', 'rain', 'wind']
        ind=0
        for var in var_dict.keys():
            for val in var_dict[var]:
                analyze_dict[var] = [(var, 'Min', 'Moy', 'Max')]
                var_min, var_incr, var_max = 15000, 0 , 0
                for i in range(c.granularite**4):
                    if Data_raw[i+1][ind]==val:
                        twso_val = Data_raw[i+1][4]
                        if twso_val < var_min:
                            var_min = twso_val
                        if twso_val > var_max:
                            var_max = twso_val
                        var_incr += twso_val
                    analyze_irrad.append((irrad, irrad_min, irrad_incr / dim, irrad_max))


            ind+=1

        analyze_temp = [('Température', 'Min', 'Moy', 'Max')]
        analyze_irrad = [('Irradiation', 'Min', 'Moy', 'Max')]
        analyze_rain = [('Rain', 'Min', 'Moy', 'Max')]
        analyze_wind = [('Wind', 'Min', 'Moy', 'Max')]
