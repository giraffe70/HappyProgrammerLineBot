import requests
from bs4 import BeautifulSoup

# url = 'http://www.bballman.com/' 
def scrapArtical(url='http://www.bballman.com/category/news'):
 	
	webContent = requests.get(url)
	webContent.encoding ='utf-8'
	soup = BeautifulSoup(webContent.text ,  'html.parser')

	# for row in soup.select('div .index-cat-box a'):
	# 	print(row['title'])
	# 	print(row['href'])
	result = ''
	for row in soup.select('.ajax-load-con'):
		if row.a != None:
			result += row.select('a')[0]['title'] + '\n'
			result += row.select('a')[0]['href']
			result += '\n------------------------------------------------------------\n'
	return result


# url = 'http://www.bballman.com/category/news'
# print(scrapArtical())

