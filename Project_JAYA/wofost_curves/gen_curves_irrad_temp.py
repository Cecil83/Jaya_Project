# -*- coding: utf-8 -*-

import sys, os

# sys.path.insert(1, '/home/user/Documents/imag/Manintec/Jaya/code/pcse')
# Gaétan chemin
sys.path.insert(1, '/Users/gaeta/PycharmProjects/Jaya/PCSE/pcse')
import matplotlib
# matplotlib.style.use("ggplot")
import matplotlib.pyplot as plt
import pandas as pd
import datetime, yaml, time
import csv

import pcse
from pcse.fileinput import CABOFileReader
from pcse.fileinput import YAMLCropDataProvider
from pcse.util import WOFOST72SiteDataProvider
from pcse.base import ParameterProvider
from pcse.fileinput import YAMLAgroManagementReader
from pcse.fileinput import ExcelWeatherDataProvider
from pcse.models import Wofost72_WLP_FD, Wofost72_PP

start_timer = time.perf_counter()
data_dir = os.path.join(os.getcwd(), 'data')
results_dir = os.path.join(os.getcwd(), 'results')
print("python version: %s " % sys.version)
print("PCSE version: %s" % pcse.__version__)

# CONFIG

crop_name = 'mungbean'
variety_name = 'Mungbean_VanHeemst_1988'
#crop_name = 'fababean'
#variety_name = 'Faba_bean_801'
start_date = datetime.datetime(2006, 1, 1, 0, 0)
end_date = datetime.datetime(2007, 1, 1, 0, 0)

variable_meaning_dict = {
    'TWSO': 'Total dry weight of living storage organs (kg ha-1)',
    'LAI': 'Leaf area index: (leaf area)/(soil area) (ha•ha-1)',
    'DVS': 'development stage of crop (-)',
    'TAGP': 'total above ground production (dead and living plant organs) (kg ha-1)',
    'TWLV': 'total dry weight of leaves (dead and living) (kg ha-1)',
    'TWST': 'total dry weight of stems (dead and living) (kg ha-1)',
    'TWRT': 'total dry weight of roots (dead and living) (kg ha-1)',
    'TRA': 'transpiration rate (mm d-1)',
    'RD': 'depth of actual root zone (cm)',
    'SM': 'soil moisture content in actual root zone (cm-3(water) / (cm-3(soil))',
    'WWLOW': 'unknow',
}

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
                            engine='xlsxwriter',
                            datetime_format='mm/d/yyyy')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    return tmp_weatherfile


def get_result_of_wofost_run(parameters, weather, agromanagement):
    wdp = ExcelWeatherDataProvider(weather)
    # print(wdp)

    #wofsim = Wofost72_PP(parameters, wdp, agromanagement)
    wofsim = Wofost72_WLP_FD(parameters, wdp, agromanagement)

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


def Write_csv_from_Data(filename, path, Data_W):
    os.chdir(path)
    f = open(filename, 'w')
    # create the csv writer
    writer = csv.writer(f, delimiter=',', lineterminator='\n')
    # writer.writerow(header)
    for row in Data_W:
        writer.writerow(row)
    f.close()

# def write_to_excel(df_results, )

