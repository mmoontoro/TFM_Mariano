# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:24:40 2021

@author: Mariano
"""
# Load LIBRARIES
import os
tfm_dir = "D://Dropbox/Escritorio/TFM/Workspace_spyder/" 
os.chdir(tfm_dir)

import pandas as pd
from my_functions import geo, sit
from datetime import datetime

import geopandas as gpd

#%%

df_sites = pd.read_csv("output/SITES_BAND.csv")

sit.df_overview(df_sites)
print("")

startTime = datetime.now()
print(startTime)

df_sites_capacity = sit.capacity_calc(df_sites)

endTime = datetime.now()
print(endTime)

df_sites_capacity.to_csv('output/SITES_CAPACITY.csv', index = False)

    


