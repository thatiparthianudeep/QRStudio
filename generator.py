import qrcode
from PIL import Image

def generate_qr(data, logo_path=None, fill_color="black", back_color="white"):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    if logo_path:
        logo = Image.open(logo_path)
        qr_width, qr_height = img.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size))
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        img.paste(logo, pos, mask=logo.convert("RGBA").split()[3])

    return img