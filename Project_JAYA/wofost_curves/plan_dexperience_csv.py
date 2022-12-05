#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, os
from config.pcse_path import pcse_path
sys.path.insert(1, pcse_path)
import matplotlib.pyplot as plt
import pandas as pd
import datetime,yaml

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

def start_runs_for_weather_parameters(parameters,agro,path):
    for irrad in c.suns:
        for temperature in c.temps:
            for wind in c.winds:
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

if __name__=='__main__':
    new_res_dir = os.path.join(results_dir,f"{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
    os.mkdir(new_res_dir)
    for soil in c.soils:
        for crop in c.crops:
            parameters = get_wofost_parameter_set(crop, soil)
            agromanagement = prepare_agromanagement(crop)
            results_dir_now = os.path.join(new_res_dir, f"{soil}_{crop.name}")
            os.mkdir(results_dir_now)
            start_runs_for_weather_parameters(parameters, agromanagement, results_dir_now)
            
    

