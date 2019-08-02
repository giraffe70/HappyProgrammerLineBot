import requests
import time  

#函式封裝
def OWMsearch(city):
	'''
	輸入英文城市名
	以字串型別輸出特定城市天氣資訊
	'''
	URL = 'https://api.openweathermap.org/data/2.5/weather?APPID=769273dc9180b5e5c3c2deb706666aa4&q={}&units=metric&lang=zh_tw'.format(city)
	try:
		r = requests.get(URL).json()
		result = ''
		if r['cod'] == 200:
			result += ('經度：{}\t緯度：{}\n'.format(r['coord']['lon'],r['coord']['lat']))
			result += ('天氣狀況：{}\n'.format(r['weather'][0]['description']))
			result += ('溫度：{}\n最高溫：{}\t最低溫：{}\n'.format(r['main']['temp'],r['main']['temp_max'],r['main']['temp_min']))
			result += ('風速：{}\n'.format(r['wind']['speed']))
			result += '日出時間：{}\n'.format(time.strftime('%H:%M:%S', time.localtime(r['sys']['sunrise'])))
			result += '日落時間：{}\n'.format(time.strftime('%H:%M:%S', time.localtime(r['sys']['sunset'])))
		elif r['cod'] == '404':
			result += r['message']
	except:
		result = '連不上伺服器'

	return result

def OWNrectSeach():
	URL = 'http://api.openweathermap.org/data/2.5/box/city?bbox=120.14,22.48,120.86,23.60,10&APPID=769273dc9180b5e5c3c2deb706666aa4&lang=zh_tw'
	webContent = requests.get(URL).json()
	result = ''
	for city in webContent['list']:
		result += city['name']+'\n'
		result += ('經度：{}\t緯度：{}\n'.format(city['coord']['Lon'],city['coord']['Lat']))
		result += '天氣狀況：{}\n'.format(city['weather'][0]['description'])

	return result

def OWMLonLatsearch(lon,lat):
	'''
	輸入英文城市名
	以字串型別輸出特定城市天氣資訊
	'''
	URL = 'https://api.openweathermap.org/data/2.5/weather?APPID=769273dc9180b5e5c3c2deb706666aa4&lon={}&lat={}&units=metric&lang=zh_tw'.format(lon,lat)
	try:
		r = requests.get(URL).json()
		result = ''
		if r['cod'] == 200:
			result += ('經度：{}\t緯度：{}\n'.format(r['coord']['lon'],r['coord']['lat']))
			result += ('天氣狀況：{}\n'.format(r['weather'][0]['description']))
			result += ('溫度：{}\n最高溫：{}\t最低溫：{}\n'.format(r['main']['temp'],r['main']['temp_max'],r['main']['temp_min']))
			result += ('風速：{}\n'.format(r['wind']['speed']))
			result += '日出時間：{}\n'.format(time.strftime('%H:%M:%S', time.localtime(r['sys']['sunrise'])))
			result += '日落時間：{}\n'.format(time.strftime('%H:%M:%S', time.localtime(r['sys']['sunset'])))
		elif r['cod'] == '404':
			result += r['message']
	except:
		result = '連不上伺服器'

	return result