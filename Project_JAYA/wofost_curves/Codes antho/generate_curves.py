# -*- coding: utf-8 -*-

import sys, os
from input_read import *
from functions_garden import *

sys.path.insert(1, 'pcse')
import matplotlib

matplotlib.use
import matplotlib.pyplot as plt

plt.style.use('ggplot')
import matplotlib.pyplot as plt
import pandas as pd
import datetime, yaml

from plante import *
from potager import *

import csv

import pcse
from pcse.fileinput import CABOFileReader
from pcse.fileinput import YAMLCropDataProvider
from pcse.util import WOFOST72SiteDataProvider
from pcse.base import ParameterProvider
from pcse.fileinput import YAMLAgroManagementReader
from pcse.fileinput import ExcelWeatherDataProvider
from pcse.models import Wofost72_WLP_FD, Wofost72_PP

data_dir = os.path.join(os.getcwd(), 'data')
results_dir = os.path.join(os.getcwd(), 'results')
print("python version: %s " % sys.version)
print("PCSE version: %s" % pcse.__version__)

# CONFIG

crop_name = 'mungbean'
#crop_name = 'fababean'
variety_name = 'Mungbean_VanHeemst_1988'
#variety_name = 'Faba_bean_801'
start_date = datetime.datetime(2006, 1, 1, 0, 0)
end_date = datetime.datetime(2007, 1, 1, 0, 0)

weather_config_dict = {'irrad': 10000.,
                       'tmin': 6.4,
                       'tmax': 15.,
                       'vap': 1.1,
                       'wind': 2.8,
                       'rain': 2.4,
                       'snowdepth': -999}

agro_dict = {'Version': 1.0,
             'AgroManagement': [{datetime.date(2006, 1, 1): {'CropCalendar': {'crop_name': crop_name,
                                                                              'variety_name': variety_name,
                                                                              'crop_start_date': datetime.date(2006, 4,
                                                                                                               5),
                                                                              'crop_start_type': 'emergence',
                                                                              'crop_end_date': datetime.date(2006, 10,
                                                                                                             20),
                                                                              'crop_end_type': 'harvest',
                                                                              'max_duration': 300},
                                                             'TimedEvents': None,
                                                             'StateEvents': None}}]}


def get_wofost_parameter_set():
    yaml_repo = os.path.join(data_dir, 'yaml')
    cropd = YAMLCropDataProvider(yaml_repo)
    # print(cropd)
    cropd.get_crops_varieties()
    cropd.set_active_crop(crop_name, variety_name)
    # print(cropd)

    soilfile = os.path.join(data_dir, 'soil', 'ec3.soil')
    soild = CABOFileReader(soilfile)
    sited = WOFOST72SiteDataProvider(WAV=10, CO2=360)
    # print(sited)
    parameters = ParameterProvider(cropdata=cropd, soildata=soild, sitedata=sited)
    return parameters


# Agromanagement

def prepare_agromanagement():
    agromanagement_file = os.path.join(data_dir, 'agro', 'sugarbeet_calendar.agro')
    with open(agromanagement_file, 'w') as file:
        file.flush()
        yaml.dump(agro_dict, file)

    agromanagement = YAMLAgroManagementReader(agromanagement_file)
    # print(agromanagement)
    return agromanagement

def isInt(n):
    if n % 1 == 0.0:
        return 1
    else:
        return 0
