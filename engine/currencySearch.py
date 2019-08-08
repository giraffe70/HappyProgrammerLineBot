import twder

def currencySearch(search):
	# result = twder.now(userInput)
	# text = ''
	# # text += '時間：{}\n現金買入：{}\n現金賣出：{}\n即期買入：{}\n即期賣出：{}\n'.format(result[0], result[1], result[2], result[3],result[4])
	# text += '時間：{}\n即期買入：{}\n即期賣出：{}\n'.format(result[0], result[3], result[4])
	# return text
	
	dollorTuple = twder.now_all()[search]
	reply = '日期：{}\n即期賣出價：{}\n即期買入：{}'.format(dollorTuple[0], dollorTuple[4])
	return reply



# print(twder.currencies())
# userInput = input("請輸入幣別(大寫)：")
# print(twder_result(userInput))