import requests
from bs4 import BeautifulSoup
# url = 'https://acg.gamer.com.tw/billboard.php?t=2&p=PC'
def acgGamer(url):
	webContent = requests.get(url)
	webContent.encoding ='utf-8'

	soup = BeautifulSoup(webContent.text, 'html.parser')
	result = ''
	for game in soup.select('.ACG-mainbox1'):
		result += game.select('.ACG-maintitle')[0].text + '\n'
		result += game.select('.ACG-mainplay')[0].text + '\n'
		result += game.select('.ACG-mainboxpoint')[0].text + '\n\n'
	return result
# print(acgGamer(url))
