import requests
import json
import os
import def_f

class YaDisk:
    def __init__(self, text):
        self.api_key = os.getenv("YADISK_TOKEN")
        if not self.api_key:
            raise ValueError("Переменная окружения YADISK_TOKEN не установлена")
        self.ya_url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.headers = {
            "Authorization": f"OAuth {self.api_key}",
            "Accept": "application/json",
        }
        self.text = text
        self.folder_path = "/FPY-140"

    def ya_create(self):
        print("Создаем папку", self.folder_path)
        resp = requests.put(
            self.ya_url,
            headers=self.headers,
            params={"path": self.folder_path},
        )
        def_f.d_load(resp, "folder", self.folder_path)
        return resp

    def upload_from_url(self, file_url: str):
        disk_path = f"{self.folder_path}/{self.text}.png"
        print("Загружаем кота на Яндекс диск")
        resp = requests.post(
            f"{self.ya_url}/upload",
            headers=self.headers,
            params={
                "path": disk_path,
                "url": file_url,
                "overwrite": "true",
            },
        )
        d_load(resp, "file", disk_path)
        return resp

    def upload_local_file(self, local_path: str, remote_path: str):
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
        href = resp.json().get("href")
        if not href:
            print("href не найден в ответе")
            return resp

        with open(local_path, "rb") as f:
            put_resp = requests.put(href, files={"file": f})
        return put_resp

    def get_cat_metadata(self):
        resp = requests.get(
            self.ya_url,
            headers=self.headers,
            params={"path": self.folder_path},
        )
        data = resp.json()
        files = {}
        for value in data.get("_embedded", {}).get("items", []):
            files[value.get("name")] = value.get("size")

        file_path = "files.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(files, f, ensure_ascii=False, indent=2)

        remote_path = f"{self.folder_path}/{file_path}"
        self.upload_local_file(file_path, remote_path)
        def_f.d_load(resp, "json", self.folder_path)
        return files