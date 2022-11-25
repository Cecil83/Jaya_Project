#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import datetime
import config as c


from collections import namedtuple

Crop = namedtuple('Crop', ['name', 'variety'])

crop_dict = {'sunflower': Crop(name='sunflower', variety='Sunflower_1101'),
             'soybean': Crop(name='soybean', variety='Soybean_901'),
             'millet': Crop(name='millet', variety='Millet_VanHeemst_1988'),
             'barley': Crop(name='springbarley', variety='Spring_barley_301'),
             'mungbean': Crop(name='mungbean', variety='Mungbean_VanHeemst_1988'),
             'tobacco': Crop(name='tobacco', variety='Tobacco_VanHeemst_1988'),
             'rapeseed': Crop(name='rapeseed', variety='Oilseed_rape_1001'),
             'groundnut': Crop(name='groundnut', variety='Groundnut_VanHeemst_1988'),
             'cotton': Crop(name='cotton', variety='Cotton_VanHeemst_1988'),
             'cowpea': Crop(name='cowpea', variety='Cowpea_VanHeemst_1988'),
             'chickpea': Crop(name='chickpea', variety='Chickpea_VanHeemst_1988'),
             'sugarbeet': Crop(name='sugarbeet', variety='Sugarbeet_601'),
             'fababean': Crop(name='fababean', variety='Faba_bean_801'),
             'sugarcane': Crop(name='sugarcane', variety='Sugarcane_VanHeemst_1988'),
             'potato': Crop(name='potato', variety='Potato_701'),
             'wheat': Crop(name='winterwheat', variety='Winter_wheat_101'),
             'pigeonpea': Crop(name='pigeonpea', variety='Pigeonpea_VanHeemst_1988'),
             'sorghum': Crop(name='sorghum', variety='Sorghum_VanHeemst_1988'),
             'cassava': Crop(name='cassava', variety='Cassava_VanHeemst_1988'),
             'maize': Crop(name='tropical_maize', variety='Maize_VanHeemst_1988'),
             'seed_onion': Crop(name='seed_onion', variety='onion_agriadapt'),
             'rice': Crop(name='rice_eu', variety='Rice_501'),
             'sweetpotato': Crop(name='sweetpotato', variety='Sweetpotato_VanHeemst_1988')}


# Crop

crop = crop_dict[c.crop_name]

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
             'AgroManagement': [{datetime.date(2006, 1, 1): {'CropCalendar': {'crop_name': crop.name,
                 'variety_name': crop.variety,
                 'crop_start_date': datetime.date(2006, 4, 5),
                 'crop_start_type': 'emergence',
                 'crop_end_date': datetime.date(2006, 10, 20),
                 'crop_end_type': 'harvest',
                 'max_duration': 300},
                'TimedEvents': None,
                'StateEvents': None}}]}