def get_data_in_csv_by_index(plant):
    index = plant.sun * 10**3 + plant.temp * 10**2 + plant.wind * 10**1 + plant.rain * 10**0
    print(f"index is {index}")
    # if float(index) < 0 or float(index) > 10 :
    #     print("Please enter number between 0 and 10 :")
    #     return 0

    # Get in the right directory
    list_data = []
    # reading csv file to get previous values
    # csvfile = "./TWSO_" + plant + "_irrad.csv"
    # print('path is ', csvfile)
    sol = 'ec1.soil_'
    csvfile = '../results/10gran_3crop_1soil_2022_12_06_22_05_51/'+ sol + plant.type_plant + '/Data.csv'
    print('path is ', csvfile)

    print("\n La source est : " + csvfile)

    with open(csvfile, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
                list_data.append(row)

    twso_val = float(list_data[int(index)][4])
    return twso_val

    #index = float(index)
    #print(index)
    # if isInt(index):
    #     index = int(index)
    #     x = str(list_data[int(index)]).split("'")
    #     #print(x[1])
    #     y = str(x[4]).split(",")
    #     return float(y[4])
    # else:
    #     float_index = index
    #     index = int(index)
    #     #result_1
    #     x = str(list_data[int(index)]).split("'")
    #     #print(x[1])
    #     result_1 = str(x[1]).split(",")
    #
    #     #result_2
    #     x = str(list_data[int(index + 1)]).split("'")
    #     #print(x[1])
    #     result_2 = str(x[1]).split(",")
    #
    #     coeff = float_index % 1
    #     #print(coeff)
    #     dist = (float(result_2[0]) - float(result_1[0])) * coeff
    #
    #     new_x = float(result_1[0]) + dist
    #     #print(new_x)
    #     a = ((float(result_2[1]) - float(result_1[1])) / (float(result_2[0]) - float(result_1[0])))
    #     b = (float(result_2[1])) - (a*(float(result_2[0])))
    #
    #     return (a*new_x) + b

def get_max_twso_sun(plant):
    list_data = []
    # reading csv file to get previous values
    csvfile = "./TWSO_" + plant + "_irrad.csv"
    #print(csvfile)
    with open(csvfile, 'r') as file:
        csvreader = csv.reader(file, delimiter='\n')
        for row in csvreader:
            if len(row) != 0:
                #print(row)
                list_data.append(row)

    x = str(list_data[9]).split("'")
    #print(x[1])
    y = str(x[1]).split(",")
    return float(y[1])

def calc_productivity_monocrop(plant, twso):
    max_twso = get_max_twso_sun(plant)
    return (twso * 100) / max_twso

def prepare_fictional_weather_file():
    weatherfile = os.path.join(data_dir, 'meteo', 'nl1.xlsx')
    tmp_weatherfile = os.path.join(data_dir, 'meteo', 'nl1_temp.xlsx')

    # on modifie le df

    df = pd.read_excel(weatherfile)
    row_start = 11
    row_end = df.shape[0] - 1

    longueur_restante_au_debut = int((row_end - row_start - (end_date - start_date).days) / 2)
    excel_start_datetime = start_date - datetime.timedelta(days=longueur_restante_au_debut)

    # On change le df comme il faut
    for i in range(0, row_end - row_start + 1):
        current_row_index = row_start + i
        # change datetime
        df.iat[current_row_index, 0] = excel_start_datetime + datetime.timedelta(days=i)
        # irradiation
        df.iat[current_row_index, 1] = weather_config_dict['irrad']
        # tmin
        df.iat[current_row_index, 2] = weather_config_dict['tmin']
        # tmax
        df.iat[current_row_index, 3] = weather_config_dict['tmax']
        # vap
        df.iat[current_row_index, 4] = weather_config_dict['vap']
        # wind
        df.iat[current_row_index, 5] = weather_config_dict['wind']
        # rain
        df.iat[current_row_index, 6] = weather_config_dict['rain']
        # snowdepth
        df.iat[current_row_index, 7] = weather_config_dict['snowdepth']

    writer = pd.ExcelWriter(tmp_weatherfile,
                            datetime_format='mm/d/yyyy')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    return tmp_weatherfile


def get_result_of_wofost_run(parameters, weather, agromanagement):
    wdp = ExcelWeatherDataProvider(weather)
    # print(wdp)

    wofsim = Wofost72_PP(parameters, wdp, agromanagement)

    wofsim.run_till_terminate()
    df_results = pd.DataFrame(wofsim.get_output())
    df_results = df_results.set_index("day")
    df_results.tail()
    return df_results


def print_curves(df_results):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
    for var, ax in zip(["DVS", "TAGP", "LAI", "TWSO"], axes.flatten()):
        ax.plot_date(df_results.index, df_results[var], 'b-')
        ax.set_title(var)
    fig.autofmt_xdate()


def print_TWSO(df_results):
    fig, ax = plt.subplots()
    ax.plot_date(df_results.index, df_results["TWSO"], 'k-')
    ax.set_title("TWSO : Total dry weight of living storage organs (kg ha-1)")
    plt.show()

def save_TWSO(df_results, filename, title):
    fig, ax = plt.subplots()
    ax.plot_date(df_results.index, df_results["TWSO"], 'k-')
    ax.set_title(title)
    plt.savefig(filename)



if __name__ == '__main__':

    """
    with open ('TWSO_mungbean_irrad.csv', 'w') as file:
        writer = csv.writer(file)

        parameters = get_wofost_parameter_set()
        agromanagement = prepare_agromanagement()
        irrad_list = list()
        twso_max_list = list()
        for i in range(10):
            new_irrad = float(4000 + i * 2500)
            irrad_list.append(new_irrad)
            # modify weather_config_file
            weather_config_dict['irrad'] = new_irrad
            # modify weather file accordingly
            tmp_weatherfile = prepare_fictional_weather_file()
            df_results = get_result_of_wofost_run(parameters, tmp_weatherfile, agromanagement)
            result_name = os.path.join(results_dir, f"TWSO_irrad_{new_irrad}.png")
            save_TWSO(df_results, result_name, "TWSO : Total dry weight of living storage organs (kg ha-1)")
            twso_max = df_results["TWSO"].max()
            #print(twso_max)
            twso_max_list.append(twso_max)

            data = [new_irrad, twso_max]
            writer.writerow(data)

    file.close()
    """

    #sun = input("Taux de soleil : ")

    """Plot
    result_name = os.path.join(results_dir, "TWSO_en_fonction_de_irrad.png")
    fig, ax = plt.subplots()
    ax.plot(irrad_list, twso_max_list, 'g-')
    ax.set_title("TWSO (kg ha-1) en fonction de l'irradiation (kJ/m2/day)")
    plt.savefig(result_name)
    """
    path = './'
    filename = 'test_input'
    Data = Read_csv_into_Data(path, filename + '.csv')

    header_potager = Data[0]
    header_plantes = Data[2]

    dim_x_potager = float(Data[1][0])
    dim_y_potager = float(Data[1][1])
    eau_potager = float(Data[1][2])
    temp_potager = float(Data[1][3])
    soleil_potager = float(Data[1][4])
    wind_potager = float(Data[1][5])

    nb_plantes = len(Data) - 3

    Nom_plantes, X_plantes, Y_plantes, Rayons, Color_plantes = [], [], [], [], []

    for i in range(nb_plantes):
        Nom_plantes.append((Data[i + 3][0]))
        X_plantes.append(assess_X_coord(int(Data[i + 3][1]), dim_x_potager))
        Y_plantes.append(assess_Y_coord(int(Data[i + 3][2]), dim_y_potager))
        Rayons.append((int(Data[i + 3][3])))
        Color_plantes.append((Data[i + 3][4]))

    #list_vegetables = what_is_in_my_garden('test_input.csv')
    my_list_plant = create_list_plant("test_input.csv")
    which_plant_are_in_my_garden(my_list_plant)
    index = 0
    for plante in my_list_plant:
        plante.sun = int(soleil_potager)
        plante.temp = int(temp_potager)
        plante.wind = int(wind_potager)
        plante.rain = int(eau_potager)

        twso = get_data_in_csv_by_index(plante)
        plante.twso = twso
        print("TWSO = " + str(twso))

        Noms_plantes_unique, index_unique = count_different_plants(Nom_plantes, nb_plantes)
        #print(Noms_plantes_unique, index_unique)


        productivity = plante.calc_productivity(twso)

    potager = Potager(my_list_plant)
    productivity_garden = potager.calc_productivity()
    twso_total = potager.calc_twso_total()
    visual(nb_plantes, X_plantes, Y_plantes, Rayons, Color_plantes, index_unique, Noms_plantes_unique, dim_x_potager,
               dim_y_potager, Data, productivity_garden, twso_total, filename)


    #Test


