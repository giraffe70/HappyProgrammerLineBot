from bs4 import BeautifulSoup
import requests

# ptt
def pttSearch(url, count=0, result=''):
	# webContent = requests.get(url)
	# webContent = requests.get(url,cookies={'over18':'1'})
	webContent = requests.post(url,cookies={'over18':'1'})
	webContent.encoding ='utf-8'
	soup = BeautifulSoup(webContent.text, 'html.parser')
	for artical in soup.select('.r-ent'):
		mark = artical.select('.mark')[0].text
		author = artical.select('.author')[0].text
		push = artical.select('.nrec')[0].text
		title = artical.select('.title')[0].text
		date = artical.select('.date')[0].text

		# 非 "[公告] 板規v6.4" 以下的內容，且文章未被刪除
		if mark == '' and author != '-':
			if push.isdigit() and int(push) > 50 or push=='爆':
				link = artical.select('.title a')[0]['href']
				count += 1
				result += '{}https://www.ptt.cc{}\t{}\n\n'.format(title, link, date)
				# result += '\n------------------------------------------------------------\n'

	if count < 10:
		paging = soup.select('div .btn-group-paging a')
		next_url = 'https://www.ptt.cc' + paging[1]['href']
		return pttSearch(next_url, count, result)
	
	return result

	

# 籃球圈
def bballman_news(url, articleNumber):
	webContent = requests.get(url)
	webContent.encoding ='utf-8'
	soup = BeautifulSoup(webContent.text ,  'html.parser')
	result = ''
	for index,row in enumerate(soup.select('.ajax-load-con')):
		if row.a != None:
			result += row.select('a')[0]['title'] + '\n'
			result += row.select('a')[0]['href'] + '\n\n'
			# result += '\n-----------------------------------------------------------------\n'
		if index == articleNumber-1:
			break
	return result

# spotify
def spotifyTop30(url):
	# url = 'https://spotifycharts.com/regional'
	webContent = requests.get(url)
	webContent.encoding ='utf-8'
	soup = BeautifulSoup(webContent.text, 'html.parser')
	result = 'Spotify Top30：\n\n'
	for index,t in enumerate(soup.select('tbody tr')):
		player = t.select('td')[3].text.split('by ')[1]
		songName = t.select('td')[3].strong.text
		imgLink = t.select('td img')[0]['src']
		imgLink_big = t.select('.chart-table-image a')[0]['href']

		result += '排名：{}\n'.format(t.select('td')[1].text)
		result += '歌名：{}\n'.format(songName)
		# result += '歌手：{}\n圖片連結：{}\n'.format(player, imgLink)
		result += '歌手：{}\n'.format(player)
		# result += '歌曲連結：{}\n'.format(imgLink_big)
		# result += '-------------------------------------------------------\n'
		# 下載圖片
		# download(bigImgLink(imgLink_big), clearName(songName))
		
		if index == 29:
			break
	return result

# TechNews
def rssTechNews(url, articleNumber):
	webContent = requests.get(url)
	rss_feed = BeautifulSoup(webContent.text, 'xml')
	result = ''
	for index, news in enumerate(rss_feed.select('item')):
		result += news.find('title').text + '\n'
		result += news.find('link').text + '\n\n'
		# result += news.find('pubDate').text + '\n'
		# result += '------------------------------------------------------------\n'
		if index == articleNumber-1:
			break
	return result

# 三立新聞
def rssNewsLtn(url, articleNumber):
	webContent = requests.get(url)
	rss_feed = BeautifulSoup(webContent.text, 'xml')
	result = ''
	for index, news in enumerate(rss_feed.select('item')):
		result += news.find('title').text + '\n'
		result += news.find('link').text + '\n\n'
		# result += news.find('pubDate').text + '\n'
		# result += '------------------------------------------------------------\n'

		if index == articleNumber-1:
			break
	return result


# webOption = int(input('[1].PTT  [2].籃球圈  [3].Spotify  [4].TechNews [5].三立新聞\n想要看什麼：'))
# if webOption == 1:
# 	SectionInput = int(input("[1].NBA  [2].Badminton  [3].HatePolitics  [4].movie  [5].joke [6].Gossiping\n請輸入要搜尋的版："))
# 	# numberInput = int(input("選擇要顯示的篇數："))
# 	SectionList = ['NBA', 'Badminton', 'HatePolitics', 'movie', 'joke', 'Gossiping']
# 	url = 'https://www.ptt.cc/bbs/{}/index.html'.format(SectionList[SectionInput-1])
# 	print(pttSearch(url))
# elif webOption == 2:
# 	url = 'http://www.bballman.com/category/news'
# 	print(bballman_news(url))
# elif webOption == 3:
# 	url = 'https://spotifycharts.com/regional'
# 	print(spotify_top30(url))
# elif webOption == 4:
# 	url = 'https://technews.tw/tn-rss/'
# 	print(rssTechNews(url))
# elif webOption == 5:
# 	SectionInput = int(input("[1].即時  [2].國際  [3].體育  [4].政治 [5].財經\n請輸入要搜尋的版："))
# 	SectionList = ['all', 'world', 'sports', 'politics', 'business']
# 	numberInput = int(input("選擇要顯示的篇數："))
# 	print(rssNewsLtn('https://news.ltn.com.tw/rss/{}.xml'.format(SectionList[SectionInput-1]), numberInput))
# else:
# 	print('請輸入數字')

