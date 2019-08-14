import qrcode

qr = qrcode.QRCode(
	version=2,
	error_correction=qrcode.constants.ERROR_CORRECT_L,
	box_size=4,
	border=2,
)

def QRCodeGenerator(name,time,seat):
	
	qr.add_data('name:{}\ntime:{}\nseat:{}\n'.format(name, time, seat))
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	img.save('qrcode.png')


# url = 'https://manager.line.biz/account/@303ataqy/richmenu/2055274'
# QRCodeGenerator()