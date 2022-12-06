#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, os, csv, shutil
from config.pcse_path import pcse_path
sys.path.insert(1, pcse_path)
import matplotlib.pyplot as plt
import pandas as pd
import datetime,yaml, time

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


def get_wofost_parameter_set(crop,soil):
    yaml_repo = os.path.join(data_dir, 'yaml')
    cropd = YAMLCropDataProvider(yaml_repo)
    cropd.set_active_crop(crop.name, crop.variety)

    soilfile = os.path.join(data_dir, 'soil', soil)
    soild = CABOFileReader(soilfile)
    sited = c.sited
    parameters = ParameterProvider(cropdata=cropd, soildata=soild, sitedata=sited)
    return parameters

# Agromanagement

def prepare_agromanagement(crop):
    # Prepare le fichier agromanagement avec la bonne culture
    agromanagement_file = os.path.join(data_dir, 'agro', 'sugarbeet_calendar.agro')
    
    c.agro_dict['AgroManagement'][0][c.start_date]['CropCalendar']['crop_name'] = crop.name
    c.agro_dict['AgroManagement'][0][c.start_date]['CropCalendar']['variety_name'] = crop.variety
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


    #wofsim = Wofost72_PP(parameters, wdp, agromanagement)
    wofsim = Wofost72_WLP_FD(parameters, wdp, agromanagement)
    

    wofsim.run_till_terminate()
    df_results = pd.DataFrame(wofsim.get_output())
    df_results = df_results.set_index("day")
    df_results.tail()
    return df_results

def Write_csv_from_Data(filename, path, Data_W):
    os.chdir(path)
    f = open(filename, 'w')
    # create the csv writer
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    # writer.writerow(header)
    for row in Data_W:
        writer.writerow(row)
    f.close()
def start_runs_for_weather_parameters(parameters,agro,path):
    simu_result = [['Irradiation', 'Temperature', 'Wind', 'Rain', 'TWSO_harvest']]
    for irrad in c.suns:
        start_timer_sim = time.perf_counter()
        for temperature in c.temps:
            print(f"Température = {temperature}")
            for wind in c.winds:
                print(f"Wind = {wind}")
                for rain in c.rains:
                    c.weather_config_dict['irrad'] = irrad
                    c.weather_config_dict['tmin'] = temperature
                    c.weather_config_dict['tmax'] = temperature
                    c.weather_config_dict['wind'] = wind
                    c.weather_config_dict['rain'] = rain
                    # modify weather file accordingly
                    tmp_weatherfile = prepare_fictional_weather_file()
                    df_results = get_result_of_wofost_run(parameters, tmp_weatherfile, agro)
                    filename = f"irr_{irrad / 1000:.0f}_temp_{temperature:.1f}_rain_{rain:.1f}_wind_{wind:.1f}.csv"
                    df_results.to_csv(os.path.join(path,filename))

                    simu_result.append([irrad, temperature, wind, rain, df_results["TWSO"].max()])
        end_timer_sim = time.perf_counter()
        print(f"Simulation time is {(end_timer_sim - start_timer_sim) / 1:.1f} for  irrad{irrad}")
    Write_csv_from_Data("Data.csv", results_dir_now, simu_result)

if __name__=='__main__':
    start_timer = time.perf_counter()
    new_res_dir = os.path.join(results_dir,f"{c.gran_irrad}gran_{len(c.crops)}crop_{len(c.soils)}soil_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    os.mkdir(new_res_dir)
    shutil.copy(os.path.join(os.getcwd(), 'config/config.py'), os.path.join(new_res_dir, 'config_sim.py'))

    for soil in c.soils:
        print(f"Soil = {soil}")
        for crop in c.crops:
            print(f"crop = {crop}")
            parameters = get_wofost_parameter_set(crop, soil)
            agromanagement = prepare_agromanagement(crop)
            results_dir_now = os.path.join(new_res_dir, f"{soil}_{crop.name}")
            os.mkdir(results_dir_now)
            start_runs_for_weather_parameters(parameters, agromanagement, results_dir_now)

    end_timer = time.perf_counter()
    print(f"Simulation time is {(end_timer - start_timer) / 1:.1f}")



    

