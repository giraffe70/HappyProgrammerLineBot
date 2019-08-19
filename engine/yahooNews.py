import requests
from bs4 import BeautifulSoup

def crawerYahoo(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	result = ''
	for s in soup.select(".Story-Item"):
		if s.find('span',class_='Va-tt') != None:
			result += '{}\n{}\n\n'.format(s.find('span',class_='Va-tt').text, s.find('a')['href'])
			# result += s.find('a')['href']
	return result

# url = 'https://tw.yahoo.com/'
# print(crawerYahoo(url))
