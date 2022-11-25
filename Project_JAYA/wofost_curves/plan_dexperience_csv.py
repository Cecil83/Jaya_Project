#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, os
from config.pcse_path import pcse_path
sys.path.insert(1, pcse_path)
import matplotlib
#matplotlib.style.use("ggplot")
import matplotlib.pyplot as plt
import pandas as pd
import datetime,yaml
import csv

import config.config as c

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
print("PCSE version: %s" %  pcse.__version__)

# CONFIG

#crop_name = 'mungbean'
#variety_name = 'Mungbean_VanHeemst_1988'
crop_name = 'fababean'
variety_name = 'Faba_bean_801'
start_date = datetime.datetime(2006, 1, 1, 0, 0)
end_date = datetime.datetime(2007, 1, 1, 0, 0)

variable_meaning_dict={
    'TWSO': 'Total dry weight of living storage organs (kg ha-1)',
    'LAI': 'Leaf area index: (leaf area)/(soil area) (ha•ha-1)',
    'DVS': 'development stage of crop (-)',
    'TAGP':'total above ground production (dead and living plant organs) (kg ha-1)',
    'TWLV': 'total dry weight of leaves (dead and living) (kg ha-1)',
    'TWST': 'total dry weight of stems (dead and living) (kg ha-1)',
    'TWRT': 'total dry weight of roots (dead and living) (kg ha-1)',
    'TRA': 'transpiration rate (mm d-1)',
    'RD': 'depth of actual root zone (cm)',
    'SM': 'soil moisture content in actual root zone (cm-3(water) / (cm-3(soil))',
    'WWLOW': 'unknow',
}


def get_wofost_parameter_set():
    yaml_repo = os.path.join(data_dir, 'yaml')
    cropd = YAMLCropDataProvider(yaml_repo)
    #print(cropd)
    cropd.get_crops_varieties()
    cropd.set_active_crop(c.crop.name, c.crop.variety)
    #print(cropd)

    soilfile = os.path.join(data_dir, 'soil', 'ec3.soil')
    soild = CABOFileReader(soilfile)
    sited = WOFOST72SiteDataProvider(WAV=10, CO2=360)
    #print(sited)
    parameters = ParameterProvider(cropdata=cropd, soildata=soild, sitedata=sited)
    return parameters

# Agromanagement

def prepare_agromanagement(crop):
    # Prepare le fichier agromanagement avec la bonne culture
    agromanagement_file = os.path.join(data_dir, 'agro', 'sugarbeet_calendar.agro')
    with open(agromanagement_file, 'w') as file:
        file.flush()
        yaml.dump(c.agro_dict, file)
    
    agromanagement = YAMLAgroManagementReader(agromanagement_file)
    #print(agromanagement)
    return agromanagement

def prepare_fictional_weather_file():
    weatherfile = os.path.join(data_dir, 'meteo', 'nl1.xlsx')
    tmp_weatherfile = os.path.join(data_dir, 'meteo', 'nl1_temp.xlsx')

    # on modifie le df

    df = pd.read_excel(weatherfile)
    row_start = 11
    row_end = df.shape[0]-1
    
    longueur_restante_au_debut = int((row_end - row_start - (c.end_date - c.start_date).days)/2)
    excel_start_datetime = c.start_date - datetime.timedelta(days=longueur_restante_au_debut)
    
    # On change le df comme il faut
    for i in range(0, row_end-row_start+1):
        current_row_index = row_start+i
        # change datetime
        df.iat[current_row_index, 0] = excel_start_datetime + datetime.timedelta(days=i)
        # irradiation
        df.iat[current_row_index, 1] = c.weather_config_dict['irrad']
        # tmin
        df.iat[current_row_index, 2] = c.weather_config_dict['tmin']
        # tmax
        df.iat[current_row_index, 3] = c.weather_config_dict['tmax']
        # vap
        df.iat[current_row_index, 4] = c.weather_config_dict['vap']
        # wind
        df.iat[current_row_index, 5] = c.weather_config_dict['wind']
        # rain
        df.iat[current_row_index, 6] = c.weather_config_dict['rain']
        # snowdepth
        df.iat[current_row_index, 7] = c.weather_config_dict['snowdepth']
    
    
    writer = pd.ExcelWriter(tmp_weatherfile,
                            engine='xlsxwriter',
                            datetime_format='mm/d/yyyy')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index = False)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    return tmp_weatherfile

