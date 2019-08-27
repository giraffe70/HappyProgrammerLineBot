import requests
from bs4 import BeautifulSoup
import json

def pchome(url):
	# url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page=1&sort=sale/dc'.format(userSearch) 
	webContent = requests.get(url)
	data = json.loads(webContent.text)
	result = ''
	webdatas = data['prods']
	for index,product in enumerate(webdatas):
		result += '{}. {}\t${}\n'.format(index+1, product['name'], product['price'])
	return result

def shopee(keyword):
	# url = 'https://shopee.tw/search?keyword={}&page=0&sortBy=relevancy'.format(keyword) # 綜合排名
	# url = 'https://shopee.tw/search?keyword={}&page=0&sortBy=ctime'.format(keyword)     # 最新
	# url = 'https://shopee.tw/search?keyword={}&page=0&sortBy=sales'.format(keyword)     # 最熱銷
	url = "https://shopee.tw/search?keyword={}&page=0&sortBy=relevancy".format(keyword)  

	headers = {
		'User-Agent': 'Googlebot',
		'From': '1061241239@nkust.edu.tw'
	}
		
	res = requests.get(url,headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')

	index = 1
	result = ''

	for s in soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item"):  # _1Ewdcf
		name = s.find_all("div", class_="_1NoI8_ _2gr36I")[0].text
		price = s.find_all("div", class_="_1w9jLI _37ge-4 _2XtIUk")[0].text
		# link = s.find_all("a")[0]['href']
		if len(result) < 1900:
			result += '{}. {}\t{}\n'.format(index, name, price)
			index += 1
	return result


def momoshop(url):
	# 騙過伺服器，我們是來自一個正常的瀏覽器
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
	}

	webContent = requests.get(url, headers=headers)
	soup = BeautifulSoup(webContent.text, 'html.parser')
	result = ''
	for index, product in enumerate(soup.select('#itemizedStyle li')):
		title = product.select('.prdName')[0].text
		price = product.select('.price')[0].text
		result += '{}{}\t{}\n'.format(index+1, title, price)
		
	return result


# userSearch = 'ssd'
# url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page=1&sort=sale/dc'.format(userSearch)
# print(pchome(url))
