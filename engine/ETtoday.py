import requests
from bs4 import BeautifulSoup

def crawerETtoday(url):
	
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' }
	res = requests.get(url, headers=headers)
	soup = BeautifulSoup(res.text, "html.parser")
	# result = '焦點新聞：\n\n'
	result = ''
	for s in soup.select('.focus-news'):
		for focus in s.select('.box_2 h3'):
			if focus.find('a') != None:
				result += '{}\n'.format(focus.find('a').text)
				result += 'https://www.ettoday.net{}\n\n'.format(focus.find('a')['href'])

	# # result += '------------------------------\n\n及時人氣：\n\n'
	# for s in soup.select('.realtime-hot'):
	# 	for realtime in s.select('.box_2 h3'):
	# 		if realtime.find('a') != None:
	# 			if len(result) < 1990:
	# 				result += '{}\n{}\n\n'.format(realtime.find('a').text, realtime.find('a')['href'])
	return result

url = 'https://www.ettoday.net/'
print(crawerETtoday(url))


# print('焦點新聞：\n')
# for s in soup.select('.focus-news'):
# 	for focus in s.select('.box_2 h3'):
# 		if focus.find('a') != None:
# 			print(focus.find('a').text)
# 			print(focus.find('a')['href'])

# print('及時新聞：\n')
# for s in soup.select('.realtime-hot'):
# 	for realtime in s.select('.box_2 h3'):
# 		if realtime.find('a') != None:
# 			print(realtime.find('a').text)
# 			print(realtime.find('a')['href'])

