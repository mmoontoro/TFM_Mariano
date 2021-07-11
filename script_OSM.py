# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:31:38 2021

@author: Mariano
"""
import os
tfm_dir = "D://Dropbox/Escritorio/TFM/Workspace_spyder/" 
os.chdir(tfm_dir)
import pandas as pd
from my_functions import osm, geo
import geopandas as gpd
from datetime import datetime

import numpy as np
import math

#%% Sites geodataframe
muni_pob = gpd.read_file("output/REJILLA.shp")
df_sites_1 = pd.read_csv('output/SITES_CAPACITY.csv')
df_sites_2 = geo.addMuniProvComA(df_sites_1, muni_pob)
df_sites_3 = geo.tag_comA(df_sites_2, muni_pob)
df_sites_4 = geo.tag_prov(df_sites_3, muni_pob)
df_sites_4.to_file('output/SITES_CAPACITY.shp', index = False)

#%% AGRIFOOD Queries
startTime = datetime.now()
print(startTime)
#landuse = "orchard"
landuse = "vineyard"

df, data_way = osm.get_way_as_point("Agrifood", "landuse", landuse)

df.to_csv("output/"+landuse+".csv", index = False)
endTime = datetime.now()
print(endTime)

#%% AGRIFOOD dataframe
muni_pob = gpd.read_file("output/REJILLA.shp")

df_orchard = pd.read_csv("output/orchard.csv")
df_vineyard = pd.read_csv("output/vineyard.csv")

# AGRIFOOD part
np.random.seed(10)
remove_n = math.floor(df_orchard.shape[0] * 19 / 20)
drop_indices = np.random.choice(df_orchard.index, remove_n, replace=False)
df_orchard_part = df_orchard.drop(drop_indices)

remove_n = math.floor(df_vineyard.shape[0] * 19 / 20)
drop_indices = np.random.choice(df_vineyard.index, remove_n, replace=False)
df_vineyard_part = df_vineyard.drop(drop_indices)

list_agrifood = [df_orchard_part, df_vineyard_part]
df_agrifood = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_agrifood = df_agrifood.append(list_agrifood)
df_agrifood.to_csv("output/agrifood.csv", index = False)

# AGRIFOOD full
list_agrifood = [df_orchard, df_vineyard]
df_agrifood = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_agrifood = df_agrifood.append(list_agrifood)
df_agrifood.to_csv("output/agrifood_full.csv", index = False)

#%% AGRIFOOD geodataframe
df_agrifood_1 = pd.read_csv("output/agrifood.csv")
df_agrifood_2 = geo.addMuniProvComA(df_agrifood_1, muni_pob)
df_agrifood_3 = geo.tag_comA(df_agrifood_2, muni_pob)
df_agrifood_4 = geo.tag_prov(df_agrifood_3, muni_pob)
df_agrifood_4.to_file('output/agrifood.shp', index = False)

#%% AGRIFOOD geodataframe FULL
df_agrifood_1 = pd.read_csv("output/agrifood_full.csv")
df_agrifood_2 = geo.addMuniProvComA(df_agrifood_1, muni_pob)
df_agrifood_3 = geo.tag_comA(df_agrifood_2, muni_pob)
df_agrifood_4 = geo.tag_prov(df_agrifood_3, muni_pob)
df_agrifood_4.to_file('output/agrifood_full.shp', index = False)

#%% MOBILITY Queries
startTime = datetime.now()
print(startTime)
#railway = "rail"
#highway = "motorway"
highway = "trunk"

df, data_way = osm.get_way_as_point("Mobility", 'highway', highway)
df.to_csv("output/"+highway+".csv", index = False)
endTime = datetime.now()
print(endTime)

#%% MOBILITY dataframe  
muni_pob = gpd.read_file("output/REJILLA.shp")

df_rail = pd.read_csv("output/rail.csv")
df_motorway = pd.read_csv("output/motorway.csv")
df_trunk = pd.read_csv("output/trunk.csv")

# MOBILITY part
np.random.seed(10)
remove_n = math.floor(df_rail.shape[0] * 19 / 20)
drop_indices = np.random.choice(df_rail.index, remove_n, replace=False)
df_rail_part = df_rail.drop(drop_indices)

np.random.seed(10)
remove_n = math.floor(df_motorway.shape[0] * 19 / 20)
drop_indices = np.random.choice(df_motorway.index, remove_n, replace=False)
df_motorway_part = df_motorway.drop(drop_indices)

np.random.seed(10)
remove_n = math.floor(df_trunk.shape[0] * 19 / 20)
drop_indices = np.random.choice(df_trunk.index, remove_n, replace=False)
df_trunk_part = df_trunk.drop(drop_indices)

list_mobility = [df_rail_part, df_motorway_part, df_trunk_part]
df_mobility = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_mobility = df_mobility.append(list_mobility)
df_mobility.to_csv("output/mobility.csv", index = False)

# MOBILITY full
list_mobility = [df_rail, df_motorway, df_trunk]
df_mobility = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_mobility = df_mobility.append(list_mobility)
df_mobility.to_csv("output/mobility_full.csv", index = False)

#%% MOBILITY geodataframe
df_mobility_1 = pd.read_csv("output/mobility.csv")
df_mobility_2 = geo.addMuniProvComA(df_mobility_1, muni_pob)
df_mobility_3 = geo.tag_comA(df_mobility_2, muni_pob)
df_mobility_4 = geo.tag_prov(df_mobility_3, muni_pob)
df_mobility_4.to_file('output/mobility.shp', index = False)

#%% MOBILITY geodataframe FULL
df_mobility_1 = pd.read_csv("output/mobility_full.csv")
df_mobility_2 = geo.addMuniProvComA(df_mobility_1, muni_pob)
df_mobility_3 = geo.tag_comA(df_mobility_2, muni_pob)
df_mobility_4 = geo.tag_prov(df_mobility_3, muni_pob)
df_mobility_4.to_file('output/mobility_full.shp', index = False)

#%% COMMERCE Queries
startTime = datetime.now()
print(startTime)
#shop = "clothes"
#shop = "electronics"
shop = "newsagent"

#not done yet:
#amenity = "pharmacy"
#amenity = "nursing_home"
df, data_node = osm.get_node("Commerce", 'shop', shop)
df.to_csv("output/"+shop+".csv", index = False)
endTime = datetime.now()
print(endTime)

#%% COMMERCE dataframe
muni_pob = gpd.read_file("output/REJILLA.shp")

df_clothes = pd.read_csv("output/clothes.csv")
df_electronics = pd.read_csv("output/electronics.csv")
df_newsagent = pd.read_csv("output/newsagent.csv")

# COMMERCE part
np.random.seed(10)
remove_n = math.floor(df_clothes.shape[0] * 2 / 3)
drop_indices = np.random.choice(df_clothes.index, remove_n, replace=False)
df_clothes_part = df_clothes.drop(drop_indices)

list_commerce = [df_clothes_part, df_electronics, df_newsagent]
df_commerce = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_commerce = df_commerce.append(list_commerce)
df_commerce.to_csv("output/commerce.csv", index = False)

# COMMERCE full
list_commerce = [df_clothes, df_electronics, df_newsagent]
df_commerce = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_commerce = df_commerce.append(list_commerce)
df_commerce.to_csv("output/commerce_full.csv", index = False)

#%% COMMERCE geodataframe
df_commerce_1 = pd.read_csv("output/commerce.csv")
df_commerce_2 = geo.addMuniProvComA(df_commerce_1, muni_pob)
df_commerce_3 = geo.tag_comA(df_commerce_2, muni_pob)
df_commerce_4 = geo.tag_prov(df_commerce_3, muni_pob)
df_commerce_4.to_file('output/commerce.shp', index = False)

#%% COMMERCE geodataframe FULL
df_commerce_1 = pd.read_csv("output/commerce_full.csv")
df_commerce_2 = geo.addMuniProvComA(df_commerce_1, muni_pob)
df_commerce_3 = geo.tag_comA(df_commerce_2, muni_pob)
df_commerce_4 = geo.tag_prov(df_commerce_3, muni_pob)
df_commerce_4.to_file('output/commerce_full.shp', index = False)


#%% HEALTH Queries
startTime = datetime.now()
print(startTime)
amenity = "hospital"
#amenity = "clinic"
#amenity = "doctors"

df, data_node, data_way = osm.get_tag("Health", "amenity", amenity)
df.to_csv("output/"+amenity+".csv", index = False)
endTime = datetime.now()
print(endTime)

#%% HEALTH dataframe
muni_pob = gpd.read_file("output/REJILLA.shp")

df_hospital = pd.read_csv("output/hospital.csv")
df_clinic = pd.read_csv("output/clinic.csv")
df_doctors = pd.read_csv("output/doctors.csv")

# HEALTH part
np.random.seed(10)
remove_n = math.floor(df_clinic.shape[0] * 2 / 3)
drop_indices = np.random.choice(df_clinic.index, remove_n, replace=False)
df_clinic_part = df_clinic.drop(drop_indices)

list_health = [df_hospital, df_clinic_part, df_doctors]
df_health = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_health = df_health.append(list_health)
df_health.to_csv("output/health.csv", index = False)

# HEALTH full
list_health = [df_hospital, df_clinic, df_doctors]
df_health = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_health = df_health.append(list_health)
df_health.to_csv("output/health_full.csv", index = False)


#%% HEALTH geodataframe
df_health_1 = pd.read_csv("output/health.csv")
df_health_2 = geo.addMuniProvComA(df_health_1, muni_pob)
df_health_3 = geo.tag_comA(df_health_2, muni_pob)
df_health_4 = geo.tag_prov(df_health_3, muni_pob)
df_health_4.to_file('output/health.shp', index = False)

#%% HEALTH geodataframe FULL
df_health_1 = pd.read_csv("output/health_full.csv")
df_health_2 = geo.addMuniProvComA(df_health_1, muni_pob)
df_health_3 = geo.tag_comA(df_health_2, muni_pob)
df_health_4 = geo.tag_prov(df_health_3, muni_pob)
df_health_4.to_file('output/health_full.shp', index = False)

#%% TOURISM Queries
startTime = datetime.now()
print(startTime)
tourism = "attraction"
#tourism = "gallery"
#tourism = "museum"
#tourism = "theme_park"

df, data_node, data_way = osm.get_tag("Tourism", 'tourism', tourism)
df.to_csv("output/"+tourism+".csv", index = False)
endTime = datetime.now()
print(endTime)

#%% TOURISM dataframe
muni_pob = gpd.read_file("output/REJILLA.shp")

df_attraction = pd.read_csv("output/attraction.csv")
df_gallery = pd.read_csv("output/gallery.csv")
df_museum = pd.read_csv("output/museum.csv")
df_theme_park = pd.read_csv("output/theme_park.csv")

# TOURISM part
np.random.seed(10)
remove_n = math.floor(df_attraction.shape[0] * 2 / 3)
drop_indices = np.random.choice(df_attraction.index, remove_n, replace=False)
df_attraction_part = df_attraction.drop(drop_indices)

np.random.seed(10)
remove_n = math.floor(df_museum.shape[0] * 2 / 3)
drop_indices = np.random.choice(df_museum.index, remove_n, replace=False)
df_museum_part = df_museum.drop(drop_indices)

list_tourism = [df_attraction_part, df_museum_part, df_gallery, df_theme_park]
df_tourism = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_tourism = df_tourism.append(list_tourism)
df_tourism.to_csv("output/tourism.csv", index = False)

#TOURISM full
list_tourism = [df_attraction, df_museum, df_gallery, df_theme_park]
df_tourism = pd.DataFrame(columns=['id','lon','lat','layer','hover','name'])
df_tourism = df_tourism.append(list_tourism)
df_tourism.to_csv("output/tourism_full.csv", index = False)


#%% TOURISM geodataframe
df_tourism_1 = pd.read_csv("output/tourism.csv")
df_tourism_2 = geo.addMuniProvComA(df_tourism_1, muni_pob)
df_tourism_3 = geo.tag_comA(df_tourism_2, muni_pob)
df_tourism_4 = geo.tag_prov(df_tourism_3, muni_pob)
df_tourism_4.to_file('output/tourism.shp', index = False)

#%% TOURISM FULL geodataframe
df_tourism_1 = pd.read_csv("output/tourism_full.csv")
df_tourism_2 = geo.addMuniProvComA(df_tourism_1, muni_pob)
df_tourism_3 = geo.tag_comA(df_tourism_2, muni_pob)
df_tourism_4 = geo.tag_prov(df_tourism_3, muni_pob)
df_tourism_4.to_file('output/tourism_full.shp', index = False)


