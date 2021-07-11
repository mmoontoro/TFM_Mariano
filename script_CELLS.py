# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:56:49 2021

@author: Mariano
"""
# Load LIBRARIES
import os
tfm_dir = "D://Dropbox/Escritorio/TFM/Workspace_spyder/" 
os.chdir(tfm_dir)
# Subset that makes a cell unique according to the standard
my_subset = ['cell', 'net', 'mcc']

import pandas as pd
from my_functions import cel, dis
from datetime import datetime
from collections import Counter

#%% 0 - Load DFs and Merge with extra information
startTime = datetime.now()
print(startTime)
print("Start Load MLS")
df_mls_raw = pd.read_csv("input/MLS-full-cell-export-2021-02-04T000000.csv")
df_mls_clean = cel.clean_df(df_mls_raw, "MLS")
df_mls_clean['source'] = 'mls'
df_mls_clean['enbid'],df_mls_clean['cellid']=divmod(df_mls_clean['cell'],256)
df_mls_band = cel.add_band(df_mls_clean)
df_mls_final = cel.del_dup_recent_area(df_mls_band)
df_mls_final.to_csv('output/MLS_final.csv', index = False)
print("Just for checking, duplicates must be 0")
df_mls_final = cel.del_dup_max_samples(df_mls_final, my_subset)
print("End Load MLS")
endTime = datetime.now()
print(endTime)
print()

startTime = datetime.now()
print(startTime)
print("Start Load OID")
df_oid_raw = pd.read_csv("input/cell_towers_2021-02-10-T000000.csv")
df_oid_clean =  cel.clean_df(df_oid_raw, "OID")
df_oid_clean['source'] = 'oid'
df_oid_clean['enbid'],df_oid_clean['cellid']=divmod(df_oid_clean['cell'],256)
df_oid_band = cel.add_band(df_oid_clean)
df_oid_final = cel.del_dup_recent_area(df_oid_band)
df_oid_final.to_csv('output/OID_final.csv', index = False)
print("Just for checking, duplicates must be 0")
df_oid_final = cel.del_dup_max_samples(df_oid_final, my_subset)
print("End Load OID")
endTime = datetime.now()
print(endTime)
print()

startTime = datetime.now()
print(startTime)
print("Start Mrege") 
df_oid_final = pd.read_csv("output/OID_final.csv")
df_mls_final = pd.read_csv("output/MLS_final.csv")
df_merged = df_mls_final.append(df_oid_final, ignore_index=True)
df_merged_2 = cel.del_dup_recent_area(df_merged)
#Debe eliminar los mismos usando ambos subsets.
#my_subset = ['cell', 'net', 'mcc', 'area']
df_cells = cel.del_dup_max_samples(df_merged_2, my_subset)
df_cells['site_lat'] = df_cells.lat
df_cells['site_lon'] = df_cells.lon
df_cells['errorKm'] = 0    
df_cells.to_csv('output/CELLS.csv', index = False)
print("End Mrege")
endTime = datetime.now()
print(endTime)

#%% 1.1 - Load DFs (10 min)
startTime = datetime.now()
print(startTime)
print("Start Load MLS")
df_mls_raw = pd.read_csv("input/MLS-full-cell-export-2021-02-04T000000.csv")
df_mls_clean = cel.clean_df(df_mls_raw, "MLS")
df_mls_clean['source'] = 'mls'
df_mls_clean['enbid'],df_mls_clean['cellid']=divmod(df_mls_clean['cell'],256)
df_mls_clean.to_csv('output/MLS_clean.csv', index = False)
print("End Load MLS")
print()
print("Start Load OID")
df_oid_raw = pd.read_csv("input/cell_towers_2021-02-10-T000000.csv")
df_oid_clean =  cel.clean_df(df_oid_raw, "OID")
df_oid_clean['source'] = 'oid'
df_oid_clean['enbid'],df_oid_clean['cellid']=divmod(df_oid_clean['cell'],256)
df_oid_clean.to_csv('output/OID_clean.csv', index = False)
print("End Load OID")
endTime = datetime.now()
print(endTime)
print()

# Solape Inicial informativo
df_mls_inf = cel.del_dup_max_samples(df_mls_clean, my_subset)
df_oid_inf = cel.del_dup_max_samples(df_oid_clean, my_subset)
df_dup_inf = df_mls_inf.append(df_oid_inf, ignore_index=True)
df_no_dup_inf = cel.del_dup_max_samples(df_dup_inf, my_subset)

#%% 1.2 - Merge (30 min)
startTime = datetime.now()
print(startTime)
print("Start Mrege") 
df_merged = df_oid_clean.append(df_mls_clean, ignore_index=True)
df_merged_2 = cel.del_dup_recent_area(df_merged)
#Debe eliminar los mismos usando ambos subsets.
#my_subset = ['cell', 'net', 'mcc', 'area']
df_cells = cel.del_dup_max_samples(df_merged_2, my_subset)
df_cells['site_lat'] = df_cells.lat
df_cells['site_lon'] = df_cells.lon
df_cells['errorKm'] = 0
df_cells_band = cel.add_band(df_cells)
df_cells_band.to_csv('output/CELLS.csv', index = False)
print("End Mrege")
endTime = datetime.now()
print(endTime)

#%% 2 - Cells clustering (10 min.)
startTime = datetime.now()
print(startTime)

df_cells = pd.read_csv('output/CELLS.csv')

df_cells_clu, df_sites_clu = cel.cells_clustering(df_cells)

df_cells_clu.to_csv('output/CELLS_CLU.csv', index = False)
df_sites_clu.to_csv('output/SITES_CLU.csv', index = False)

endTime = datetime.now()
print(endTime)

#%% 2.1 Calculate errorKm distribution
df_cells_clu = pd.read_csv('output/CELLS_CLU.csv')
df_sites_clu = pd.read_csv('output/SITES_CLU.csv')

p = [.5, .75, .9, .95]
print("CELLS errorKm")
print(str(df_cells_clu.errorKm.describe(percentiles = p)))
print()
print("CELLS errorKm by samples")
df = df_cells_clu[df_cells_clu.samples < 10]
print(str(df.groupby('samples').errorKm.describe(percentiles = p)))
print()
print("SITES errorKm_mean")
print(str(df_sites_clu.errorKm_mean.describe(percentiles = p)))
print()

#%% 3.1 - Delete sites with much error after clustering
startTime = datetime.now()
print(startTime)

df_cells_clu = pd.read_csv('output/CELLS_CLU.csv')
df_sites_clu = pd.read_csv('output/SITES_CLU.csv')

percentil95 = 4.025017
df_cells_threshold = df_cells_clu[df_cells_clu['errorKm'] < percentil95]
df_cells_clean_1, df_sites_clean_1 = cel.cells_clustering(df_cells_threshold)

df_cells_clean_1.to_csv('output/CELLS_CLEAN_1.csv', index = False)
df_sites_clean_1.to_csv('output/SITES_CLEAN_1.csv', index = False)

endTime = datetime.now()
print(endTime)

#%% 3.2 - Delete sites with much error after clustering (15 min)
startTime = datetime.now()
print(startTime)

df_cells_clu = pd.read_csv('output/CELLS_CLU.csv')
df_sites_clu = pd.read_csv('output/SITES_CLU.csv')

threshold_km = percentil95
n_iter = 1
df_cells_clean_2, df_sites_clean_2 = cel.clean_clustering\
    (df_cells_clu, df_sites_clu, n_iter, threshold_km)
    
t_d_c = df_cells_clu.shape[0] - df_cells_clean_2.shape[0]
t_d_s = df_sites_clu.shape[0] - df_sites_clean_2.shape[0]
print("Deleted Sites: " + str(t_d_s))
print("Total Deleted Cells: "+str(t_d_c))

df_cells_clean_2.to_csv('output/CELLS_CLEAN_2.csv', index = False)
df_sites_clean_2.to_csv('output/SITES_CLEAN_2.csv', index = False)

endTime = datetime.now()
print(endTime)

#%% 4 Band info to the sites dataframe
startTime = datetime.now()
print(startTime)

df_cells_clean_2 = pd.read_csv('output/CELLS_CLEAN_2.csv')
df_sites_clean_2 = pd.read_csv('output/SITES_CLEAN_2.csv')

df_sites_band = cel.add_sites_band(df_cells_clean_2, df_sites_clean_2)

df_sites_band.to_csv('output/SITES_BAND.csv', index = False)

endTime = datetime.now()
print(endTime)

#%% 100 - Map Plot before and after clustering
df_cells = pd.read_csv('output/CELLS.csv')
df_cells_clu = pd.read_csv('output/CELLS_CLU.csv')
df_cells_clean_1 = pd.read_csv('output/CELLS_CLEAN_1.csv')
df_cells_clean_2 = pd.read_csv('output/CELLS_CLEAN_2.csv')

dis.plot(df_cells, 'net', "Cells Non-Clustered")
dis.plot(df_cells_clu, 'net', "Cells Clustered")
dis.plot(df_cells_clean_1, 'net', "Cells Clustered Clean 1")
dis.plot(df_cells_clean_2, 'net', "Cells Clustered Clean 2")

#%% Celdas segun la banda
df_cells_clean_2 = pd.read_csv('output/CELLS_CLEAN_2.csv')
df = df_cells_clean_2.sort_values('band')
dis.plot(df, 'band', "Cells Clustered Clean 2")

#%% 101 - Print data overview

df_cells_clu = pd.read_csv('output/CELLS_CLU.csv')
df_sites_clu = pd.read_csv('output/SITES_CLU.csv')

df_cells_clean_1 = pd.read_csv('output/CELLS_CLEAN_1.csv')
df_sites_clean_1 = pd.read_csv('output/SITES_CLEAN_1.csv')

df_cells_clean_2 = pd.read_csv('output/CELLS_CLEAN_2.csv')
df_sites_clean_2 = pd.read_csv('output/SITES_CLEAN_2.csv')

group_subset = ['net', 'enbid']
cel.df_overview(df_cells_clu, group_subset, "Cells Clustered")
cel.df_overview(df_cells_clean_1, group_subset, "Cells Clustering Clean 1")
cel.df_overview(df_cells_clean_2, group_subset, "Cells Clustering Clean 2")

#%% Estudio de casos concretos de clean clustering

#c = [7, 380155]
#c = [7, 351084]
c = [1, 10107]

df_cells_clean_2 = pd.read_csv('output/CELLS_CLEAN_2.csv')
df_sites_clean_2 = pd.read_csv('output/SITES_CLEAN_2.csv')
df = df_cells_clean_2.copy()
dfc = df[(df.net==c[0])&(df.enbid==c[1])]
df = df_sites_clean_2.copy()
dfs = df[(df.net==c[0])&(df.enbid==c[1])]
dis.plot_cluestering(dfc, dfs, 'type', str(c)+" After clean 2")

df_cells_clean_1 = pd.read_csv('output/CELLS_CLEAN_1.csv')
df_sites_clean_1 = pd.read_csv('output/SITES_CLEAN_1.csv')
df = df_cells_clean_1.copy()
dfc = df[(df.net==c[0])&(df.enbid==c[1])]
df = df_sites_clean_1.copy()
dfs = df[(df.net==c[0])&(df.enbid==c[1])]
dis.plot_cluestering(dfc, dfs, 'type', str(c)+" After clean 1")

df_cells_clu = pd.read_csv('output/CELLS_CLU.csv')
df_sites_clu = pd.read_csv('output/SITES_CLU.csv')
df = df_cells_clu.copy()
dfc = df[(df.net==c[0])&(df.enbid==c[1])]
df = df_sites_clu.copy()
dfs = df[(df.net==c[0])&(df.enbid==c[1])]
dis.plot_cluestering(dfc, dfs, 'type', str(c)+" Before")

#%% ------------ useful code -------------------
        
df[(df.net==1)&(df.area==3090)&(df.enbid==73209)]
condition_sites = (df_sites_2.net!=i[0])|(df_sites_2.area!=i[1])\
            |(df_sites_2.enbid!=i[2])
            
df_no_dup.groupby(['net','cell']).size().value_counts()

