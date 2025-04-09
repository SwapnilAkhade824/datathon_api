import qrcode
from io import BytesIO
import base64

def generate_qr(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    return img_str