def get_result_of_wofost_run(parameters, weather, agromanagement):
    wdp = ExcelWeatherDataProvider(weather)
    #print(wdp)

    wofsim = Wofost72_PP(parameters, wdp, agromanagement)


    wofsim.run_till_terminate()
    df_results = pd.DataFrame(wofsim.get_output())
    df_results = df_results.set_index("day")
    df_results.tail()
    return df_results

def print_curves(df_results):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,10))
    for var, ax in zip(["DVS", "TAGP", "LAI", "TWSO"], axes.flatten()):
        ax.plot_date(df_results.index, df_results[var], 'b-')
        ax.set_title(var)
    fig.autofmt_xdate()

def print_var(var_type, df_results):
    fig, ax = plt.subplots()
    ax.plot_date(df_results.index, df_results[var_type], 'k-')
    ax.set_title(f"{var_type} : {variable_meaning_dict[var_type]}")
    plt.show()

def save_var(var_type, df_results, filename):
    fig, ax = plt.subplots()
    ax.plot_date(df_results.index, df_results[var_type], 'k-')
    ax.set_title(f"{var_type} : {variable_meaning_dict[var_type]}")
    plt.savefig(filename)


def Write_csv_from_Data (filename,path, Data_W):
    os.chdir(path)
    f = open(filename, 'w')
    # create the csv writer
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    # writer.writerow(header)
    for row in Data_W:
        writer.writerow(row)
    f.close()

#def write_to_excel(df_results, )

if __name__=='__main__':
    parameters = get_wofost_parameter_set()
    agromanagement = prepare_agromanagement()
    irrad_list = list()
    twso_max_list = list()
    results_dir_now = os.path.join(results_dir, f"TWSO_{crop_name}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    os.mkdir(results_dir_now)
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig_dict, ax_dict = dict(), dict()
    for key in variable_meaning_dict.keys():
        fig_dict[key], ax_dict[key] = plt.subplots()
    for i in range(10):
        new_irrad = float(4000+i*2500)

        irrad_list.append(new_irrad)
        # modify weather_config_file
        c.weather_config_dict['irrad'] = new_irrad
        # modify weather file accordingly
        tmp_weatherfile = prepare_fictional_weather_file()
        df_results = get_result_of_wofost_run(parameters, tmp_weatherfile, agromanagement)
        result_name = os.path.join(results_dir_now, f"TWSO_{crop_name}_irrad_{new_irrad}.png")
        #save_var('TWSO', df_results, result_name)
        #save_var('LAI', df_results, os.path.join(results_dir_now, f"LAI_{crop_name}_irrad_{new_irrad}.png"))

        twso_max_list.append(df_results["TWSO"].max())
        df_results.to_csv(os.path.join(results_dir_now,f"TWSO_{crop_name}_irrad_{new_irrad}.csv"))

        for key in variable_meaning_dict.keys():
            fig = ax_dict[key].plot(df_results.index, df_results[key], '-', label=f"{new_irrad / 1000:.1f}")
            ax_dict[key].legend(title=f"Irradiations in MJ/m2/day ")
            ax_dict[key].set_title(f"{key} : {variable_meaning_dict[key]}")
            fig_dict[key].savefig(os.path.join(results_dir_now, f"{key}_irrad_fct_temps.png"))


        # ax1.plot(df_results.index, df_results[key], '-', label=f"{new_irrad/1000:.1f}")
        # ax1.legend()
        # fig1.savefig(os.path.join(results_dir_now, f"{key}_irrad_fct_temps.png"))
        #
        # ax2.plot(df_results.index, df_results['LAI'], '-', label=f"{new_irrad/1000:.1f}")
        # ax2.legend()
        # fig2.savefig(os.path.join(results_dir_now, f"LAI_irrad_fct_temps.png"))
        #

    result_name = os.path.join(results_dir_now, f"TWSO_{crop_name}_en_fonction_de_irrad.png")
    fig, ax = plt.subplots()
    ax.plot(irrad_list, twso_max_list, 'g-')
    ax.set_title("TWSO (kg ha-1) en fonction de l'irradiation (kJ/m2/day)")
    plt.savefig(result_name)

    Data_results, header = [],[]

    Data_results.append([key for key in c.weather_config_dict.keys()])
    Data_results.append([c.weather_config_dict[key] for key in c.weather_config_dict.keys()])

    Data_results.append(('Irrad_value','TWSO_harvest_value'))
    for i in range(len(irrad_list)):
        Data_results.append((irrad_list[i], twso_max_list[i]))

    Write_csv_from_Data(f"Results_{crop_name}_irrad.csv", results_dir_now, Data_results)

