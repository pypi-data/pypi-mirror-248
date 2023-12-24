import qrcode
def user_input():
    s = input("Enter the URL: ")
    return s
def method(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("my_qrcode.png")
user_url = user_input()
method(user_url)



