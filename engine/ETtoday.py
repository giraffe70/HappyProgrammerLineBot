import requests
from bs4 import BeautifulSoup

def crawerETtoday(url):
	res = requests.get(url)
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

