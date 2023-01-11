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
#dir_analyze = os.path.join(results_dir, '10gran_3crop_1soil_2022_12_06_00_25_09')
dir_analyze = os.path.join(results_dir, '10gran_3crop_1soil_2022_12_06_22_05_51')
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

dim = c.gran_temp * c.gran_irrad * c.gran_rain * c.gran_wind
def analyse_min_moy_max():
    for soil in c.soils:
        fig, a = plt.subplots(2, 2)
        for crop in c.crops:
            results_dir_now = os.path.join(dir_analyze, f"{soil}_{crop.name}")
            Data_raw = Read_csv_into_Data(results_dir_now, 'Data.csv')

            # Vars = ['temp', 'irrad', 'rain', 'wind']
            # ind=0
            # for var in var_dict.keys():
            #     for val in var_dict[var]:
            #         analyze_dict[var] = [(var, 'Min', 'Moy', 'Max')]
            #         var_min, var_incr, var_max = 15000, 0, 0
            #         for i in range(dim):
            #             if Data_raw[i+1][ind] == val:
            #                 twso_val = Data_raw[i+1][4]
            #                 if twso_val < var_min:
            #                     var_min = twso_val
            #                 if twso_val > var_max:
            #                     var_max = twso_val
            #                 var_incr += twso_val
            #             analyze_dict[var].append((val, var_min, var_incr / c.gran, var_max))
            #             print(analyze_dict[var])
            #
            #
            #     ind+=1

            print(soil)
            print(crop.name)
            print(c.suns, c.winds, c.rains, c.temps)

            analyze_temp = [('Température', 'Twso_min', 'Twso_moy', 'Twso_max')]
            analyze_irrad = [('Irradiation', 'Twso_min', 'Twso_moy', 'Twso_max')]
            analyze_rain = [('Rain', 'Twso_min', 'Twso_moy', 'Twso_max')]
            analyze_wind = [('Wind', 'Twso_min', 'Twso_moy', 'Twso_max')]


            for irrad in c.suns:
                irrad_min, irrad_incr, irrad_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][0]) == irrad:
                        twso_val = float(Data_raw[i + 1][4])
                        if twso_val < irrad_min:
                            irrad_min = twso_val
                        if twso_val > irrad_max:
                            irrad_max = twso_val
                        irrad_incr += twso_val

                analyze_irrad.append((irrad, irrad_min, irrad_incr / (dim), irrad_max))

            for temp in c.temps:
                temp_min, temp_incr, temp_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][1]) == temp:
                        twso_val = float(Data_raw[i + 1][4])
                        if twso_val < temp_min:
                            temp_min = twso_val
                        if twso_val > temp_max:
                            temp_max = twso_val
                        temp_incr += twso_val
                analyze_temp.append((temp, temp_min, temp_incr / (dim), temp_max))

            for wind in c.winds:
                wind_min, wind_incr, wind_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][2]) == wind:
                        twso_val = float(Data_raw[i + 1][4])
                        if twso_val < wind_min:
                            wind_min = twso_val
                        if twso_val > wind_max:
                            wind_max = twso_val
                        wind_incr += twso_val
                analyze_wind.append((wind, wind_min, wind_incr / (dim), wind_max))

            for rain in c.rains:
                rain_min, rain_incr, rain_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][3]) == rain:
                        twso_val = float(Data_raw[i + 1][4])
                        if twso_val < rain_min:
                            rain_min = twso_val
                        if twso_val > rain_max:
                            rain_max = twso_val
                        rain_incr += twso_val
                analyze_rain.append((rain, rain_min, rain_incr / (dim), rain_max))

            abs_max, index = 0, 0
            for i in range(dim):
                if float(Data_raw[i + 1][4]) > abs_max:
                    abs_max = float(Data_raw[i + 1][4])
                    index = i + 1

            print(f"TWSO max value is {abs_max} and was reach for {[Data_raw[index][i] for i in range(4)]}")

            Analyse_results = analyze_temp + analyze_irrad + analyze_rain + analyze_wind
            Analyse_results.append((f"TWSO max value is {abs_max} and was reach for {[Data_raw[index][i] for i in range(4)]}", '0', '0', '0'))
            Write_csv_from_Data(f"Analyse_Results_dim{c.gran}_{crop.name}_{soil}.csv", dir_analyze, Analyse_results)

            #Affichage graphique
            Crops_irrad, Crops_temp, Crops_rain, Crops_wind = list(), list(), list(), list()

            ind=1
            for i in range(c.gran_temp):
                Crops_temp.append(Analyse_results[ind+i][2])
            ind += c.gran_temp + 1

            a[0][0].plot(c.temps, Crops_temp, label=str(crop.name))
            a[0][0].set_xlabel('Température en °C')
            a[0][0].set_ylabel('TWSO en kg/ha')
            a[0][0].legend()


            for i in range(c.gran_irrad):
                Crops_irrad.append(Analyse_results[ind+i][2])
            ind += c.gran_irrad + 1

            a[0][1].plot(c.suns, Crops_irrad, label=str(crop.name))
            a[0][1].set_xlabel('Irradiation en kJ/m2/day')
            a[0][1].set_ylabel('TWSO en kg/ha')
            a[0][1].legend()


            for i in range(c.gran_rain):
                Crops_rain.append(Analyse_results[ind+i][2])
            ind += c.gran_rain + 1

            a[1][0].plot(c.rains, Crops_rain, label=str(crop.name))
            a[1][0].set_xlabel('Rain en mm')
            a[1][0].set_ylabel('TWSO en kg/ha')
            a[1][0].legend()


            for i in range(c.gran_wind):
                Crops_wind.append(Analyse_results[ind+i][2])
            ind += c.gran_wind + 1

            a[1][1].plot(c.winds, Crops_wind, label=str(crop.name))
            a[1][1].set_xlabel('Wind en m/s')
            a[1][1].set_ylabel('TWSO en kg/ha')
            a[1][1].legend()

        fig.suptitle(f"Evolution de la valeur moyenne du TWSO pour le sol {soil}")
        fig.savefig(f"Analyse_Results_dim_{soil}.png", bbox_inches='tight', dpi=150)
        plt.show()

