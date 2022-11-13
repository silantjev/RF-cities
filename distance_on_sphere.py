from geopy.distance import great_circle
import pandas as pd
path_file = '/home/silant/Python/goroda/goroda.csv'
nas_punkt_df = pd.read_csv(path_file)

goroda_df = nas_punkt_df[nas_punkt_df['Тип города'] == 'г']
goroda_df = goroda_df[goroda_df['Тип н/п'] != 'г']
#d = great_circle((40.7128, 74.0060), (31.9686, 99.9018))
# print(d)
def city_coord(df, city, region = 'any'):
	city = city.lower()
	region = region.lower()
	index_list = []
	for i in df.index:
		if df.loc[i,'Город'].lower() == city and (df.loc[i,'Регион'].lower() == region or region == 'any'):
			index_list.append(i)
	if len(index_list) == 0:
		return 0
	if len(index_list) == 1:
		i = index_list[0]
		return df.loc[i,'Широта'], df.loc[i,'Долгота']

#kazan = city_coord(goroda_df, 'Казань')
#print(kazan)
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

