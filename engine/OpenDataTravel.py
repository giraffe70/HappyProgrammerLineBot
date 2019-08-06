import requests
import json
# from OpenWeatherMap import OWMLonLatsearch
# from gamma import gammamonitor
# from AQI import AQImonitor

# 景點 - 觀光資訊資料庫
# https://data.gov.tw/dataset/7777
# http://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json

#使用Json模組來讀取檔案物件
#load()讀取方法、dump()寫入方法
def readJsonFilter(userInput):

	file = open('scenic_spot_C_f.json',mode='r',encoding='utf-8-sig')
	data = json.load(file) #把JSON檔轉成dictionary類別

	# url = 'http://gis.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json'
	# data = requests.get(url).json()
	

	filterList = []
	filterDict = []

	for shop in data['XML_Head']['Infos']['Info']:
		if userInput in shop['Add']:
			#串列
			temp = []
			temp.append(shop['Name'])
			temp.append(shop['Add'])
			temp.append(shop['Tel'])
			temp.append(shop['Px'])
			temp.append(shop['Py'])
			filterList.append(temp)

			#字典
			tempDict = dict()
			tempDict['景點名稱'] = shop['Name']
			tempDict['地址'] = shop['Add']
			tempDict['電話'] = shop['Tel']
			tempDict['經度'] = shop['Px']
			tempDict['緯度'] = shop['Py']
			filterDict.append(tempDict)
			
	#輸出JSON檔
	# file = open('xxxx.json',mode='w',encoding='utf-8')
	# data = json.dump(filterDict, file, ensure_ascii=False)
	# file.close()

	return filterDict


def showList(filterDict):
	result = ''
	for index,place in enumerate(filterDict):
		result += '{}. {}\n'.format(index+1,place['景點名稱'])
		if len(result) > 1999:
			break
	return result

def showResult(userSelect):
	result = ''
	place = filterDict[userSelect-1]
	weather = OWMLonLatsearch(place['經度'],place['緯度'])
	gammaResult = gammamonitor(place['經度'],place['緯度'])
	aqiResult = AQImonitor(place['經度'],place['緯度'])
	result += '景點名稱：{}\n地址：{}\n電話：{}\n\n天氣狀況：\n{}\n'.format(place['景點名稱'],place['地址'],place['電話'],weather)
	result += '輻射值：\n' + gammaResult + '\n'
	result += '空氣品質：\n' + aqiResult
	return result


# filterDict = readJsonFilter(input('請輸入旅遊縣市：'))
# print(showList(filterDict))
# print(len(showList(filterDict)))
# userSelect = int(input('請輸入選項：'))
# print(showResult(userSelect))
