import requests
import json
import os
from google.colab import userdata

# Кот от CATAAS
print("Соединениe с сайтом cataas.com установлено")

class CatAPi:
    def __init__(self):
        self.text = ""
        self.url = f"https://cataas.com/cat/says/"

    def get_input(self):
        self.text =input("Введите текст или 'q' для выхода: ").strip()
        return self.text

    def get_url(self):
        return self.url

class YaDisk:
    def __init__(self,text):
        self.api_key = os.getenv("YADISK_TOKEN")
        self.ya_url= "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
                        "Authorization": f"OAuth {self.api_key}",
                        "Accept": "application/json",
                        }
        self.text=text
        self.folder_path = "/FPY-140"

    def ya_create(self):
        print("Создаем папку",self.folder_path)
        resp = requests.put(
                             self.ya_url,
                             headers=self.headers,
                             params={"path": self.folder_path},
                            )

        d_load(resp,'folder',self.folder_path)
        return resp

    def upload_from_url(self, file_url: str):
        disk_path = f"{self.folder_path}/{self.text}.png"
        print(f"Загружаем кота  на Яндекс диск")
        resp = requests.post(
                            f"{self.ya_url}/upload",
                            headers=self.headers,
                            params={
                                    "path": disk_path,
                                    "url": file_url,
                                    "overwrite": "true",
                                  },
                            )
        d_load(resp, 'file', disk_path)


    def upload_local_file(self, local_path: str, remote_path: str):
        # 1. Получаем URL для загрузки
        resp = requests.get(
                            f"{self.ya_url}/upload",
                            headers=self.headers,
                            params={
                                    "path": remote_path,
                                    "overwrite": "true",
                                   },
                           )
        if resp.status_code != 200:
              print(f"Ошибка получения href: код {resp.status_code}")
              return resp
        href = resp.json()["href"]
        # 2. Загружаем файл по этому href
        with open(local_path, "rb") as f:
                put_resp = requests.put(href, files={"file": f})

    def get_cat_metadata(self):
        # Получаем метаданные папки
        resp = requests.get(
                              self.ya_url,
                              headers=self.headers,
                              params={"path": self.folder_path},
                            )
        data = resp.json()
        files = {}
        for value in data.get("_embedded", {}).get("items", []):
                  files[value.get("name")] = value.get("size")
        # 1. Сохраняем словарь в JSON
        file_path = "files.json"
        with open(file_path, "w", encoding="utf-8") as f:
                  json.dump(files, f, ensure_ascii=False, indent=2)
        # 2. Загружаем этот JSON на Диск
        remote_path = f"{self.folder_path}/{file_path}"
        self.upload_local_file(file_path, remote_path)
        d_load(resp,'json',self.folder_path)
        return files

def d_load(resp,ff,create_path):
        if resp.status_code in [200,201,202]:
            if  ff=='file':
                print(f"Файл загружен на Яндекс.Диск: {create_path}")
            elif ff=='folder':
                print(f"Папка {create_path} создана")
            elif ff=='json':
                print(f"Файл json загружен на Яндекс.Диск.")
        else:
            if  ff=='File':
                print("Ошибка загрузки файла, код:", resp.status_code)
            elif ff=='folder':
                print("Ошибка создания папки: код ", resp.status_code)
            elif ff=='json':
                print(f"Ошибка загрузки файла, код:", resp.status_code)
text1=CatAPi().get_input()
while text1 != 'q' :
    url1=CatAPi().get_url()
    ya1=YaDisk(text1)
    ya1.ya_create()
    ya1.upload_from_url(url1)
    ya1.get_cat_metadata()
    text1=CatAPi().get_input()
else:
    print("Спасибо за работу!")