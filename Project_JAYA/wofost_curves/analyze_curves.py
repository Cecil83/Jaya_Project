import sys, os

# sys.path.insert(1, '/home/user/Documents/imag/Manintec/Jaya/code/pcse')
import matplotlib
# matplotlib.style.use("ggplot")
import matplotlib.pyplot as plt
import pandas as pd
import datetime, yaml, time
import csv

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
    #print(Data)
    return Data


data_dir = os.path.join(os.getcwd(), 'data')
results_dir = os.path.join(os.getcwd(), 'results')
#dir_analyze = os.path.join(results_dir, '2022_12_05_14_44_51')
dir_analyze = os.path.join(results_dir, '10gran_3crop_1soil_2022_12_06_00_25_09')

print("python version: %s " % sys.version)

sys.path.insert(1, dir_analyze)
import config_sim as c

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

        # Vars = ['temp', 'irrad', 'rain', 'wind']
        # ind=0
        # for var in var_dict.keys():
        #     for val in var_dict[var]:
        #         analyze_dict[var] = [(var, 'Min', 'Moy', 'Max')]
        #         var_min, var_incr, var_max = 15000, 0, 0
        #         for i in range(c.granularite**4):
        #             if Data_raw[i+1][ind] == val:
        #                 twso_val = Data_raw[i+1][4]
        #                 if twso_val < var_min:
        #                     var_min = twso_val
        #                 if twso_val > var_max:
        #                     var_max = twso_val
        #                 var_incr += twso_val
        #             analyze_dict[var].append((val, var_min, var_incr / c.granularite, var_max))
        #             print(analyze_dict[var])
        #
        #
        #     ind+=1

        print(soil)
        print(crop.name)
        print(c.suns, c.winds, c.rains, c.temps)

        analyze_temp = [('Température', 'Min', 'Moy', 'Max')]
        analyze_irrad = [('Irradiation', 'Min', 'Moy', 'Max')]
        analyze_rain = [('Rain', 'Min', 'Moy', 'Max')]
        analyze_wind = [('Wind', 'Min', 'Moy', 'Max')]

        for irrad in c.suns:
            irrad_min, irrad_incr, irrad_max = 15000, 0, 0
            for i in range(c.granularite ** 4):
                if float(Data_raw[i + 1][0]) == irrad:
                    twso_val = float(Data_raw[i + 1][4])
                    if twso_val < irrad_min:
                        irrad_min = twso_val
                    if twso_val > irrad_max:
                        irrad_max = twso_val
                    irrad_incr += twso_val
            analyze_irrad.append((irrad, irrad_min, irrad_incr / c.granularite, irrad_max))

        for temp in c.temps:
            temp_min, temp_incr, temp_max = 15000, 0, 0
            for i in range(c.granularite ** 4):
                if float(Data_raw[i + 1][1]) == temp:
                    twso_val = float(Data_raw[i + 1][4])
                    if twso_val < temp_min:
                        temp_min = twso_val
                    if twso_val > temp_max:
                        temp_max = twso_val
                    temp_incr += twso_val
            analyze_temp.append((temp, temp_min, temp_incr / c.granularite, temp_max))

        for wind in c.winds:
            wind_min, wind_incr, wind_max = 15000, 0, 0
            for i in range(c.granularite ** 4):
                if float(Data_raw[i + 1][2]) == wind:
                    twso_val = float(Data_raw[i + 1][4])
                    if twso_val < wind_min:
                        wind_min = twso_val
                    if twso_val > wind_max:
                        wind_max = twso_val
                    wind_incr += twso_val
            analyze_wind.append((wind, wind_min, wind_incr / c.granularite, wind_max))

        for rain in c.rains:
            rain_min, rain_incr, rain_max = 15000, 0, 0
            for i in range(c.granularite ** 4):
                if float(Data_raw[i + 1][3]) == rain:
                    twso_val = float(Data_raw[i + 1][4])
                    if twso_val < rain_min:
                        rain_min = twso_val
                    if twso_val > rain_max:
                        rain_max = twso_val
                    rain_incr += twso_val
            analyze_rain.append((rain, rain_min, rain_incr / c.granularite, rain_max))

        abs_max, index = 0, 0
        for i in range(c.granularite ** 4):
            if float(Data_raw[i + 1][4]) > abs_max:
                abs_max = float(Data_raw[i + 1][4])
                index = i + 1

        print(f"TWSO max value is {abs_max} and was reach for {[Data_raw[index][i] for i in range(4)]}")

        Analyse_results = analyze_temp + analyze_irrad + analyze_rain + analyze_wind
        Analyse_results.append((f"TWSO max value is {abs_max} and was reach for {[Data_raw[index][i] for i in range(4)]}",'0','0','0'))
        Write_csv_from_Data(f"Analyse_Results_dim{c.granularite}_{crop.name}_{soil}.csv", dir_analyze, Analyse_results)





























