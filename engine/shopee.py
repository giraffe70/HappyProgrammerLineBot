import requests
from bs4 import BeautifulSoup

def crawler_shopee(keyword):
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

keyword = 'UAG'
print(crawler_shopee(keyword))



# import time
# import requests
# import json

# def shopeeAPI_Scraper(keyword, n_items):

#     url1 = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={}&limit={}'.format(keyword,n_items)
#     headers = {'User-Agent': 'Googlebot',}
#     r = requests.get(url1,headers=headers)
#     api1_data = json.loads(r.text)
    
#     for i in range(n_items):
#         itemid = api1_data['items'][i]['itemid']
#         shopid = api1_data['items'][i]['shopid']
        
#         url2 = 'https://shopee.tw/api/v2/item/get?itemid={}&shopid={}'.format(itemid, shopid)
#         r = requests.get(url2,headers=headers)
#         api2_data = json.loads(r.text)
#         output = api1_data['items'][i]['name'].ljust(50) +': ' + str(api2_data['item']['price']//100000)
#         print(output)
#         time.sleep(0.2)
    
# shopeeAPI_Scraper(keyword = 'ssd', n_items = 10)

