import requests
import json
import time
import base64
from random import randint as r
import os

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def gen(self, prom, dirr="res"):
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'B2C4685CA7669D34FB7A0081595FE330', 'C235FDD9A9E04C805E1DBE1CE49DB2AA')
        model_id = api.get_model()
        uuid = api.generate(prom, model_id)
        images = api.check_generation(uuid)

        # Здесь image_base64 - это строка с данными изображения в формате base64
        image_base64 = images[0]

        # Декодируем строку base64 в бинарные данные
        image_data = base64.b64decode(image_base64)

        # Открываем файл для записи бинарных данных изображения
        try:
            with open(f"{dirr}/{prom.split('.')[0]}_{r(0, 100000)}.jpg", "wb") as file:
                file.write(image_data)
        except Exception as e:
            print(f"Ошибка при записи файла: {e}")
def main():
    while True:
        zapros = input("prompt: ")

        try:
            os.mkdir(os.getcwd().replace("\\", "/") + f'/' + zapros.replace("\n", " ").split(".")[0])
        except FileExistsError:
            print('exist')

        for j in range(4):
            Text2ImageAPI('https://api-key.fusionbrain.ai/', 'B2C4685CA7669D34FB7A0081595FE330', 'C235FDD9A9E04C805E1DBE1CE49DB2AA').gen(zapros.replace("\n", " "), zapros.replace("\n", " ").split(".")[0])

            print(f"сделано {j + 1}")

        print("завершено")


if __name__ == "__main__":
    main()