if __name__ == '__main__':
    parameters = get_wofost_parameter_set()
    agromanagement = prepare_agromanagement()
    irrad_list = list()
    twso_max_list = list()
    temp_list= list()

    # fig1, ax1 = plt.subplots()
    # fig2, ax2 = plt.subplots()
    # fig_dict, ax_dict = dict(), dict()
    # for key in variable_meaning_dict.keys():
    #     fig_dict[key], ax_dict[key] = plt.subplots()
    dim = 10
    results_dir_now = os.path.join(results_dir,
                                   f"TWSO_{crop_name}_IRRAD_TEMP_dim{dim}{datetime.datetime.now().strftime('%m_%d_%H_%M_%S')}")
    os.mkdir(results_dir_now)
    irrad_min = 100
    irrad_max = 28000
    temp_min = -8.5
    temp_max = 26.9

    for i in range(dim):
        new_irrad = round(float(irrad_min + i * (irrad_max-irrad_min)/(dim - 1)),2)
        irrad_list.append(new_irrad)
        # modify weather_config_file
        weather_config_dict['irrad'] = new_irrad
        for j in range(dim):
            new_temp = round(float(temp_min + j * (temp_max - temp_min) / (dim - 1)), 2)
            temp_list.append(new_temp)
            weather_config_dict['tmin'] = new_temp
            weather_config_dict['tmax'] = new_temp

            # modify weather file accordingly
            tmp_weatherfile = prepare_fictional_weather_file()
            df_results = get_result_of_wofost_run(parameters, tmp_weatherfile, agromanagement)
            result_name = os.path.join(results_dir_now, f"TWSO_{crop_name}_irrad_{new_irrad}_temp{new_temp}.png")
            # save_var('TWSO', df_results, result_name)
            # save_var('LAI', df_results, os.path.join(results_dir_now, f"LAI_{crop_name}_irrad_{new_irrad}.png"))

            twso_max_list.append(df_results["TWSO"].max())
            df_results.to_csv(os.path.join(results_dir_now, f"TWSO_{crop_name}_irrad_{new_irrad}_temp{new_temp}.csv"))

            ###
            # for key in variable_meaning_dict.keys():
            #     fig = ax_dict[key].plot(df_results.index, df_results[key], '-', label=f"{new_irrad / 1000:.1f}")
            #     ax_dict[key].legend(title=f"Irradiations in MJ/m2/day ")
            #     ax_dict[key].set_title(f"{key} : {variable_meaning_dict[key]}")
            #     fig_dict[key].savefig(os.path.join(results_dir_now, f"{key}_irrad_fct_temps.png"))
            ###
            # ax1.plot(df_results.index, df_results[key], '-', label=f"{new_irrad/1000:.1f}")
            # ax1.legend()
            # fig1.savefig(os.path.join(results_dir_now, f"{key}_irrad_fct_temps.png"))
            #
            # ax2.plot(df_results.index, df_results['LAI'], '-', label=f"{new_irrad/1000:.1f}")
            # ax2.legend()
            # fig2.savefig(os.path.join(results_dir_now, f"LAI_irrad_fct_temps.png"))
            #
    temp_list=temp_list[:dim]
    # result_name = os.path.join(results_dir_now, f"TWSO_{crop_name}_en_fonction_de_irrad.png")
    # fig, ax = plt.subplots()
    # ax.plot(irrad_list, twso_max_list, 'g-')
    # ax.set_title("TWSO (kg ha-1) en fonction de l'irradiation (kJ/m2/day)")
    # plt.savefig(result_name)
    print(irrad_list)
    print(temp_list)
    print(twso_max_list)
    Data_results, header = [], []

    Data_results.append([key for key in weather_config_dict.keys()])
    Data_results.append([weather_config_dict[key] for key in weather_config_dict.keys()])

    Data_results.append(('Irrad_value', 'Temp_value', 'TWSO_harvest_value'))
    ind = 0
    for i in range(dim):
        for j in range(dim):
            Data_results.append((irrad_list[i], temp_list[j], twso_max_list[ind]))
            ind+=1

    Write_csv_from_Data(f"Results_{crop_name}_irrad_temp{new_temp}.csv", results_dir_now, Data_results)

    end_timer = time.perf_counter()
    print(f"Simulation time is {(end_timer-start_timer)/1:.1f}")

    analyze_temp = [('Température', 'Min', 'Moy', 'Max')]
    analyze_irrad = [('Irradiation', 'Min', 'Moy', 'Max')]

    for temp in temp_list:
        temp_min, temp_incr, temp_max = 7000, 0, 0
        for i in range(dim**2):
            if Data_results[i+3][1]==temp:
                twso_val = Data_results[i+3][2]
                if twso_val<temp_min:
                    temp_min=twso_val
                if twso_val>temp_max:
                    temp_max=twso_val
                temp_incr += twso_val
        analyze_temp.append((temp,temp_min, temp_incr/dim, temp_max))

    for irrad in irrad_list:
        irrad_min, irrad_incr, irrad_max = 7000, 0, 0
        for i in range(dim**2):
            if Data_results[i+3][0]==irrad:
                twso_val = Data_results[i+3][2]
                if twso_val<irrad_min:
                    irrad_min=twso_val
                if twso_val>irrad_max:
                    irrad_max=twso_val
                irrad_incr += twso_val
        analyze_irrad.append((irrad, irrad_min, irrad_incr/dim, irrad_max))

    print(analyze_irrad)
    print(analyze_temp)

    abs_max, index = 0, 0
    for i in range(dim**2):
        if Data_results[i+3][2]>abs_max:
            abs_max=Data_results[i+3][2]
            index = i+3

    print(f"TWSO max value is {abs_max} and was reach for temp = {Data_results[index][1]} and irrad = {Data_results[index][0]}")

    Analyse_results = analyze_temp
    for i in range(len(analyze_irrad)):
        Analyse_results.append(analyze_irrad[i])
    Analyse_results.append((f"TWSO max value is {abs_max} and was reach for temp = {Data_results[index][1]} and irrad = {Data_results[index][0]}"))
    Analyse_results.append((f"Simulation time is {(end_timer-start_timer)/1:.1f}"))
    Write_csv_from_Data(f"Analyse_Results_IRRAD_TEMP_dim{dim}.csv", results_dir_now, Analyse_results)