#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from pcse.util import WOFOST72SiteDataProvider

from collections import namedtuple

Crop = namedtuple('Crop', ['name', 'variety'])

granularite = 2

# CROP CHOICE

"""
Choix de crops :
    sunflower, soybean, millet, barley, mungbean, obacco, rapeseed, roundnut,
    cotton, cowpea, chickpea, sugarbeet, fababean, sugarcane, potato, wheat, 
    pigeonpea, sorghum, cassava, maize, seed_onion, rice, sweetpotato
"""
# Soit itérer sur toutes les crops

# one_crop=False
one_crop = True

# Si one_crop=True
crop_name = 'fababean'

# CONFIG

start_date = datetime.date(2006, 1, 1)
end_date = datetime.date(2007, 1, 1)

# WEATHER
# Soleil
# Soit one_sun=True et une seule valeur d'ensoleillement "sun" est choisie, soit False
# et 10 valeurs sont prises en partant de sun_min et par step de sun_step

one_sun = False
# one_sun=True

sun_min = 4000.
sun_max = 28000
#elargir le max
sun_step = (sun_max - sun_min) / (granularite - 1)

sun = 10000.0

# Wind

one_wind = False
# one_wind=True

wind_min = 0.6
wind_max = 9.9
wind_step = (wind_max - wind_min) / (granularite - 1)

wind = 2.8

# Rain

one_rain = False
# one_rain=True

rain_min = 0.
rain_max = 50.4
rain_step = (rain_max - rain_min) / (granularite - 1)

rain = 2.4

# Température
# Soit one_sun=True et une seule valeur d'ensoleilement "sun" est choisie, soit False
# et 10 valeurs sont prises en partant de sun_min et par step de sun_step

one_temp = False
# one_temp=True

temp_min = -8.5
temp_max = 26.9
#A AFFINER
temp_step = (temp_max - temp_min) / (granularite - 1)

temp = 18.

# SOIL


# Soit itérer sur tous les soils

# one_soil=False
one_soil = True

# Si one_soil=True
soil_name = 'ec3.soil'

##########################################################################
# FIN DU FICHIER CONFIG (La suite est faite pour s'exécuter par import du fichier)


# Soleil, température, eau, nutriment

crop_dict = {  # 'sunflower': Crop(name='sunflower', variety='Sunflower_1101'),
    # 'soybean': Crop(name='soybean', variety='Soybean_901'),
    # 'millet': Crop(name='millet', variety='Millet_VanHeemst_1988'),
    # 'barley': Crop(name='barley', variety='Spring_barley_301'),
    # 'mungbean': Crop(name='mungbean', variety='Mungbean_VanHeemst_1988'),
    # 'tobacco': Crop(name='tobacco', variety='Tobacco_VanHeemst_1988'),
    # 'rapeseed': Crop(name='rapeseed', variety='Oilseed_rape_1001'),
    # 'groundnut': Crop(name='groundnut', variety='Groundnut_VanHeemst_1988'),
    # 'cotton': Crop(name='cotton', variety='Cotton_VanHeemst_1988'),
    # 'cowpea': Crop(name='cowpea', variety='Cowpea_VanHeemst_1988'),
    # 'chickpea': Crop(name='chickpea', variety='Chickpea_VanHeemst_1988'),
    # 'sugarbeet': Crop(name='sugarbeet', variety='Sugarbeet_601'),
    'fababean': Crop(name='fababean', variety='Faba_bean_801'),
    # 'sugarcane': Crop(name='sugarcane', variety='Sugarcane_VanHeemst_1988'),
    # 'potato': Crop(name='potato', variety='Potato_701'),
    # 'wheat': Crop(name='wheat', variety='Winter_wheat_101'),
    # 'pigeonpea': Crop(name='pigeonpea', variety='Pigeonpea_VanHeemst_1988'),
    # 'sorghum': Crop(name='sorghum', variety='Sorghum_VanHeemst_1988'),
    # 'cassava': Crop(name='cassava', variety='Cassava_VanHeemst_1988'),
    # 'maize': Crop(name='maize', variety='Maize_VanHeemst_1988'),
    # 'seed_onion': Crop(name='seed_onion', variety='onion_agriadapt'),
    # 'rice': Crop(name='rice', variety='Rice_501'),
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
    suns = [sun_min + sun_step * float(i) for i in range(granularite)]

# Wind

if one_wind:
    winds = [wind]
else:
    winds = [wind_min + wind_step * float(i) for i in range(granularite)]

# Rain

if one_rain:
    rains = [rain]
else:
    rains = [rain_min + rain_step * float(i) for i in range(granularite)]

# Temperature

if one_temp:
    temps = [temp]
else:
    temps = [temp_min + temp_step * float(i) for i in range(granularite)]

# Site
"""
The following site specific parameter values can be set through this data provider::

    - IFUNRN    Indicates whether non-infiltrating fraction of rain is a function of storm size (1)
                or not (0). Default 0
    - NOTINF    Maximum fraction of rain not-infiltrating into the soil [0-1], default 0.
    - SSMAX     Maximum depth of water that can be stored on the soil surface [cm]
    - SSI       Initial depth of water stored on the surface [cm]
    - WAV       Initial amount of water in total soil profile [cm]
    - SMLIM     Initial maximum moisture content in initial rooting depth zone [0-1], default 0.4
"""

sited = WOFOST72SiteDataProvider(IFUNRN=0,
                                 NOTINF=0.,
                                 SSI=0.,
                                 SSMAX=0,
                                 WAV=0.,
                                 SMLIM=0.)

# Reste à faire l'eau et les nutriments, et le site (soil profile etc )


##################################################################

# Ici, config de base qui sera modifiée par les scripts

# config

weather_config_dict = {'irrad': 10000.,
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
