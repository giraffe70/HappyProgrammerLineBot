from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
# from linebot.models import *   # vscode 有問題
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, TextMessage, ConfirmTemplate
from linebot.models import StickerSendMessage, ButtonsTemplate, ImageSendMessage, MessageAction, CarouselTemplate
from linebot.models import URIAction, PostbackAction, PostbackTemplateAction, MessageTemplateAction, CarouselColumn
from linebot.models import ImageCarouselTemplate, StickerMessage, PostbackEvent, LocationMessage

from engine.currencySearch import currencySearch, rateBot
from engine.OpenWeatherMap import OWMLonLatsearch
from engine.AQI import AQImonitor
from engine.gamma import gammamonitor
from engine.SpotifyScrap import scrapSpotify
from engine.crawlerArtical import pttSearch, bballman_news, Spotify_TOP30, rssTechNews, rssNewsLtn, crawerYahoo
from engine.OpenDataTravel import readJsonFilter, showList
from engine.shopWeb import pchome, shopee, momoshop
from engine.ibus import getRoute, getRouteID, showRouteList, showRouteResult
from engine.GoogleMapsURL import googleMapsLat, googleMapsLon
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('HappyProgrammer.json',scope)

client = gspread.authorize(creds)

LineBotSheet = client.open('happy programmer')
userStatusSheet = LineBotSheet.worksheet('userStatus')
userInfoSheet = LineBotSheet.worksheet('userInfo')

app = Flask(__name__)


# 設定你的Channel Access Token
line_bot_api = LineBotApi('kxyKN1dmIBxDNcfm6ZHFkIBbSwpN/inhArVJP6TyBqUXL1S0EmHI5R+DsgRV+GGUNrJxHwgcKi14HcXS3HYGuLYuJrkc5YCF0P/M9Wnpus3afvEi/NqcRVfWOD19LbtKmE9iGbgf5OB38wrRktwnHwdB04t89/1O/w1cDnyilFU=')
# 設定你的Channel Secret
handler = WebhookHandler('0d60d38103dc9914b0e3be902c8cf2c2')




# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	# vscode 有問題
	# app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

	userSend = event.message.text
	userID = event.source.user_id
	try:
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		# userCol = cell.col
		member = userStatusSheet.cell(cell.row,2).value
		status = userStatusSheet.cell(cell.row,3).value
	except:
		userStatusSheet.append_row([userID])
		userInfoSheet.append_row([userID])
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		# userCol = cell.col
		member = ''
		status = ''
	if member == '':
		message = TextSendMessage(text='請輸入姓名，讓我認識你！')
		userStatusSheet.update_cell(userRow, 2, '註冊中')
	elif member == '註冊中':
		userInfoSheet.update_cell(userRow, 2, userSend)
		userStatusSheet.update_cell(userRow, 2, '已註冊')
		message = TextSendMessage(text='Hi,{}'.format(userSend))

	# Google 試算表上的 status
	elif status == '旅遊查詢':
		place = readJsonFilter(userSend)
		message = TextSendMessage(text=showList(place))
		userStatusSheet.update_cell(userRow, 3, '')
	elif status == 'PChome':
		userStatusSheet.update_cell(userRow, 4, userSend)
		url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={}&page=1&sort=sale/dc'.format(userSend)
		message = TextSendMessage(text=pchome(url))
		userStatusSheet.update_cell(userRow, 3, '')
		userStatusSheet.update_cell(userRow, 4, '')
	elif status == 'Shopee':
		userStatusSheet.update_cell(userRow, 4, userSend) 
		url = 'https://shopee.tw/search?keyword={}&page=0&sortBy=relevancy'.format(userSend)
		message = TextSendMessage(text=shopee(url))
		userStatusSheet.update_cell(userRow, 3, '')
		userStatusSheet.update_cell(userRow, 4, '')
	elif status == 'momo':
		userStatusSheet.update_cell(userRow, 4, userSend) 
		url = 'https://m.momoshop.com.tw/mosearch/{}.html'.format(userSend)
		message = TextSendMessage(text=momoshop(url))
		userStatusSheet.update_cell(userRow, 3, '')
		userStatusSheet.update_cell(userRow, 4, '')
	elif status == '公車查詢0':
		userStatusSheet.update_cell(userRow, 4, userSend)
		message = TextSendMessage(text=showRouteList(userSend))
		userStatusSheet.update_cell(userRow, 3, '公車查詢1')
	elif status == '公車查詢1':
		userStatusSheet.update_cell(userRow, 5, userSend)
		userSearch = userStatusSheet.cell(userRow,4).value
		message = TextSendMessage(text=showRouteResult(userSearch,int(userSend)))
		userStatusSheet.update_cell(userRow, 3, '')
		userStatusSheet.update_cell(userRow, 4, '')
		userStatusSheet.update_cell(userRow, 5, '')
	
	elif status == '天氣查詢':
		userStatusSheet.update_cell(userRow, 4, userSend)
		userAdd = userStatusSheet.cell(userRow,4).value
		url = 'https://www.google.com/maps/search/?api=1&query={}'.format(userAdd)
		userLat = googleMapsLat(url) 
		userLon = googleMapsLon(url)
		
		weatherResult = OWMLonLatsearch(userLon,userLat)
		AQIResult = AQImonitor(userLon,userLat)
		gammaResult = gammamonitor(userLon,userLat)
		userStatusSheet.update_cell(userRow, 3, '')
		userStatusSheet.update_cell(userRow, 4, '')
		message = TextSendMessage(text='⛅天氣狀況：\n{}\n☁空氣品質：\n{}\n☀輻射值：\n{}\n'.format(weatherResult, AQIResult, gammaResult))
	

	elif member == '已註冊':
		currencyList = ['USD', 'HKD', 'GBP', 'AUD', 'CAD', 'SGD', 'CHF', 'JPY', 'ZAR', 'SEK', 'NZD', 'THB', 'PHP', 'IDR', 'EUR', 'KRW', 'VND', 'MYR', 'CNY']
		byeList = ['goodbye', 'Goodbye', '掰掰','BYE', 'bye', 'Bye', '再見','byebye']
		currency = '請輸入你要查詢的匯率：\n1.USD 2.HKD 3.GBP 4.AUD\n 5.CAD 6.SGD 7.CHF 8.JPY\n 9.ZAR  10.SEK 11.NZD 12.THB\n 13.PHP 14.IDR 15.EUR 16.KRW\n 17.VND 18.MYR 19.CNY\n'

		if userSend in ['hello', 'Hello', 'Hey', 'hey', 'Hi','hi','哈囉','你好']:
			userName = userInfoSheet.cell(cell.row,2).value
			message = TextSendMessage(text='Hello, ' + userName)
		elif userSend in ['功能', '能做甚麼', '能幹嘛', '可以幹嘛']:
			message = TextSendMessage(text='目前的功能有：\n天氣、匯率、音樂、新聞、批踢踢、圖片、旅遊景點查詢、公車路線查詢、PChome/蝦皮商品查詢、Spotify排行榜、Line內部連結')
		elif userSend in ['狀態清空', '清空', 'clean']:
			message = TextSendMessage(text='狀態已清空！')
			userStatusSheet.update_cell(userRow, 3, '')
			userStatusSheet.update_cell(userRow, 4, '')
			userStatusSheet.update_cell(userRow, 5, '')
		
		elif userSend == '匯率清單':
			message = TextSendMessage(text=currency)
		elif userSend.upper() in currencyList:
			message = TextSendMessage(text=currencySearch(userSend.upper()))
		elif userSend == '全部匯率':
			url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
			message = TextSendMessage(text=rateBot(url))

		# PTT
		elif userSend == 'PTT_NBA':
			url = 'https://www.ptt.cc/bbs/NBA/index.html'
			message = TextSendMessage(text=pttSearch(url))
		elif userSend == 'PTT_Badminton':
			url = 'https://www.ptt.cc/bbs/Badminton/index.html'
			message = TextSendMessage(text=pttSearch(url))
		elif userSend == 'PTT_Gossiping':
			url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
			message = TextSendMessage(text=pttSearch(url))
		elif userSend == 'PTT_HatePolitics':
			url = 'https://www.ptt.cc/bbs/HatePolitics/index.html'
			message = TextSendMessage(text=pttSearch(url))
		# 科技新報
		elif userSend in ['TechNews', '科技新報', '科技', 'tech', 'Tech']:
			url = 'https://technews.tw/tn-rss/'
			message = TextSendMessage(text=rssTechNews(url, 10))
		# 籃球圈
		elif userSend in ['bballman', '籃球圈' , '籃球']:
			url = 'http://www.bballman.com/category/news'
			message = TextSendMessage(text=bballman_news(url, 10))
		# 三立新聞
		elif userSend == 'ltnAll':
			url = 'https://news.ltn.com.tw/rss/all.xml'
			message = TextSendMessage(text=rssNewsLtn(url, 10))
		elif userSend == 'ltnWorld':
			url = 'https://news.ltn.com.tw/rss/world.xml'
			message = TextSendMessage(text=rssNewsLtn(url, 10))
		elif userSend == 'ltnSports':
			url = 'https://news.ltn.com.tw/rss/sports.xml'
			message = TextSendMessage(text=rssNewsLtn(url, 10))
		elif userSend == 'ltnPolitics':
			url = 'https://news.ltn.com.tw/rss/politics.xml'
			message = TextSendMessage(text=rssNewsLtn(url, 10))
		# yahoo新聞
		elif userSend == 'yahooNews':
			url = 'https://tw.yahoo.com/'
			message = TextSendMessage(text=crawerYahoo(url))

		# 傳送貼圖
		elif userSend in byeList:
			message = StickerSendMessage(package_id='11537',sticker_id='52002758')

		# Spotify 排行榜
		elif userSend == 'Spotify_global':
			url = 'https://spotifycharts.com/regional/global/daily/latest'
			message = TextSendMessage(text=Spotify_TOP30(url))
		elif userSend == 'Spotify_tw':
			url = 'https://spotifycharts.com/regional/tw/daily/latest'
			message = TextSendMessage(text=Spotify_TOP30(url))
		elif userSend == 'Spotify_us':
			url = 'https://spotifycharts.com/regional/us/daily/latest'
			message = TextSendMessage(text=Spotify_TOP30(url))
		elif userSend == 'Spotify_gb':
			url = 'https://spotifycharts.com/regional/gb/daily/latest'
			message = TextSendMessage(text=Spotify_TOP30(url))
		
		# 天氣查詢
		# elif userSend == '天氣':
		# 	# message = TextSendMessage(text='請傳入座標位置')
		# 	userStatusSheet.update_cell(userRow, 3, '天氣查詢')
		# 	message = TextSendMessage(text='請傳送你的座標')

		# 天氣查詢
		elif userSend in ['天氣', 'weather', 'Weather']:
			userStatusSheet.update_cell(userRow, 3, '天氣查詢')
			message = TemplateSendMessage(
				alt_text='天氣查詢',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://www.bviddm.com/wp-content/uploads/2015/10/weather-forecast-370x280@2x.jpg',
					title='天氣查詢',
					text='請傳送座標',
					actions=[
						URIAction(
							label='傳送我的地點',
							uri='line://nv/location'
						),
						MessageAction(
							label='手動輸入其他地址',
							text='請輸入你的地點'
						),
						PostbackAction(
							label='取消查詢',
							data='clean'
						)
					]
				)
			)

		# Confirm Template
		elif userSend == "Confirm template":     
			message = TemplateSendMessage(
				alt_text='目錄 template',
				template=ConfirmTemplate(
					title='這是ConfirmTemplate',
					text='這就是ConfirmTemplate,用於兩種按鈕選擇',
					actions=[                              
						PostbackTemplateAction(
							label='Y',
							text='Y',  # 會顯示，可以不寫 
							data='action=buy&itemid=1'
						),
						MessageTemplateAction(
							label='N',
							text='N'
						)
					]
				)
			)

		# 旅遊景點查詢
		elif userSend == '旅遊':
			userStatusSheet.update_cell(userRow, 3, '旅遊查詢')
			message = TextSendMessage(text='請輸入旅遊縣市(或地名)')
		# Pchome 商品查詢
		elif userSend in ['pchome', 'PChome', 'PCHOME', 'Pchome']:
			userStatusSheet.update_cell(userRow, 3, 'PChome')
			message = TextSendMessage(text='請輸入要搜尋的商品')
		# 蝦皮 商品查詢
		elif userSend in ['shopee', 'Shopee', 'SHOPEE', '蝦皮']:
			userStatusSheet.update_cell(userRow, 3, 'Shopee')
			message = TextSendMessage(text='請輸入要搜尋的商品')
		# momo購物 商品查詢
		elif userSend in ['momo', 'Momo', 'Momo',]:
			userStatusSheet.update_cell(userRow, 3, 'momo')
			message = TextSendMessage(text='請輸入要搜尋的商品')
		# 公車查詢
		elif userSend in ['bus', 'Bus', 'BUS', '公車']:
			userStatusSheet.update_cell(userRow, 3, '公車查詢0')
			message = TextSendMessage(text='請問要搜尋幾號公車')

		# 傳送圖片
		elif userSend == '圖片':
			message = ImageSendMessage(
			original_content_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Google_Chrome_icon_%28September_2014%29.svg/220px-Google_Chrome_icon_%28September_2014%29.svg.png',
			preview_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Google_Chrome_icon_%28September_2014%29.svg/220px-Google_Chrome_icon_%28September_2014%29.svg.png'
			)
		
		# Buttons Template
		elif userSend in ['ptt', 'Ptt', 'PTT', '批踢踢']:
			message = TemplateSendMessage(
				alt_text='PTT List',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://static.newmobilelife.com/wp-content/uploads/2018/09/Shortcuts-PTT.jpg',
					title='PTT',
					text='請選擇看版',
					actions=[
						MessageAction(
							label='NBA',
							text='PTT_NBA'
						),
						MessageAction(
							label='Badminton',
							text='PTT_Badminton'
						),
						MessageAction(
							label='Gossiping',
							text='PTT_Gossiping'
						),
						MessageAction(
							label='HatePolitics',
							text='PTT_HatePolitics'
						)
					]
				)
			)
		elif userSend == '匯率':
			message = TemplateSendMessage(
				alt_text='匯率清單',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://image.pttnews.cc/2018/11/14/ad72e3ed08/9bcfb811bb4fd8307837daa245a65e19.jpg',
					title='匯率查詢',
					text='請選擇幣別',
					actions=[
						MessageAction(
							label='查詢美金匯率',
							text='USD'
						),
						MessageAction(
							label='查詢人民幣匯率',
							text='CNY'
						),
						MessageAction(
							label='查詢全部匯率',
							text='全部匯率'
						),
						URIAction(
							label='連結網址',
							uri='https://rate.bot.com.tw/xrt?Lang=zh-TW'
						)
					]
				)
			)
		elif userSend in ['新聞', 'news', 'News']:
			message = TemplateSendMessage(
				alt_text='News List',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://www.breakingbelizenews.com/wp-content/uploads/2018/01/bbn-breaking-news.jpg',
					title='News',
					text='請選擇新聞',
					actions=[
						MessageAction(
							label='科技新報',
							text='TechNews'
						),
						MessageAction(
							label='三立新聞',
							text='set'
						),
						MessageAction(
							label='Yahoo新聞',
							text='yahooNews'
						),
						MessageAction(
							label='籃球圈',
							text='bballman'
						)
					]
				)
			)
		elif userSend in ['set', 'Set', 'SET', '三立', '三立新聞']:
			message = TemplateSendMessage(
				alt_text='Set List',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://img.vpnclub.cc/content/zh/2018/09/SET-News-Logo.jpg',
					title='Set三立新聞',
					text='請選擇新聞',
					actions=[
						MessageAction(
							label='即時',
							text='ltnAll'
						),
						MessageAction(
							label='國際',
							text='ltnWorld'
						),
						MessageAction(
							label='體育',
							text='ltnSports'
						),
						MessageAction(
							label='政治',
							text='ltnPolitics'
						)
					]
				)
			)
		elif userSend in ['spotify','Spotify','排行榜']:
			message = TemplateSendMessage(
				alt_text='Spotify Charts',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Spotify_logo_horizontal_black.jpg/1280px-Spotify_logo_horizontal_black.jpg',
					title='TOP 30',
					text='Filter by',
					actions=[
						MessageAction(
							label='GLOBAL',
							text='Spotify_global'
						),
						MessageAction(
							label='TAIWAN',
							text='Spotify_tw'
						),
						MessageAction(
							label='UNITED STATES',
							text='Spotify_us'
						),
						MessageAction(
							label='UNITED KINGDOM',
							text='Spotify_gb'
						)
					]
				)
			)
		elif userSend == '查詢':
			message = TemplateSendMessage(
				alt_text='Spotify Charts',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9XvdKuBZwx5JXqpXZN60MW5wvEScm2kzzJW76v-h45L1nd0Tr',
					title='對話式查詢',
					text='請選擇動作',
					actions=[
						MessageAction(
							label='天氣查詢',
							text='天氣'
						),
						MessageAction(
							label='公車查詢',
							text='公車'
						),
						MessageAction(
							label='購物商品查詢',
							text='購物'
						),
						MessageAction(
							label='旅遊景點查詢',
							text='旅遊'
						)
					]
				)
			)
		elif userSend in ['購物', 'shopping', 'Shopping', 'buy', 'Buy']:
			message = TemplateSendMessage(
				alt_text='Shop List',   
				template=ButtonsTemplate(
					thumbnail_image_url='https://www.stockvault.net//data/2015/11/14/181047/thumb16.jpg',
					title='購物查詢',
					text='請選擇一個平台',
					actions=[
						MessageAction(
							label='PChome線上購物',
							text='pchome'
						),
						MessageAction(
							label='MOMO購物網',
							text='momo'
						),
						MessageAction(
							label='蝦皮購物',
							text='shopee'
						)
					]
				)
			)

		# Line 內部連結：可藉由選單按鈕，並設定為URIAction，直接開啟內部連結。
		elif userSend == "內部連結":
			message = TemplateSendMessage(
				alt_text='這是個按鈕選單',
				template=ButtonsTemplate(
					thumbnail_image_url='https://s.yimg.com/ny/api/res/1.2/uylrkl1acHE34LKR7QNV9Q--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9ODAw/https://media.zenfs.com/zh-tw/nownews.com/c818263ea257c217bfcde6a924a1c3ca',
					title='內部連結',
					text='請選擇動作',
					actions=[
						URIAction(
							label='傳送我的地點',
							uri='line://nv/location'
						),
						URIAction(
							label='打開照相機',
							uri='line://nv/camera/'
						),
						URIAction(
							label='傳送單張照片',
							uri='line://nv/cameraRoll/single'
						),
						URIAction(
							label='傳送多張照片',
							uri='line://nv/cameraRoll/multi'
						)
					]
				)
			)
		
		# Carousel template：就像很多個Buttons Template，一次最多可以有10則
		elif userSend in ["安安", 'c', 'C']:
			message = TemplateSendMessage(
			alt_text='Carousel template',
			template=CarouselTemplate(
				columns=[
					CarouselColumn(
						thumbnail_image_url='https://www.breakingbelizenews.com/wp-content/uploads/2018/01/bbn-breaking-news.jpg',
						title='News List',
						text='請選擇新聞',
						actions=[
							MessageAction(
								label='科技新報',
								text='TechNews'
							),
							MessageAction(
								label='三立新聞',
								text='set'
							),
							MessageAction(
								label='Yahoo新聞',
								text='yahooNews'
							),
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://static.newmobilelife.com/wp-content/uploads/2018/09/Shortcuts-PTT.jpg',
						title='PTT',
						text='請選擇看板',
						actions=[
							MessageAction(
								label='NBA',
								text='PTT_NBA'
							),
							MessageAction(
								label='Gossiping',
								text='PTT_Gossiping'
							),
							MessageAction(
								label='HatePolitics',
								text='PTT_HatePolitics'
							)
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Spotify_logo_horizontal_black.jpg/1280px-Spotify_logo_horizontal_black.jpg',
						title='Spotify TOP 30',
						text='Filter by',
						actions=[
							MessageAction(
								label='GLOBAL',
								text='Spotify_global'
							),
							MessageAction(
								label='TAIWAN',
								text='Spotify_tw'
							),
							MessageAction(
								label='UNITED STATES',
								text='Spotify_us'
							)
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://image.pttnews.cc/2018/11/14/ad72e3ed08/9bcfb811bb4fd8307837daa245a65e19.jpg',
						title='匯率查詢',
						text='請選擇幣別',
						actions=[
							MessageAction(
								label='查詢美金匯率',
								text='USD'
							),
							MessageAction(
								label='查詢全部匯率',
								text='全部匯率'
							),
							URIAction(
								label='連結網址',
								uri='https://rate.bot.com.tw/xrt?Lang=zh-TW'
							)
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9XvdKuBZwx5JXqpXZN60MW5wvEScm2kzzJW76v-h45L1nd0Tr',
						title='對話式查詢',
						text='請選擇動作',
						actions=[
							MessageAction(
								label='購物查詢',
								text='購物'
							),
							MessageAction(
								label='公車查詢',
								text='公車'
							),
							MessageAction(
								label='旅遊景點查詢',
								text='旅遊'
							)
						]
					),
					CarouselColumn(
						thumbnail_image_url='https://s.yimg.com/ny/api/res/1.2/uylrkl1acHE34LKR7QNV9Q--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9ODAw/https://media.zenfs.com/zh-tw/nownews.com/c818263ea257c217bfcde6a924a1c3ca',
						title='內部連結',
						text='請選擇動作',
						actions=[
							URIAction(
								label='傳送我的地點',
								uri='line://nv/location'
							),
							URIAction(
								label='打開照相機',
								uri='line://nv/camera/'
							),
							URIAction(
								label='傳送單張照片',
								uri='line://nv/cameraRoll/single'
							)
						]
					)
				]
			)
		)

		# Image Carousel template：跟Carousel template很像，最多也是一次10則。大圖顯示，一則只會執行一個action
		elif userSend in ['Music','music','音樂']:
			columnReply = scrapSpotify()
			message = TemplateSendMessage(
				alt_text='Music List',
				template=ImageCarouselTemplate(
					columns=columnReply
				)
			)
		else:
			message = TextSendMessage(text=userSend)

	line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_message_StickerMessage(event):
	message = TextSendMessage(text='我看不懂貼圖')
	line_bot_api.reply_message(event.reply_token, message)

# Postback 回傳隱藏資訊
@handler.add(PostbackEvent)
def handle_message_PostbackEvent(event):
	send = event.postback.data
	userID = event.source.user_id
	cell = userStatusSheet.find(userID)
	userRow = cell.row
	if send == 'clean':
		userStatusSheet.update_cell(userRow, 3, '')
		userStatusSheet.update_cell(userRow, 4, '')
		reply = '已經取消查詢'
		message = TextSendMessage(text=reply)
	line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_message_LocationMessage(event):
	userID = event.source.user_id
	try:
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		# userCol = cell.col
		status = userStatusSheet.cell(cell.row,3).value
	except:
		userStatusSheet.append_row([userID])
		cell = userStatusSheet.find(userID)
		userRow = cell.row
		# userCol = cell.col
		status = ''
	if status == "天氣查詢":   
		# userAdd = event.message.address
		userLat = event.message.latitude
		userLon = event.message.longitude
		
		weatherResult = OWMLonLatsearch(userLon,userLat)
		AQIResult = AQImonitor(userLon,userLat)
		gammaResult = gammamonitor(userLon,userLat)
		userStatusSheet.update_cell(userRow, 3, '')
		message = TextSendMessage(text='⛅天氣狀況：\n{}\n☁空氣品質：\n{}\n☀輻射值：\n{}\n'.format(weatherResult, AQIResult, gammaResult))
	else:
		message = TextSendMessage(text='傳地址幹嘛?')
	line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)

