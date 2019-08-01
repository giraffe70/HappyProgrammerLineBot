import twder

def twder_result(userInput):
	result = twder.now(userInput)
	text = ''
	# text += '時間：{}\n現金買入：{}\n現金賣出：{}\n即期買入：{}\n即期賣出：{}\n'.format(result[0], result[1], result[2], result[3],result[4])
	text += '時間：{}\n即期買入：{}\n即期賣出：{}\n'.format(result[0], result[3], result[4])
	return text

print(twder.currencies())
userInput = input("請輸入幣別(大寫)：")
print(twder_result(userInput))