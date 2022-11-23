# -*- coding: utf-8 -*-

import sys, os
sys.path.insert(1, '/home/user/Documents/imag/Manintec/Jaya/code/pcse')
import matplotlib
matplotlib.style.use("ggplot")
import matplotlib.pyplot as plt
import pandas as pd
import datetime,yaml

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

crop_name = 'mungbean'
variety_name = 'Mungbean_VanHeemst_1988'
start_date = datetime.datetime(2006, 1, 1, 0, 0)
end_date = datetime.datetime(2007, 1, 1, 0, 0)

weather_config_dict={'irrad': 10000.,
                     'tmin': 6.4,
                     'tmax': 15.,
                     'vap': 1.1,
                     'wind': 2.8,
                     'rain': 2.4,
                     'snowdepth': -999}


agro_dict = {'Version': 1.0,
             'AgroManagement': [{datetime.date(2006, 1, 1): {'CropCalendar': {'crop_name': crop_name,
                 'variety_name': variety_name,
                 'crop_start_date': datetime.date(2006, 4, 5),
                 'crop_start_type': 'emergence',
                 'crop_end_date': datetime.date(2006, 10, 20),
                 'crop_end_type': 'harvest',
                 'max_duration': 300},
                'TimedEvents': None,
                'StateEvents': None}}]}


def get_wofost_parameter_set():
    yaml_repo = os.path.join(data_dir, 'yaml')
    cropd = YAMLCropDataProvider(yaml_repo)
    #print(cropd)
    cropd.get_crops_varieties()
    cropd.set_active_crop(crop_name, variety_name)
    #print(cropd)
    
    soilfile = os.path.join(data_dir, 'soil', 'ec3.soil')
    soild = CABOFileReader(soilfile)
    sited = WOFOST72SiteDataProvider(WAV=10, CO2=360)
    #print(sited)
    parameters = ParameterProvider(cropdata=cropd, soildata=soild, sitedata=sited)
    return parameters

# Agromanagement

def prepare_agromanagement():
    agromanagement_file = os.path.join(data_dir, 'agro', 'sugarbeet_calendar.agro')
    with open(agromanagement_file, 'w') as file:
        file.flush()
        yaml.dump(agro_dict, file)
    
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
    
    longueur_restante_au_debut = int((row_end - row_start - (end_date - start_date).days)/2)
    excel_start_datetime = start_date - datetime.timedelta(days=longueur_restante_au_debut)
    
    # On change le df comme il faut
    for i in range(0, row_end-row_start+1):
        current_row_index = row_start+i
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


if __name__=='__main__':
    parameters = get_wofost_parameter_set()
    agromanagement = prepare_agromanagement()
    irrad_list = list()
    twso_max_list = list()
    for i in range(10):
        new_irrad = float(4000+i*2500)
        irrad_list.append(new_irrad)
        # modify weather_config_file
        weather_config_dict['irrad'] = new_irrad
        # modify weather file accordingly
        tmp_weatherfile = prepare_fictional_weather_file()
        df_results = get_result_of_wofost_run(parameters, tmp_weatherfile, agromanagement)
        result_name = os.path.join(results_dir, f"TWSO_irrad_{new_irrad}.png")
        save_TWSO(df_results,result_name,"TWSO : Total dry weight of living storage organs (kg ha-1)")
        twso_max_list.append(df_results["TWSO"].max())
    

    result_name = os.path.join(results_dir, "TWSO_en_fonction_de_irrad.png")
    fig, ax = plt.subplots()
    ax.plot(irrad_list, twso_max_list, 'g-')
    ax.set_title("TWSO (kg ha-1) en fonction de l'irradiation (kJ/m2/day)")
    plt.savefig(result_name)