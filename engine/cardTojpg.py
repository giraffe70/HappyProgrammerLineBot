import imgkit
import qrcode
import cloudinary.uploader
import cloudinary

# name = input('請輸入姓名：')
# seat = input('請輸入座位：')
# time = input('請輸入時間：')

def QRCodeGenerator(name,time,seat):
	
	qr = qrcode.QRCode(
	version=2,
	error_correction=qrcode.constants.ERROR_CORRECT_L,
	box_size=4,
	border=2,
	)
	qr.add_data('name:{}\ntime:{}\nseat:{}\n'.format(name, time, seat))
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	img.save('qrcode.png')

def booking(name, time, seat):
	qrcodeURL = QRCodeGenerator(name, time, seat)

	htmlDoc = '''
	<!DOCTYPE html>
	<html lang="zh-cn">
	<head>
		<link rel="stylesheet" type="text/css" href="bootstrap.css" >
		<link href="https://fonts.googleapis.com/css?family=Noto+Sans+TC&display=swap" rel="stylesheet"> 
		<meta charset="utf-8">
	</head>
		<body style="font-family: 'Noto Sans TC', sans-serif;">
		<div class="card border-info mb-3" style="width: 18rem;">
			<img class="card-img-top" src="https://www.goodtechtricks.com/wp-content/uploads/2018/04/free-movie-streaming-sites.jpg" alt="Card image cap">
			<div class="card-body">
				<h5 class="card-title">門票</h5>
			    <p class="card-text">Happy Programmer</p>
			</div>
			<ul class="list-group list-group-flush">
			    <li class="list-group-item">持有人：'''+name+'''</li>
			    <li class="list-group-item">時間：'''+time+'''</li>
			    <li class="list-group-item">座位：'''+seat+'''</li>
			</ul>
			<div class="text-center">
				<img class="rounded" src="app/qrcode.png" alt="Card image cap">
			</div>
			
			<!--div class="card-body">
			    <a href="#" class="card-link">Card link</a>
			    <a href="#" class="card-link">Another link</a>
			</div-->
		</div>
		</body>

	</html>
	'''

	css = 'app/engine/bootstrap.css'

	config = imgkit.config(wkhtmltoimage='./bin/wkhtmltoimage')
	options={'quality':'100','width':'100', 'encoding':'utf-8', 'zoom':'3.125'}
	imgkit.from_string(htmlDoc, 'ticket.jpg', config=config, css=css, options=options)
	cloudinary.uploader.upload('ticket.jpg')['secure_url']
	return secure_url



