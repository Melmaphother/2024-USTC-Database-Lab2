from captcha.image import ImageCaptcha
from io import BytesIO
import base64
import random


def gen_captcha():
    image = ImageCaptcha(width=150, height=45)
    code = str(random.randint(1000, 9999))
    data = image.generate(code)
    image_file = BytesIO(data.read())
    image_data = base64.b64encode(image_file.getvalue()).decode('utf-8')
    image_data_url = f"data:image/png;base64,{image_data}"
    return code, image_data_url
