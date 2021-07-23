# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:30:45 2021

@author: Mariano
"""
import pandas as pd
from my_functions import geo
from collections import Counter

def clean_df(df_raw, str_cleaning_id):
    '''
    Filtra las filas del dataframe para conservar solo las que interesan.
    
    Apartado TFM: "3.2.1 Filtrado inicial de los datos abiertos"

    Parameters
    ----------
    df_raw : dataframe
        todas las celdas descargadas de la fuente de datos.
    str_cleaning_id : string
        nombre que identifica al dataframe.

    Returns
    -------
    df_fil : dataframe
        celdas que nos interesan.

    '''
    print("-----------------------------------")
    print("Start Clean " + str_cleaning_id)
    df_fil = df_raw.copy()
    df_fil = df_raw[df_raw['samples'] > 4]
    df_fil = df_fil.loc[df_fil['mcc'] == 214]
    df_fil = df_fil.loc[df_fil['radio'] != 'UMTS']
    df_fil = df_fil.loc[df_fil['radio'] != 'GSM']
    df_fil = df_fil[df_fil['lat'].between(27.64, 43.78, inclusive=True)]
    df_fil = df_fil[df_fil['lon'].between(-18.16, 4.32, inclusive=True)]
    # Eliminamos operadores pequeños
    df_fil = df_fil[df_fil.groupby('net')['net'].transform('count').ge(300)]
    # Celdas vistas los ultimos dos años
    df_fil = df_fil.loc[df_fil['updated'] > 1546297200]
    del df_fil['unit']
    del df_fil['averageSignal']
    del df_fil['changeable']
    print("End Clean " + str_cleaning_id)
    print("-----------------------------------")
    return df_fil

def del_dup_recent_area(df_dup):
    '''
    Recorre todas las estaciones que tengan más de un TAC, y mantiene todas 
    las celdas de aquella estacion con un codigo TAC más reciente.
    
    Apartado TFM: "3.2.2 Eliminacion de celdas duplicadas debido al codigo de area"

    Parameters
    ----------
    df_dup : dataframe
        dataframe con algunas celdas duplicadas.

    Returns
    -------
    df_no_dup : dataframe
        dataframe de celdas, sin celdas duplicadas.

    '''
    print("-----------------------------------")
    print("Start Delete Duplicates keeping most recent area site")
    set_sites = ['enbid', 'net', 'mcc']
    list_columns = []
    for c in df_dup.columns:
        list_columns.append(str(c))
    df_no_dup = pd.DataFrame(columns = list_columns)
                             
    list_dup = []
    list_repetitions = []
    list_n_areas = []
    n_solapes = 0
    n_no_solapes = 0
    n_simultaneos = 0
    # Recorremos primero los viendo cuales tienen mas de 1 TAC. 
    # De ahi saca el valor de TAC con las celdas mas recientes.
    # Nos quedamos con todas las celdas del site con el TAC mas reciente.
    
    for i, s in df_dup.groupby(set_sites):
        n_areas = len(s.area.value_counts())
        list_n_areas.append(n_areas)
    
        if n_areas > 1:
            #print(i)
            areas = s.area.unique()
            dict_areas = dict((a,0) for a in areas)
            for j, r in s.groupby(['cell']):
                n_repetitions = len(r)
                list_repetitions.append(n_repetitions)
                if n_repetitions > 1:
                    list_dup.append(r)
                    a = r[r.updated == r.updated.max()].area.values[0]
                    dict_areas[a] = dict_areas[a] + 1
                    #Mera informacion acerca de los solapes
                    c1 = r.iloc[0].created; c2 = r.iloc[1].created
                    u1 = r.iloc[0].updated; u2 = r.iloc[1].updated
                    if c2 < c1:
                        if u2 <= c1: n_no_solapes = n_no_solapes + 1
                        else: n_solapes = n_solapes + 1
                    elif c1 < c2:
                        if u1 <= c2: n_no_solapes = n_no_solapes + 1
                        else: n_solapes = n_solapes + 1
                    else: n_simultaneos = n_simultaneos + 1
            #print(dict_areas)
            #print("")
            max_value = max(dict_areas.values())
            max_keys = [k for k, v in dict_areas.items() if v == max_value]
            if len(max_keys) > 1:
                a = s[s.updated == s.updated.max()].area.values[0]
                dict_areas[a] = dict_areas[a] + 1
                max_value = max(dict_areas.values())
                max_keys = [k for k, v in dict_areas.items() if v == max_value]    
            chosen_area = max_keys[0]
            
        elif n_areas == 1:
            chosen_area = s.area.values[0]
        
        condition = (df_dup.net == i[1])&\
                        (df_dup.area == chosen_area)&\
                        (df_dup.enbid == i[0])
        df_no_dup = df_no_dup.append(df_dup.loc[condition])

    n_duplicates = df_dup.shape[0] - df_no_dup.shape[0]
    print("    Original DF size: " + str(df_dup.shape[0]))
    print("        MLS: " + str(df_dup[df_dup['source'] == 'mls'].shape[0]))
    print("        OID: " + str(df_dup[df_dup['source'] == 'oid'].shape[0]))
    print("    Final DF size: " + str(df_no_dup.shape[0]))
    print("        MLS: "+str(df_no_dup[df_no_dup['source']=='mls'].shape[0]))
    print("        OID: "+str(df_no_dup[df_no_dup['source']=='oid'].shape[0]))
    print("    ")
    print("    Combination for sites: " + str(set_sites))
    print("    Sites total: " + str(len(list_n_areas)))
    dict_n_areas = Counter(list_n_areas)
    for k in dict_n_areas:
        print("        " + str(k) + " area: " + str(dict_n_areas[k]))
    sites_sev_areas = len(list_n_areas) - dict_n_areas[1]
    print("    ")
    print("    The "+str(sites_sev_areas)+" sites with more than 1 area have:")
    print("    " + str(len(list_repetitions)) + " different cell ids.")
    print("    If one cell id is repeated it is always due to the existence")
    print("    of several area codes for that cell id. Cell ids with: ")
    dict_n_rep = Counter(list_repetitions)
    for k in dict_n_rep:
        print("        " + str(k) + " area: " + str(dict_n_rep[k]))
    cells_sev_areas = len(list_repetitions) - dict_n_rep[1]
    print("    ")
    print("    The "+str(cells_sev_areas)+ " cell ids with more than 1 area can be")
    print("    overlapping in time or not.")
    print("        No overlapping in time: "+str(n_no_solapes))
    print("        Overlapping in time:    "+str(n_solapes))
    print("        Simultaneous in time:   "+str(n_simultaneos))
    print("    ")
    print("End Delete Duplicates keeping most recent area site")
    print("-----------------------------------")
    return df_no_dup

def del_dup_max_samples(df_dup, my_subset):
    '''
    Elimina las celdas repetidas (aquellas con valores repetidos en todas  
    las columnas del subset), manteniendo unicamente aquella celda con 
    mayor numero de muestras.
    
    Apartado TFM: N/A

    Parameters
    ----------
    df_dup : dataframe
        dataframe de celdas con duplicados.
    my_subset : list
        lista de columnas que definen que exista duplicidad.

    Returns
    -------
    df_no_dup : dataframe
        datframe de celdas sin duplicados.

    '''
    print("-----------------------------------")
    print("Start Delete Duplicates keeping cell with maximum samples")
    
    df_dup_sorted = df_dup.sort_values('samples', ascending=False)
    df_no_dup = df_dup_sorted.drop_duplicates(my_subset, keep='first')
    n_duplicates = df_dup.shape[0] - df_no_dup.shape[0]
    
    print("    Original DF size: " + str(df_dup.shape[0]))
    print("        MLS: " + str(df_dup[df_dup['source'] == 'mls'].shape[0]))
    print("        OID: " + str(df_dup[df_dup['source'] == 'oid'].shape[0]))
    print("    Final DF size: " + str(df_no_dup.shape[0]))
    print("        MLS: "+str(df_no_dup[df_no_dup['source']=='mls'].shape[0]))
    print("        OID: "+str(df_no_dup[df_no_dup['source']=='oid'].shape[0]))
    print("    Using the subset: " + str(my_subset))
    print("    Duplicates: " + str(n_duplicates))
    
    print("End Delete Duplicates keeping cell with maximum samples")
    print("-----------------------------------")
    return df_no_dup

def cells_clustering(df_ini):
    '''
    Agrupa las celdas con el mismo codigo de estacion en la misma posicion.
    Añade nuevas columnas al dataframe de celdas. Crea un nuevo dataframe 
    de estaciones, indicando cuantas celdas hay encada estacion.
    
    Apartado TFM: "3.2.4 Creación del dataframe de estaciones inicial"

    Parameters
    ----------
    df_ini : dataframe
        dataframe de celdas inicial.

    Returns
    -------
    df_cells : dataframe
        dataframe de celdas con las nuevas columnas.
    df_sites : dataframe
        dataframe de estaciones inicial.

    '''
    print("-----------------------------------")
    print("Start Cells Clustering")
    df_cells = df_ini.copy()
    id_row = 0
    df_sites = pd.DataFrame(columns = ['net','enbid','area',\
                                       'site_lat','site_lon',\
                                        'n_cells','d_cells','errorKm_mean'])
    for i, g in df_cells.groupby(['net','enbid']):
        n_areas = len(g.area.value_counts())
        if n_areas > 1:
            print("There is one error. More than 1 area for this site:")
            print(str(i) + " " + str(g.area))
        site_n_cells = len(g)
        site_lat = g.lat.mean()
        site_lon = g.lon.mean()
        condition = (df_cells.net==i[0])&(df_cells.enbid==i[1]) 
        df_cells.loc[condition, 'site_lon'] = site_lon
        df_cells.loc[condition, 'site_lat'] = site_lat
        sum_dist = 0
        for j in g.index:
            cell_lat = g[g.index == j].lat
            cell_lon = g[g.index == j].lon
            dist_cell_site = geo.distance_calc(site_lat, site_lon,\
                                           cell_lat, cell_lon)
            df_cells.loc[df_cells.index == j, 'errorKm'] = dist_cell_site
            sum_dist = sum_dist + dist_cell_site
        errorKm_mean = sum_dist / site_n_cells
        df_sites.loc[id_row] = [i[0],i[1],str(g.area.values[0]),\
                                site_lat, site_lon,\
                                site_n_cells, 0, errorKm_mean]
        id_row = id_row + 1
    print("End Cells Clustering")
    print("-----------------------------------")
    return df_cells, df_sites


def clean_clustering(df_cells_1, df_sites_1, n_iter, threshold_km):
    '''
    Método A de mejora de la posicion de las estaciones.
    1. De todas las estaciones con celdas con error por encima del percentil 
    95% inicial, eliminar solo una celda por estación.
    2.	Recalcular la media de la posición y el nuevo error de las celdas 
    restantes de cada estación.
    3.	Volver a iterar hasta que el error todas las celdas quede por debajo 
    del percentil 95% inicial.
    
    Apartado TFM: "3.2.5 Mejora de posicion de las estaciones"

    Parameters
    ----------
    df_cells_1 : dataframe
        celdas iniciales, algunas de ellas con error por encima del umbral.
    df_sites_1 : dataframe
        estacione iniciales, algunas de ellas con error por encima del umbral.
    n_iter : integer
        indice de la iteracion, numero de veces que se ha pasado el dataframe 
        inicial por esta funcion recursiva.
    threshold_km : float
        umbral de error.

    Returns
    -------
    df_cells_fin : dataframe
        celdas tras iterar con el metodo A. En caso de que todas tengan un 
        error por debajo del umbral, no se volvera a iterar en esta funcion.
    df_sites_fin : dataframe
        estaciones tras iterar con el metodo A. En caso de que todas tengan un 
        error por debajo del umbral, no se volvera a iterar en esta funcion.

    '''
    i_c_c = 0
    i_s_s = 0
    if n_iter == 1:
        i_c_c = df_cells_1.shape[0]
        i_c_s = df_sites_1.n_cells.sum()
        i_s_c = df_cells_1.groupby(['net','area','enbid']).size().shape[0]
        i_s_s = df_sites_1.shape[0]
        print("-----------------------------------")
        print("CLEAN CLUSTERING")
        print("Initial Data:")
        print("-----------DF Cells------------")
        print("Sites: " + str(i_s_c) + ", Cells: "+str(i_c_c))
        print("-----------DF Sites------------")
        print("Sites: " + str(i_s_s) + ", Cells: "+str(i_c_s))
    print("    Start iter.: " + str(n_iter))
    df_cells_2 = df_cells_1.copy()
    df_sites_2 = df_sites_1.copy()
    #Start Select sites and cells
    df_to_keep = pd.DataFrame(columns=df_cells_1.columns)
    df_to_del = pd.DataFrame(columns=df_cells_1.columns)
    df_aux = df_cells_1[df_cells_1.errorKm > threshold_km]
    for i, g in df_aux.groupby(['net','area','enbid']):
        condition_cells = (df_cells_1.net==i[0])&(df_cells_1.area==i[1])\
            &(df_cells_1.enbid==i[2])
        df_one_site = df_cells_1[condition_cells].\
            sort_values('errorKm', ascending=False)
        if df_one_site.shape[0] > 2:        
            df_to_del = df_to_del.append(df_one_site.iloc[0])
            df_to_keep = df_to_keep.append(df_one_site.iloc[1:])
        else:
            df_to_del = df_to_del.append(df_one_site)
            condition_sites = (df_sites_2.net==i[0])&(df_sites_2.area==i[1])\
                &(df_sites_2.enbid==i[2])
            n_deleted_cells = df_sites_2[condition_sites].d_cells.values[0]
            n_cells = df_sites_2[condition_sites].n_cells.values[0]
            n_cells_to_del = df_one_site.shape[0]
            df_sites_2.loc[condition_sites, 'd_cells'] =\
                n_deleted_cells + n_cells_to_del
            df_sites_2.loc[condition_sites, 'n_cells'] =\
                n_cells - n_cells_to_del
    #End Select sites and cells
    
    #Start Delete and cells
    for i, g in df_to_del.groupby(['net','area','enbid']):
        condition_cells = (df_cells_1.net==i[0])&(df_cells_1.area==i[1])\
            &(df_cells_1.enbid==i[2])
        df_cells_2 = df_cells_2.drop(df_cells_1[condition_cells].index)
    #End Delete cells
    
    #Start recalculate coord. and reintroduce
    df_cells_3 = df_cells_2.copy()
    for i, g in df_to_keep.groupby(['net','area','enbid']):
        df_cells_3 = df_cells_3.append(g)
        site_n_cells = len(g)
        site_lat = g.lat.mean()
        site_lon = g.lon.mean()
        sum_dist = 0
        for j in g.index:
            cell_lat = g[g.index == j].lat
            cell_lon = g[g.index == j].lon
            distance = geo.distance_calc(site_lat, site_lon, cell_lat, cell_lon)
            sum_dist = sum_dist + distance
            df_cells_3.loc[df_cells_3.index == j, 'errorKm'] = distance
            df_cells_3.loc[df_cells_3.index == j, 'site_lat'] = site_lat
            df_cells_3.loc[df_cells_3.index == j, 'site_lon'] = site_lon
            
        errorKm_mean = sum_dist / site_n_cells
        condition_sites = (df_sites_2.net==i[0])&(df_sites_2.area==i[1])\
            &(df_sites_2.enbid==i[2])
        n_deleted_cells = df_sites_2[condition_sites].d_cells.values[0]
        df_sites_2.loc[condition_sites, 'errorKm_mean'] = errorKm_mean
        df_sites_2.loc[condition_sites, 'n_cells'] = site_n_cells
        df_sites_2.loc[condition_sites, 'site_lat'] = site_lat
        df_sites_2.loc[condition_sites, 'site_lon'] = site_lon
        df_sites_2.loc[condition_sites, 'd_cells'] = n_deleted_cells + 1
    #End recalculate coord. and reintroduce
    print("    End iter.: " + str(n_iter))
    
    max_errorKm = df_cells_3.sort_values('errorKm', ascending=False)\
        .head(1).errorKm.values[0]
    if max_errorKm > threshold_km:
        n_iter = n_iter + 1
        df_cells_fin, df_sites_fin = clean_clustering(df_cells_3, df_sites_2,\
                                                  n_iter, threshold_km)
    else:
        df_cells_fin = df_cells_3.copy()
        df_sites_fin = df_sites_2[df_sites_2.n_cells != 0]
        f_c_c = df_cells_fin.shape[0]
        f_c_s = df_sites_fin.n_cells.sum()
        f_s_c = df_cells_fin.groupby(['net','area','enbid']).size().shape[0]
        f_s_s = df_sites_fin.shape[0] 
        d_c_s = df_sites_fin.d_cells.sum()
        print("Final Data:")
        print("-----------DF Cells------------")
        print("Sites: " + str(f_s_c) + ", Cells: "+str(f_c_c))
        print("-----------DF Sites------------")
        print("Sites: " + str(f_s_s) + ", Cells: "+str(f_c_s))
        print("-------------Check-------------")
        print("Cells deleted from kept sites: " + str(d_c_s))
        print("-----------------------------------")
        
    return df_cells_fin, df_sites_fin

def add_band(df_ini):
    '''
    Añade la inforacion de la banda de frecuencia a cada celda, utilizando las
    correspondencias entre el cellid y la banda que proporciona la fuente de 
    datos CellMapper.
    
    Apartado TFM: "3.2.6 Calculo de la capcidad de las estaciones"

    Parameters
    ----------
    df_ini : dataframe
        celdas sin informacion de banda de frecuencia.

    Returns
    -------
    df : dataframe
        celdas con informacion de banda de frecuencia..

    '''
    df = df_ini.copy()
    print("-----------------------------------")
    print("Start adding band")
    df['band'] = 0
    #diccionarios proporcionados por CellMapper
    #MOVISTAR
    mov_dict = {1800: [10,20,30,40,50,60,70,80,1,2,3,101],\
                800: [11,21,31,41,51,61,8,9],\
                2600: [12,22,32,42,52,62],\
                2100: [14,24,34,44,54,64,202],\
                900: [13,23,33]}
    #VODAFONE
    vod_dict = {1800: [1,2,3,101,102,103,110,111,112,201,202,20330,210],\
                800: [7,8,9,120,121,122,207,208,209,11,31,216],\
                2600: [4,5,6,61,94,95,96,128,129,130,220,12,22,205],\
                2100: [18,19,20,21,14,24,34],\
                900: [73,74,75]}
    #ORANGE
    ora_dict = {1800: [10,11,12,13,14,110,111,112,113,210],\
                800: [20,21,22,23,120,121,122,123,124,216],\
                2600: [0,1,2,3,100,101,102,103,40,41,42,213],\
                2100: [30,31,32],\
                900: []}
    #YOIGO
    yoi_dict = {1800: [101,102,103,1,10],\
                800: [21],\
                2600: [5],\
                2100: [201,202,203],\
                900: []}
    all_dict = {7: mov_dict, 1: vod_dict, 3: ora_dict, 4: yoi_dict}
    for nop_key in all_dict:
        for band_key in all_dict[nop_key]:
            for i in all_dict[nop_key][band_key]:
                condition = (df.net == nop_key)&(df.cellid == i)
                df.loc[condition, 'band'] = band_key
        #condition_drop = (df.net == nop_key)&(df.band == 0)
        #df = df.drop(df[condition_drop].index)
    print("End adding band")
    print("-----------------------------------")
    return df

def df_overview(df, group_subset, title):
    '''
    Imprime en la pantalla una vision general de un dataframe de celdas.
    Informa sobre el numero de celdas y estacion por operador y por fuente de 
    datos.
    
    Apartado TFM: "3.2.9 Resumen de la infraestructura de red movil"

    Parameters
    ----------
    df : dataframe
        dataframe del que queremos saber informacion.
    group_subset : list
        columnas que definen un grupo, por ejemplo una estacion.
    title : string
        nombre que identifica al dataframe.

    Returns
    -------
    None.

    '''
    print("-----------------------------------")
    print("Start " +title+ " overview")
    
    df_mls = df[df['source'] == 'mls']
    df_oid = df[df['source'] == 'oid']
    df_mov = df[df['net'] == 7]
    df_vod = df[df['net'] == 1]
    df_ora = df[df['net'] == 3]
    df_yoi = df[df['net'] == 4]
    print("---------------------Total----------------------")
    print("DF size: " + str(df.shape[0]))
    print("-----------------")
    print("    MLS: " + str(df_mls.shape[0]))
    print("    OID: " + str(df_oid.shape[0]))
    print("-----------------")
    print("    Mov: " + str(df_mov.shape[0]))
    print("    Vod: " + str(df_vod.shape[0]))
    print("    Ora: " + str(df_ora.shape[0]))
    print("    Yoi: " + str(df_yoi.shape[0]))

    print("-------DF Grouped by: " + str(group_subset)+"------")
    print("DF size: " + str(df.groupby(group_subset).size().shape[0]))
    print("-----------------")
    print("    MLS: " + str(df_mls.groupby(group_subset).size().shape[0]))
    print("    OID: " + str(df_oid.groupby(group_subset).size().shape[0]))
    print("-----------------")
    print("    Mov: " + str(df_mov.groupby(group_subset).size().shape[0]))
    print("    Vod: " + str(df_vod.groupby(group_subset).size().shape[0]))
    print("    Ora: " + str(df_ora.groupby(group_subset).size().shape[0]))
    print("    Yoi: " + str(df_yoi.groupby(group_subset).size().shape[0]))
    
    print("End overview ")
    print("-----------------------------------")
    

def add_sites_band(df_cells_ini, df_sites_ini):
    '''
    Añade la inforacion de la banda de frecuencia a cada estacion, utilizando
    la informacion de la banda de frecuencia de cada celda.
    
    Apartado TFM: "3.2.6 Calculo de la capcidad de las estaciones"

    Parameters
    ----------
    df_cells_ini : dataframe
        celdas con informacion de la banda de frecuencia.
    df_sites_ini : dataframe
        estaciones sin informacion de la banda de frecuencia.

    Returns
    -------
    df_sites : dataframe
        estaciones con informacion de la banda de frecuencia..

    '''
    print("-----------------------------------")
    print("Start add band info to sites dataframe")
    df_cells = df_cells_ini.copy()
    df_sites = df_sites_ini.copy()
    
    df_sites['cells800'] = 0
    df_sites['cells900'] = 0
    df_sites['cells1800'] = 0
    df_sites['cells2100'] = 0
    df_sites['cells2600'] = 0
    df_sites['cells0'] = 0
    df_sites['name'] = ""
    
    for i, gc in df_cells.groupby(['net','enbid']):
        condition_sites = (df_sites.net==i[0])&(df_sites.enbid==i[1])
        n_cells_ini = df_sites.loc[condition_sites].n_cells.values[0]
        if n_cells_ini != len(gc):
            print("Error found in the site: " + str(i))
        for index, c in gc.iterrows():
            if c.band == 800:
                cells800 = df_sites[condition_sites].cells800.values[0]
                df_sites.loc[condition_sites, 'cells800'] = cells800 + 1
            elif c.band == 900:
                cells900 = df_sites[condition_sites].cells900.values[0]
                df_sites.loc[condition_sites, 'cells900'] = cells900 + 1
            elif c.band == 1800:
                cells1800 = df_sites[condition_sites].cells1800.values[0]
                df_sites.loc[condition_sites, 'cells1800'] = cells1800 + 1
            elif c.band == 2100:
                cells2100 = df_sites[condition_sites].cells2100.values[0]
                df_sites.loc[condition_sites, 'cells2100'] = cells2100 + 1
            elif c.band == 2600:
                cells2600 = df_sites[condition_sites].cells2600.values[0]
                df_sites.loc[condition_sites, 'cells2600'] = cells2600 + 1
            else:
                cells0 = df_sites[condition_sites].cells0.values[0]
                df_sites.loc[condition_sites, 'cells0'] = cells0 + 1
                
        cells800 = df_sites[condition_sites].cells800.values[0]
        cells900 = df_sites[condition_sites].cells900.values[0]
        cells1800 = df_sites[condition_sites].cells1800.values[0]
        cells2100 = df_sites[condition_sites].cells2100.values[0]
        cells2600 = df_sites[condition_sites].cells2600.values[0]
        cells0 = df_sites[condition_sites].cells0.values[0]
        n_cells_sum = cells800 + cells900 + cells1800 + cells2100 + \
                      cells2600 + cells0          
        if n_cells_sum != n_cells_ini:
            print("Error found in the site: " + str(i))
        
        if cells800 > 0:
            df_sites.loc[condition_sites,'name'] = str(cells800) + "x800 "
        if cells900 > 0:
            df_sites.loc[condition_sites,'name'] = \
                df_sites.loc[condition_sites,'name'] + str(cells900)+"x900 "
        if cells1800 > 0:
            df_sites.loc[condition_sites,'name'] = \
                df_sites.loc[condition_sites,'name'] + str(cells1800)+"x1800 "
        if cells2100 > 0:
            df_sites.loc[condition_sites,'name'] = \
                df_sites.loc[condition_sites,'name'] + str(cells2100)+"x2100 "
        if cells2600 > 0:
            df_sites.loc[condition_sites,'name'] = \
                df_sites.loc[condition_sites,'name'] + str(cells2600)+"x2600 "
        if cells0 > 0:
            df_sites.loc[condition_sites,'name'] = \
                df_sites.loc[condition_sites,'name'] + str(cells0) + \
                    "xUnknownBand"
            
    print("End add band info to sites dataframe")
    print("-----------------------------------")
    return df_sites




