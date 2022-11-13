from geopy.distance import great_circle
import pandas as pd
path_file = '/home/silant/Python/goroda/goroda.csv'
nas_punkt_df = pd.read_csv(path_file)
goroda_df = nas_punkt_df[(nas_punkt_df['Тип города'] == 'г') | (nas_punkt_df['Тип региона'] == 'г')]
goroda_df = goroda_df[goroda_df['Тип н/п'] != 'г']
def city_coord(df, city, region = 'any'):
	city = city.lower()
	region = region.lower()
	index_list = []
	for i in df.index:
		if df['Город'].isna()[i] == False:
			if df.loc[i,'Город'].lower() == city and (df.loc[i,'Регион'].lower() == region or region == 'any'):
				index_list.append(i)
		elif df.loc[i,'Регион'].lower() == city and df.loc[i,'Тип региона'] == 'г' and df.loc[i,'Уровень по ФИАС'] == '1: регион':
			index_list.append(i)
	if len(index_list) == 0:
		return 0
	if len(index_list) == 1:
		i = index_list[0]
		return df.loc[i,'Широта'], df.loc[i,'Долгота']

city = None
while True:
	city = input('Введите город: ')
	if city == '':
		break
	coords = city_coord(goroda_df, city)
	if coords == 0:
		print('Нет такого города')
	elif coords != None:
		print(f'Координаты города {city}: {coords}')
	else:
		region = input('Таких городов несколько. Введите регион: ')
		coords = city_coord(goroda_df, city, region)
		if coords == 0:
			print(f'Нет города {city} в регионе {region}')
		else:
			print(f'Координаты города {city} в регионе {region}: {coords}')

