from geopy.distance import great_circle
import pandas as pd
path_file = '/home/silant/Python/games/goroda/goroda.csv'
nas_punkt_df = pd.read_csv(path_file)
goroda_df = nas_punkt_df[(nas_punkt_df['Тип города'] == 'г') | (nas_punkt_df['Тип региона'] == 'г')]
goroda_df = goroda_df[goroda_df['Тип н/п'] != 'г']
big_cities_df = goroda_df[goroda_df['Население'] > 50000]

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

def city_info(df, param, city, region = 'any'):
	"""Выдаёт параметры param для города"""
	param = param.capitalize()
	if param not in df.columns:
		return None
	index_list = city_indices(df, city, region = 'any')
	ret = []
	for i in index_list:
		if df[param].isna()[i] == False:
			ret.append(df.loc[i,param])
	return ret


def city_coord(df, city, region = 'any'):
	"""Выдаёт координаты города (0 -- если города нет, None -- если городов несколько)"""
	index_list = city_indices(df, city, region)
	if len(index_list) == 0:
		return 0
	if len(index_list) == 1:
		i = index_list[0]
		return df.loc[i,'Широта'], df.loc[i,'Долгота']

def city_full_name(df, city, region = 'any'):
	"""Имя города с регионом"""
	city = city.capitalize()
	index_list = city_indices(df, city, region)
	ret = []
	for i in index_list:
		region = df.loc[i,'Регион']
		region_type = df.loc[i, 'Тип региона']
		if region_type == 'Респ':
			region_name = ' (Республика ' + region + ')'
		elif region_type == 'Чувашия':
			region_name = ' (' + region + ')'
		elif region_type == 'г':
			region_name = ' (город федерального значения)'
		else:
			region_name = ' (' + region + ' ' + region_type + ')'
		ret.append(city + region_name)
	return ret

def city_region_by_index(df, i):
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
	return great_circle(coor_i,coor_j)

def nearst_cities(df,i, n = 3):
#	indices = list(df.index)
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


df = big_cities_df
n = 10
indices = list(df.index)
city = 'Москва'
i = city_indices(df,city)[0]
while True:
	region = df.loc[i,'Регион']
#	city_region = city_full_name(df, city, region)
	city_region = city_region_by_index(df,i)
	print(f'Вы находитесь в городе {city_region}: {coords_by_ind(df, i)}')
	nearst = nearst_cities(df, i, n)
	print('Выберете ближайший город:')
	cities = []
	for k in range(n):
		j = nearst[k]
		print(f'{k} \u2014 {city_region_by_index(df,j)}: ({coords_by_ind(df, j)[0]:.2f}, {coords_by_ind(df, j)[1]:.2f})')
	
	print(f'q \u2014 выход')
	while True:
		choice = input('Ваш выбор:')
		if choice == 'q':
			break
		try:
			k = int(choice)
		except:
			continue
		if k in range(n):
			break

	if choice == 'q':
		break

	i = nearst[k]