#analyse_min_moy_max()
def analyse_min_moy_max_augmented():
    for soil in c.soils:
        fig, a = plt.subplots(2, 2)
        for crop in c.crops:
            results_dir_now = os.path.join(dir_analyze, f"{soil}_{crop.name}")
            Data_raw = Read_csv_into_Data(results_dir_now, 'Data_lai.csv')

            print(soil)
            print(crop.name)
            print(c.suns, c.winds, c.rains, c.temps)

            analyze_temp = [('Température', 'Twso_min', 'Twso_moy', 'Twso_max', 'Time_min', 'Time_moy', 'Time_max',
                             'Lai_min', 'Lai_moy', 'Lai_max')]
            analyze_irrad = [('Irradiation', 'Twso_min', 'Twso_moy', 'Twso_max', 'Time_min', 'Time_moy', 'Time_max',
                              'Lai_min', 'Lai_moy', 'Lai_max')]
            analyze_rain = [('Rain', 'Twso_min', 'Twso_moy', 'Twso_max', 'Time_min', 'Time_moy', 'Time_max', 'Lai_min',
                             'Lai_moy', 'Lai_max')]
            analyze_wind = [('Wind', 'Twso_min', 'Twso_moy', 'Twso_max', 'Time_min', 'Time_moy', 'Time_max', 'Lai_min',
                             'Lai_moy', 'Lai_max')]


            Types = [c.suns, c.temps, c.winds, c.rains]
            type_index = 0
            for type in Types:
                for type_val in type:
                    Mins = [15000, 15000, 15000]
                    Incrs = [0, 0, 0]
                    Maxs = [0, 0, 0]
                    Values = [0, 0, 0]
                    for i in range(dim):
                        if
                
                type_index += 1


            for irrad in c.suns:
                irrad_min, irrad_incr, irrad_max = 15000, 0, 0
                time_min, time_incr, time_max = 15000, 0, 0
                lai_min, lai_incr, lai_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][0]) == irrad:
                        twso_val, time_val, lai_val = float(Data_raw[i + 1][4]), float(Data_raw[i + 1][5]), float(
                            Data_raw[i + 1][6])
                        if twso_val < irrad_min:
                            irrad_min = twso_val
                        if twso_val > irrad_max:
                            irrad_max = twso_val
                        irrad_incr += twso_val

                analyze_irrad.append((irrad, irrad_min, irrad_incr / (dim), irrad_max))

            for temp in c.temps:
                temp_min, temp_incr, temp_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][1]) == temp:
                        twso_val = float(Data_raw[i + 1][4])
                        if twso_val < temp_min:
                            temp_min = twso_val
                        if twso_val > temp_max:
                            temp_max = twso_val
                        temp_incr += twso_val
                analyze_temp.append((temp, temp_min, temp_incr / (dim), temp_max))

            for wind in c.winds:
                wind_min, wind_incr, wind_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][2]) == wind:
                        twso_val = float(Data_raw[i + 1][4])
                        if twso_val < wind_min:
                            wind_min = twso_val
                        if twso_val > wind_max:
                            wind_max = twso_val
                        wind_incr += twso_val
                analyze_wind.append((wind, wind_min, wind_incr / (dim), wind_max))

            for rain in c.rains:
                rain_min, rain_incr, rain_max = 15000, 0, 0
                for i in range(dim):
                    if float(Data_raw[i + 1][3]) == rain:
                        twso_val = float(Data_raw[i + 1][4])
                        if twso_val < rain_min:
                            rain_min = twso_val
                        if twso_val > rain_max:
                            rain_max = twso_val
                        rain_incr += twso_val
                analyze_rain.append((rain, rain_min, rain_incr / (dim), rain_max))

            abs_max, index = 0, 0
            for i in range(dim):
                if float(Data_raw[i + 1][4]) > abs_max:
                    abs_max = float(Data_raw[i + 1][4])
                    index = i + 1

            print(f"TWSO max value is {abs_max} and was reach for {[Data_raw[index][i] for i in range(4)]}")

            Analyse_results = analyze_temp + analyze_irrad + analyze_rain + analyze_wind
            Analyse_results.append((
                                   f"TWSO max value is {abs_max} and was reach for {[Data_raw[index][i] for i in range(4)]}",
                                   '0', '0', '0'))
            Write_csv_from_Data(f"Analyse_Results_dim{c.gran}_{crop.name}_{soil}.csv", dir_analyze, Analyse_results)

            # Affichage graphique
            Crops_irrad, Crops_temp, Crops_rain, Crops_wind = list(), list(), list(), list()

            ind = 1
            for i in range(c.gran_temp):
                Crops_temp.append(Analyse_results[ind + i][2])
            ind += c.gran_temp + 1

            a[0][0].plot(c.temps, Crops_temp, label=str(crop.name))
            a[0][0].set_xlabel('Température en °C')
            a[0][0].set_ylabel('TWSO en kg/ha')
            a[0][0].legend()

            for i in range(c.gran_irrad):
                Crops_irrad.append(Analyse_results[ind + i][2])
            ind += c.gran_irrad + 1

            a[0][1].plot(c.suns, Crops_irrad, label=str(crop.name))
            a[0][1].set_xlabel('Irradiation en kJ/m2/day')
            a[0][1].set_ylabel('TWSO en kg/ha')
            a[0][1].legend()

            for i in range(c.gran_rain):
                Crops_rain.append(Analyse_results[ind + i][2])
            ind += c.gran_rain + 1

            a[1][0].plot(c.rains, Crops_rain, label=str(crop.name))
            a[1][0].set_xlabel('Rain en mm')
            a[1][0].set_ylabel('TWSO en kg/ha')
            a[1][0].legend()

            for i in range(c.gran_wind):
                Crops_wind.append(Analyse_results[ind + i][2])
            ind += c.gran_wind + 1

            a[1][1].plot(c.winds, Crops_wind, label=str(crop.name))
            a[1][1].set_xlabel('Wind en m/s')
            a[1][1].set_ylabel('TWSO en kg/ha')
            a[1][1].legend()

        fig.suptitle(f"Evolution de la valeur moyenne du TWSO pour le sol {soil}")
        fig.savefig(f"Analyse_Results_dim_{soil}.png", bbox_inches='tight', dpi=150)
        plt.show()


