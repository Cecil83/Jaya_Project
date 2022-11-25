#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from collections import namedtuple

Crop = namedtuple('Crop', ['name', 'variety'])

# CROP CHOICE

"""
Choix de crops :
    sunflower, soybean, millet, barley, mungbean, obacco, rapeseed, roundnut,
    cotton, cowpea, chickpea, sugarbeet, fababean, sugarcane, potato, wheat, 
    pigeonpea, sorghum, cassava, maize, seed_onion, rice, sweetpotato
"""
# Soit itérer sur toutes les crops

one_crop=False
#one_crop=True

# Si one_crop=True
crop_name = 'fababean'

# CONFIG

start_date = datetime.date(2006, 1, 1)
end_date = datetime.date(2007, 1, 1)

# WEATHER
# Soleil
# Soit one_sun=True et une seule valeur d'ensoleillement "sun" est choisie, soit False
# et 10 valeurs sont prises en partant de sun_min et par step de sun_step

#one_sun=False
one_sun=True

sun_min = 4000.
sun_step = 2500.

sun = 10000.0


# Température
# Soit one_sun=True et une seule valeur d'ensoleillement "sun" est choisie, soit False
# et 10 valeurs sont prises en partant de sun_min et par step de sun_step

#one_temp=False
one_temp=True

temp_min = -8.5
temp_step = (26.9 + 8.5 )/ 9

temp = 18.


# SOIL


# Soit itérer sur tous les soils

one_soil=False
#one_soil=True

# Si one_soil=True
soil_name = 'ec3.soil'


##########################################################################
# FIN DU FICHIER CONFIG (La suite est faite pour s'exécuter par import du fichier)







# Soleil, température, eau, nutriment

crop_dict = {'sunflower': Crop(name='sunflower', variety='Sunflower_1101'),
             #'soybean': Crop(name='soybean', variety='Soybean_901'),
             #'millet': Crop(name='millet', variety='Millet_VanHeemst_1988'),
             #'barley': Crop(name='barley', variety='Spring_barley_301'),
             #'mungbean': Crop(name='mungbean', variety='Mungbean_VanHeemst_1988'),
             #'tobacco': Crop(name='tobacco', variety='Tobacco_VanHeemst_1988'),
             #'rapeseed': Crop(name='rapeseed', variety='Oilseed_rape_1001'),
             #'groundnut': Crop(name='groundnut', variety='Groundnut_VanHeemst_1988'),
             #'cotton': Crop(name='cotton', variety='Cotton_VanHeemst_1988'),
             #'cowpea': Crop(name='cowpea', variety='Cowpea_VanHeemst_1988'),
             #'chickpea': Crop(name='chickpea', variety='Chickpea_VanHeemst_1988'),
             #'sugarbeet': Crop(name='sugarbeet', variety='Sugarbeet_601'),
             'fababean': Crop(name='fababean', variety='Faba_bean_801'),
             #'sugarcane': Crop(name='sugarcane', variety='Sugarcane_VanHeemst_1988'),
             #'potato': Crop(name='potato', variety='Potato_701'),
             #'wheat': Crop(name='wheat', variety='Winter_wheat_101'),
             #'pigeonpea': Crop(name='pigeonpea', variety='Pigeonpea_VanHeemst_1988'),
             #'sorghum': Crop(name='sorghum', variety='Sorghum_VanHeemst_1988'),
             #'cassava': Crop(name='cassava', variety='Cassava_VanHeemst_1988'),
             'maize': Crop(name='maize', variety='Maize_VanHeemst_1988'),
             'seed_onion': Crop(name='seed_onion', variety='onion_agriadapt'),
             'rice': Crop(name='rice', variety='Rice_501'),
             'sweetpotato': Crop(name='sweetpotato', variety='Sweetpotato_VanHeemst_1988')}


# Crop

if one_crop:
    crops = [crop_dict[crop_name]]
else:
    crops = list(crop_dict.values())

# Soil

if one_soil:
    soils = [soil_name]
else:
    soils = ['ec1.soil', 'ec2.soil', 'ec3.soil']

# Soleil

if one_sun:
    suns = [sun]
else:
    suns = [sun_min + sun_step*float(i) for i in range(10)]

# Temperature

if one_temp:
    temps = [temp]
else:
    temps = [temp_min + temp_step*float(i) for i in range(10)]


# Reste à faire l'eau et les nutriments, et le site (soil profile etc )



##################################################################

# Ici, config de base qui sera modifiée par les scripts

# config

weather_config_dict={'irrad': 10000.,
                     'tmin': 6.4,
                     'tmax': 15.,
                     'vap': 1.1,
                     'wind': 2.8,
                     'rain': 2.4,
                     'snowdepth': -999}



# Agro File Config

agro_dict = {'Version': 1.0,
             'AgroManagement': [{start_date: {'CropCalendar': {'crop_name': crop_dict[crop_name].name,
                 'variety_name': crop_dict[crop_name].variety,
                 'crop_start_date': start_date,
                 'crop_start_type': 'emergence',
                 'crop_end_date': end_date,
                 'crop_end_type': 'harvest',
                 'max_duration': 300},
                'TimedEvents': None,
                'StateEvents': None}}]}
