## selenium 作法慢，浪費電腦資源
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import time
# driver = webdriver.Chrome('chromedriver.exe')
# driver.get("https://ibus.tbkc.gov.tw/bus/BusRoute.aspx")
# driver.find_element_by_link_text(u"0南").click()
# driver.find_element_by_id("BackTxT").click()
# # 執行需要時間，程式寫得太密集會擷取到錯誤的東西
# time.sleep(2)
# soup = BeautifulSoup(driver.page_source, "html.parser")
# # print(soup.select('#table_stop_tbody')[0].text)
# for stop in soup.select('#table_stop_tbody tr'):
#     print('{}：{}'.format(stop.select('td')[1].text, stop.select('td')[3].text))



# 直接連伺服器的資料庫
# GetEstimateTime.ashx => Request URL: https://ibus.tbkc.gov.tw/bus/newAPI/GetEstimateTime.ashx
import requests
import json

def getRoute(routeid):
    # 按了按鈕要去請求的網址
    url ='https://ibus.tbkc.gov.tw/bus/newAPI/GetEstimateTime.ashx'
    data={'type':'web','routeid':routeid, 'lang':'Cht'}
    webContent = requests.post(url, data=data).json()

    reply = ''
    for route in webContent:
        if route['goback'] == '1':
            reply += '\n去程：\n'
        elif route['goback'] == '2':
            reply += '\n返程：\n'

        for stop in route['cometime']:
            reply += '{}：{}\n'.format(stop['stopname'], stop['cometime'])
        reply += '\n------------------------------'
    return reply



'''
Request URL: https://ibus.tbkc.gov.tw/bus/NewAPI/RealRoute.ashx

type: GetRoute
Lang: Cht

'ID': '1421', 'nameZh': '0南'
'''
def getRouteID(userSearch):
    url ='https://ibus.tbkc.gov.tw/bus/NewAPI/RealRoute.ashx'
    data={'type':'GetRoute', 'lang':'Cht'}
    webContent = requests.post(url, data=data).json()
    reply = []

    for busRoute in webContent:
        tempdict = dict()
        Name = busRoute['nameZh']
        if Name.startswith(userSearch) or ( Name[1:].startswith(userSearch) and not Name[0].isdigit() ):
            tempdict['name'] = busRoute['nameZh']
            tempdict['id'] = busRoute['ID']
            if tempdict not in reply:
                reply.append(tempdict)
    return reply

def showRouteList(userSearch):
    routeList = getRouteID(userSearch)
    result = ''
    if len(routeList) == 1:
        routeID = routeList[0]['id']
        result += routeList[0]['name']
        return result
    elif len(routeList) > 1:
        for index, route in enumerate(routeList):
            result += '{}. {}\n'.format(index+1,route['name'])
        return result
    else:
        result += '沒有這個路線'
        return result

def showRouteResult(userSelect,userSearch):
    routeList = getRouteID(userSearch)
    result = ''
    if len(routeList) == 1:
        routeID = routeList[0]['id']
        result += getRoute(routeID)
        return result

    elif len(routeList) > 1:
        routeID = routeList[userSelect-1]['id']
        result += getRoute(routeID)
        return result
    else:
        result += '沒有這個路線'
        return result



userSearch = input('請輸入查詢的路線：')
print(showRouteList(userSearch))
userSelect = int(input('\n請輸入路線的選項編號：'))
print(showRouteResult(userSelect, userSearch))

