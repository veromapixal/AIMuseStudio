import requests
from io import BytesIO
from PIL import Image

api_key = 'YOUR_API_KEY'  # Получите ключ API на https://www.remove.bg/api

def remove_bg(image_path):
    url = 'https://api.remove.bg/v1.0/removebg'
    headers = {'X-Api-Key': api_key}
    files = {'image_file': open(image_path, 'rb')}

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == requests.codes.ok:
        result_image = Image.open(BytesIO(response.content))
        return result_image
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Пример использования
image_path = 'path/to/your/image.jpg'
result_image = remove_bg(image_path)

if result_image:
    result_image.show()