def analyse_donnees_poussees_par_plante():
    for soil in c.soils:
        start_timer_sim = time.perf_counter()
        for crop in c.crops:
            results_dir_now = os.path.join(dir_analyze, f"{soil}_{crop.name}")
            Data_raw = Read_csv_into_Data(results_dir_now, 'Data.csv')

            print(soil)
            print(crop.name)
            print(c.suns, c.winds, c.rains, c.temps)

            simu_result =[['Irradiation','Temperature','Wind','Rain','TWSO_harvest','Harvest_Time','Lai_Integration']]
            for irrad in c.suns:
                start_timer_sim = time.perf_counter()
                for temperature in c.temps:
                    for wind in c.winds:
                        for rain in c.rains:
                            c.weather_config_dict['irrad'] = irrad
                            c.weather_config_dict['tmin'] = temperature
                            c.weather_config_dict['tmax'] = temperature
                            c.weather_config_dict['wind'] = wind
                            c.weather_config_dict['rain'] = rain
                            # modify weather file accordingly
                            filename_plant = f"irr_{irrad / 1000:.0f}_temp_{temperature:.1f}_rain_{rain:.1f}_wind_{wind:.1f}.csv"

                            Data_plante = Read_csv_into_Data(results_dir_now, filename_plant)
                            lai_index, twso_index = 2, 4
                            twso_max, harvest_time = 0, 0
                            for i in range(len(Data_plante) - 1):
                                if float(Data_plante[i + 1][twso_index]) > twso_max:
                                    twso_max = float(Data_plante[i + 1][twso_index])
                                    harvest_time = i + 1

                            int_lai = 0
                            for i in range(harvest_time):
                                int_lai += float(Data_plante[i + 1][lai_index])
                            simu_result.append([irrad, temperature, wind, rain, twso_max, harvest_time, int_lai])
            Write_csv_from_Data("Data_lai.csv", results_dir_now, simu_result)
            end_timer_sim = time.perf_counter()
            print(f"Simulation time is {(end_timer_sim - start_timer_sim) / 1:.1f} for  irrad{irrad}")

            # filename_plant = "irr_4_temp_6.7_rain_8.3_wind_0.0.csv"
            # Data_plante = Read_csv_into_Data(results_dir_now, filename_plant)
            #
            # print(Data_plante)
            # print(len(Data_plante))
            # lai_index, twso_index = 2, 4
            # twso_max, harvest_time = 0, 0
            # for i in range(len(Data_plante)-1):
            #     print(float(Data_plante[i + 1][twso_index]))
            #     if float(Data_plante[i+1][twso_index]) > twso_max:
            #         twso_max = float(Data_plante[i+1][twso_index])
            #         harvest_time = i+1
            #
            # int_lai = 0
            # for i in range(harvest_time):
            #     int_lai += float(Data_plante[i+1][lai_index])
            #
            # print(f"Harvest time is {harvest_time}, twso is {twso_max}, int_lai is {int_lai}")

#analyse_donnees_poussees_par_plante()
