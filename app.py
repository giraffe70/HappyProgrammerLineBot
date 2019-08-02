from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from engine.currencySearch import *
from engine.OpenWeatherMap import OWMLonLatsearch
from engine.AQI import AQImonitor
from engine.gamma import gammamonitor

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
    app.logger.info("Request body: " + body)
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
    userId = event.source.user_id

    currencyList = ['USD', 'HKD', 'GBP', 'AUD', 'CAD', 'SGD', 'CHF', 'JPY', 'ZAR', 'SEK', 'NZD', 'THB', 'PHP', 'IDR', 'EUR', 'KRW', 'VND', 'MYR', 'CNY']
    USDlist = ['美金', '美元', 'USD', 'usd', 'Usd', '美']
    byeList = ['goodbye', 'good bye', 'Good bye', 'Goodbye', '掰掰','BYE', 'bye', 'Bye', '再見','byebye']
    currency = '請輸入你要查詢的匯率：\n1.USD 2.HKD 3.GBP 4.AUD\n 5.CAD 6.SGD 7.CHF 8.JPY\n 9.ZAR  10.SEK 11.NZD 12.THB\n 13.PHP 14.IDR 15.EUR 16.KRW\n 17.VND 18.MYR 19.CNY\n'
    sayHelloList = ['hello', 'Hello', 'Hey', 'hey', 'Hi','hi','哈囉','你好']

    if userSend in sayHelloList:
        message = TextSendMessage(text='Hello, ' + userId)
    elif userSend == '匯率':
        message = TextSendMessage(text=currency)
    elif userSend in USDlist:
        message = TextSendMessage(text=currencySearch('USD'))
    elif userSend in currencyList:
        message = TextSendMessage(text=currencySearch(userSend))
    elif userSend in byeList:
        message = StickerSendMessage(package_id='11537',sticker_id='52002758')
    else:
        message = TextSendMessage(text=userSend)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    message = TextSendMessage(text='我看不懂貼圖')
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    userAdd = event.message.address
    userLat = event.message.latitude
    userLon = event.message.longitude
    
    weatherResult = OWMLonLatsearch(userLon,userLat)
    AQIResult = AQImonitor(userLon,userLat)
    gammaResult = gammamonitor(userLon,userLat)
    message = TextSendMessage(text='地址：{}\n緯度：{}\n經度：{}\n'.format(userAdd,userLat,userLon))
    message = TextSendMessage(text='天氣狀況：\n{}\n空氣品質：\n{}\n輻射值：\n{}\n'.format(weatherResult, AQIResult, gammaResult))
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

