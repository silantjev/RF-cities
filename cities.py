# Это файл с функциями, необходимыми для игры.

import os
from geopy.distance import great_circle
import pandas as pd


def df_city_load(POP = 200000):
    path_dir = os.path.dirname(__file__)
    path_file =  os.path.join(path_dir, 'goroda.csv')
    nas_punkt_df = pd.read_csv(path_file)
    goroda_df = nas_punkt_df[(nas_punkt_df['Тип города'] == 'г') | (nas_punkt_df['Тип региона'] == 'г')]
    goroda_df = goroda_df[goroda_df['Тип н/п'] != 'г']
    big_cities_df = goroda_df[goroda_df['Население'] > POP] # Оставляем города с населением > POP
    big_cities_df = big_cities_df[big_cities_df['Регион'] != 'Московская'] # Удалим города из московской области, иначе нас будет сюда затягивать

    return big_cities_df    


def city_indices(df, city, region = 'any'):
    """Ищет город city (в регионе region) в датафрейме df"""
    city = city.capitalize()
    region = region.capitalize()
    index_list = []
    for i in df.index:
        if df['Город'].isna()[i] == False:
            if df.loc[i,'Город'].capitalize() == city and (df.loc[i,'Регион'].capitalize() == region or region == 'Any'):
                index_list.append(i)
        elif df.loc[i,'Регион'].capitalize() == city and df.loc[i,'Тип региона'] == 'г' and df.loc[i,'Уровень по ФИАС'] == '1: регион':
            index_list.append(i)
    return index_list

def city_region_by_index(df, i):
    """Возвращает город и регион по индексу"""
    region = df.loc[i,'Регион']
    region_type = df.loc[i, 'Тип региона']
    if region_type == 'г' and df.loc[i,'Уровень по ФИАС'] == '1: регион':
        return region + ' (город федерального значения)'
    city = df.loc[i,'Город']
    if region_type == 'Респ':
        return city + ' (Республика ' + region + ')'
    if region_type == 'Чувашия':
        return city + ' (' + region + ')'
    return city + ' (' + region + ' ' + region_type + ')'

def coords_by_ind(df,i):
    return df.loc[i,'Широта'], df.loc[i,'Долгота']

def dist(df,i,j):
    coor_i = coords_by_ind(df, i)
    coor_j = coords_by_ind(df, j)
    return great_circle(coor_i,coor_j).km

def nearst_cities(df,i, n = 3):
    """Возвращает индексы для n ближайших городов"""
    indices = list(df.index)
    indices.remove(i)
    distances = dict()
    for j in indices:
        distances[j] = dist(df, i, j)
    l = len(indices)
    for k in range(0,n):
        for j in range(l-1,k,-1):
            if distances[indices[j-1]] > distances[indices[j]]:
                indices[j], indices[j-1] = indices[j-1], indices[j]
    return indices[:n]


