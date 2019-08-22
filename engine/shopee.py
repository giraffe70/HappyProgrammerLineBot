import requests
from bs4 import BeautifulSoup

def crawler_shopee(keyword):
	# url = 'https://shopee.tw/search?keyword={}&page=0&sortBy=relevancy'.format(keyword) # 綜合排名
	# url = 'https://shopee.tw/search?keyword={}&page=0&sortBy=sales'.format(keyword)  # 最熱銷
	url = 'https://shopee.tw/search?keyword={}&page=0&sortBy=relevancy'.format(keyword)  

	headers = {
		'User-Agent': 'Googlebot',	
	}
		
	res = requests.get(url,headers=headers)
	soup = BeautifulSoup(res.text, 'html.parser')

	result = ''
	for s in soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item"):  # _1Ewdcf
		name = s.find_all("div", class_="_1NoI8_ _2gr36I")[0].text
		price = s.find_all("div", class_="_1w9jLI _37ge-4 _2XtIUk")[0].text
		link = s.find_all("a")[0]['href']
		result += '{}\n{}\nhttps://shopee.tw/{}\n\n'.format(name, price, link)
	return result
 
# sortby = 'relevancy' # 綜合排名
# sortby = 'ctime'   # 最新
# sortby = 'sales'   # 最熱銷
# keyword = 'UAG'
# print(crawler_shopee(keyword))
