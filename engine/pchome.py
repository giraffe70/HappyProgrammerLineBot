import requests
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

userSearch = 'ssd'
url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page=1&sort=sale/dc'.format(userSearch)
print(pchome(url))
