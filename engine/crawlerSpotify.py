import requests
from bs4 import BeautifulSoup
import random

# def download(link,songName):
# 	image = requests.get(link)
# 	file = open('./download/{}.jpg'.format(songName), mode='wb')
# 	file.write(image.content)
# 	file.close()

# def clearName(songName):
# 	newName = ''
# 	for word in songName:
# 		if word.isalpha() or word == ' ':
# 			newName += word
# 	return newName

def bigImgLink(bigImgL):
	songContent = requests.get(bigImgL)
	soup = BeautifulSoup(songContent.text,'html.parser')
	newImgLink = 'https:'+ soup.select('.cover-art-image')[0]['style'].split('url(')[1].split(')')[0]
	return newImgLink

def scrapSpotify():
	url = 'https://spotifycharts.com/regional'
	webContent = requests.get(url)
	# webContent.encoding ='utf-8'
	soup = BeautifulSoup(webContent.text, 'html.parser')
	songReplyList = []
	for index,t in enumerate(soup.select('tbody tr')):
		player = t.select('td')[3].text.split('by ')[1]
		songName = t.select('td')[3].strong.text
		imgLink = t.select('td img')[0]['src']
		imgLink_big = t.select('.chart-table-image a')[0]['href']
		imgLink = bigImgLink(bigImgL)
		songReplyList.append([player,songName,imgLink])
		# print('排名：{}'.format(t.select('td')[1].text))
		# # print('歌名：{}'.format(t.select('td')[3].text.split('by')[0]))
		# print('歌名：{}'.format(songName))
		# print('歌手：{}圖片連結：{}'.format(player, imgLink))
		# print('歌曲連結：{}\n'.format(imgLink_big))
		# print('--------------------------------------------------')
		# 下載圖片
		# download(bigImgLink(imgLink_big), clearName(songName))
		
		if index == 29:
			break
