from geopy.distance import great_circle
import pandas as pd
path_file = '/home/silant/Python/goroda/goroda.csv'
nas_punkt_df = pd.read_csv(path_file)
goroda_df = nas_punkt_df[(nas_punkt_df['Тип города'] == 'г') | (nas_punkt_df['Тип региона'] == 'г')]
goroda_df = goroda_df[goroda_df['Тип н/п'] != 'г']

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

while True:
	city = input('Введите город: ')
	if city == '':
		break
	city = city.capitalize()
	coords = city_coord(goroda_df, city)
	if coords == 0:
		print('Нет такого города')
	elif coords != None:
		#region = city_info(goroda_df, 'Регион', city)[0]
		#region_type = city_info(goroda_df, 'Тип региона', city)[0]
		city_full = city_full_name(goroda_df, city)[0]
		print(f'Координаты города {city_full}: {coords}')
	else:
		regions = city_info(goroda_df, 'Регион', city)
		print(f'Город {city} есть в следующих регионах: ')
		for r in regions:
			print(r,end =' ')
		region = input('\nВведите регион: ')
		region = region.capitalize()
		coords = city_coord(goroda_df, city, region)
		if coords == 0:
			print(f'Нет города {city} в регионе {region}')
		else:
			city_full = city_full_name(goroda_df, city, region)[0]
			print(f'Координаты города {city_full}: {coords}')

