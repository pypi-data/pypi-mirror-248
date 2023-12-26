import qrcode

def text_to_ascii_qr(txt:str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(txt)
    qr.make(fit=True)
    qr.print_ascii()
