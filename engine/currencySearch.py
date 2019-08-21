import twder
import requests
from bs4 import BeautifulSoup
def currencySearch(search):
	# result = twder.now(userInput)
	# text = ''
	# # text += '時間：{}\n現金買入：{}\n現金賣出：{}\n即期買入：{}\n即期賣出：{}\n'.format(result[0], result[1], result[2], result[3],result[4])
	# text += '時間：{}\n即期買入：{}\n即期賣出：{}\n'.format(result[0], result[3], result[4])
	# return text
	
	dollorTuple = twder.now_all()[search]
	reply = '日期：{}\n即期賣出：{}\n即期買入：{}'.format(dollorTuple[0], dollorTuple[4], dollorTuple[3])
	return reply


def rateBot(url):
	webContent = requests.get(url)
	webContent.encoding ='utf-8'
	soup = BeautifulSoup(webContent.text, 'html.parser')
	# 找尋所有table
	data1 = soup.find("table",{"class","table table-striped table-bordered table-condensed table-hover"})
	# 幣別名稱
	data_name = data1.find_all("div",{"class","hidden-phone print_show"})
	# 即期買入、即期賣出
	data2 = data1.find_all("td",{"class","rate-content-sight text-right print_hide"})

	result = ''
	for n in range(0, len(data_name)):
		if data2[n*2].text != '-':
			result += '{}\n'.format(data_name[n].text.strip())
			result += '即期買入：{}\n'.format(data2[n*2].text)
			result += '即期賣出：{}\n\n'.format(data2[n*2+1].text)
	return result

# print(twder.currencies())
# userInput = input("請輸入幣別(大寫)：")
# print(currencySearch(userInput))