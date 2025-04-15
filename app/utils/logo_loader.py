import base64
from PIL import Image
import requests
from io import BytesIO

def load_logo_base64():
    try:
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/2560px-Airbnb_Logo_B%C3%A9lo.svg.png"
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    except:
        return ""