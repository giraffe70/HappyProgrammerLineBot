import requests
from bs4 import BeautifulSoup

userAdress = '高雄市苓雅區和平一路116號'
url = 'https://www.google.com/maps/search/?api=1&query={}'.format(userAdress)

def googleMapsURL(url):
	webContent = requests.get(url)
	soup = BeautifulSoup(webContent.text,'lxml')
	coord = soup.findAll('meta',{'itemprop':'image'})[0]['content'].split('center=')[1].split('&')[0]
	lat = coord.split('%2C')[0]
	lon = coord.split('%2C')[1]
	return lat + ' ' + lon

print(googleMapsURL(url))


# import requests
# from bs4 import BeautifulSoup
# option = '牛肉麵'
# userAdress = '高雄'
# url = 'https://www.google.com/maps/search/?api=1&query={}+{}'.format(option, userAdress)

# webContent = requests.get(url)
# webContent.encoding ='utf-8'
# soup = BeautifulSoup(webContent.text,'html.parser')

# coord = soup.findAll('meta',{'itemprop':'image'})[0]['content'].split('center=')[1].split('&')[0]
# lat = coord.split('%2C')[0]
# lon = coord.split('%2C')[1]




