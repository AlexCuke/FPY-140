import requests
import json
import os


# Кот от CATAAS 
text1 = input("Введите текст: ").strip()
url1 = f"https://cataas.com/cat/says/"
fin_url1=f"{url1}{text1}"
print("Соединениe с сайтом cataas.com установлено")
class CatAPi:
    def __init__(self,text,url):
        self.text=text
        self.url=url
        self.fin_url = f"{url}{text}"
    def get_cat_url(self):
          return self.fin_url

class YaDisk: 
    def __init__(self,text):
        self.api_key = os.getenv("YADISK_TOKEN")
        self.ya_url= "https://cloud-api.yandex.net/v1/disk"
        self.headers = {
                     "Authorization": f"OAuth {self.api_key}",
                    "Accept": "application/json",
        }
        self.text=text
        self.folder_path = "/FPY-140"

    def ya_create(self):
        print("Создаем папку",self.folder_path)
        resp = requests.put(
                             f"{self.ya_url}/resources",
                             headers=self.headers, 
                             params={"path": self.folder_path},
                            )
        if resp.status_code == 201:
            # 201 — создано, 409 — уже существует
            print(f"Папка {self.folder_path} создана")
            resp.raise_for_status()
        else:
            print("Ошибка создания папки: код ", resp.status_code)
    def upload_from_url(self, file_url: str):
        disk_path = f"{self.folder_path}/{self.text}.png"
        resp = requests.post(
            f"{self.ya_url}/resources/upload",
            headers=self.headers,
            params={
                "path": disk_path,
                "url": file_url,
                "overwrite": "true",
            },
        )
        if resp.status_code == 202:
            # 201 — создано, 409 — уже существует
            print(f"Файл залит на яндекс-диск")
            resp.raise_for_status()
        else:
            print("Ошибка загрузки файла: код ", resp.status_code)
        resp.raise_for_status()   
    def upload_local_file(self, local_path: str, remote_path: str):
        # 1. Получаем URL для загрузки
        resp = requests.get(
            f"{self.ya_url}/resources/upload",
            headers=self.headers,
            params={
                "path": remote_path,
                "overwrite": "true",
            },
        )
        resp.raise_for_status()
        href = resp.json()["href"]
        # 2. Загружаем файл по этому href
        with open(local_path, "rb") as f:
            put_resp = requests.put(href, files={"file": f})
        if put_resp.status_code in (201, 202):
            print(f"Локальный файл загружен на Яндекс.Диск: {remote_path}")
        else:
            print("Ошибка загрузки локального файла: код", put_resp.status_code)
            put_resp.raise_for_status()
    def get_cat_metadata(self):
        # Получаем метаданные папки
        resp = requests.get(
            f"{self.ya_url}/resources",
            headers=self.headers,
            params={"path": self.folder_path},
        )
        resp.raise_for_status()
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
        print(f"Файл Json загружен")
        return files
        
cat1=CatAPi(text1,url1)
cat1.get_cat_url()
cat_url = cat1.get_cat_url()
ya1=YaDisk(text1)
ya1.ya_create()
ya1.upload_from_url(cat_url)
ya1.get_cat_metadata()
ya1.get_cat_metadata()

