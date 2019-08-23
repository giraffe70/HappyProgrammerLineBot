from bs4 import BeautifulSoup
import requests

# PTT
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
		title = artical.select('.title')[0].text.strip()
		date = artical.select('.date')[0].text

		# 非 "[公告] 板規v6.4" 以下的內容，且文章未被刪除
		if mark == '' and author != '-':
			if push.isdigit() and int(push) > 50 or push=='爆':
				link = artical.select('.title a')[0]['href']
				count += 1
				result += '{}\nhttps://www.ptt.cc{}\t{}\n\n'.format(title, link, date)

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
		if index == articleNumber-1:
			break
	return result

# Spotify
def Spotify_TOP30(url):
	# url = 'https://spotifycharts.com/regional'
	# url = 'https://spotifycharts.com/regional/global/daily/latest'
	webContent = requests.get(url)
	webContent.encoding ='utf-8'
	soup = BeautifulSoup(webContent.text, 'html.parser')
	result = 'Spotify Top30：\n\n'
	for index,t in enumerate(soup.select('tbody tr')):
		player = t.select('td')[3].text.split('by ')[1]
		songName = t.select('td')[3].strong.text
		# imgLink = t.select('td img')[0]['src']   # 圖片連結
		# imgLink_big = t.select('.chart-table-image a')[0]['href']

		result += '排名：{}\n'.format(t.select('td')[1].text)
		result += '歌名：{}\n'.format(songName)
		result += '歌手：{}\n'.format(player)
		# result += '歌曲連結：{}\n'.format(imgLink_big)
		# download(bigImgLink(imgLink_big), clearName(songName))   # 下載圖片
		
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
		if index == articleNumber-1:
			break
	return result

# Yahoo新聞
def crawerYahoo(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	result = ''
	index = 1
	for s in soup.select(".Story-Item"):
		if s.find('span',class_='Va-tt') != None:
			if len(result) < 1800 and index <= 30:
				# result += '{}\n{}\n\n'.format(s.find('span',class_='Va-tt').text, s.find('a')['href'])
				result += '{}. {}\n'.format(index, s.find('span',class_='Va-tt').text)
				index += 1
			else:
				break
	return result

