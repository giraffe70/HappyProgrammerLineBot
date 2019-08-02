import requests
from geopy.distance import geodesic
import json

# 空氣品質指標(AQI)
# https://data.gov.tw/dataset/40448

def AQImonitor(lon,lat):
	url = 'https://quality.data.gov.tw/dq_download_json.php?nid=40448&md5_url=05c834d071ad5b62eaf85658de4d2e6f'
	r = requests.get(url).json()
	
	distance = 1000000

	placeTuple = (lat,lon) #觀光地點的經緯度
	for row in r:
		stationTuple = (row['Latitude'], row['Longitude']) #監測站的經緯度
		if row['Status'] != '設備維護':
			if geodesic(placeTuple,stationTuple).km < distance:
				distance = geodesic(placeTuple,stationTuple).km
				row['AQI'] = int(row['AQI'])
				if row['AQI'] <= 50:
					row['AQI'] = '綠色'
				elif 50 < row['AQI'] <= 100:
					row['AQI'] = '黃色'
				elif 100 < row['AQI'] <= 150:
					row['AQI'] = '橘色'
				elif 150 < row['AQI'] <= 200:
					row['AQI'] = '紅色'
				elif 200 < row['AQI'] <= 250:
					row['AQI'] = '紫色'
				elif 251 <= row['AQI']:
					row['AQI'] = '棗紅色'
				result = [row['AQI'],row['PM2.5'],row['PM10']]
	result = '{}警戒\nPM2.5：{}\nPM10：{}\n'.format(result[0], result[1], result[2])
	return result