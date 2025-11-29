import requests
import json
import pprint as pp
import os
# Кот от CATAAS 
text = input("Введите текст: ").strip()
url = f"https://cataas.com/cat/says/{text}?json=true"

response = requests.get(url)
response.raise_for_status()
print("Соединениt с сайтом cataas.com установлено")
data = response.json()
print(f"JSON загружен") # Сохранить JSON в файл 
pp.pprint(data)     # Печатаем JSON в файл 

cat_img_url =data["url"]
img_response = requests.get(data["url"])
img_response.raise_for_status()


#Соединяем с яндесом
api_key=""
ya_url= "https://cloud-api.yandex.net/v1/disk"
headers = {
    "Authorization": f"OAuth {api_key}",
    "Accept": "application/json",
}

print("Создаем папку")
folder_path = "/FPY-140"
disk_file_path = folder_path + "/" + f"{text}.jpg"

# Создать папку (если уже есть — проигнорировать 409)
resp = requests.put(
    f"{ya_url}/resources",
    headers=headers,
    params={"path": folder_path},
)

if resp.status_code not in (201, 409):
    # 201 — создано, 409 — уже существует
    print("Ошибка создания папки:", resp.status_code, resp.text)
    resp.raise_for_status()

# Загрузить файл
print("Загружаем файл на Яндекс.Диск")
resp = requests.post(
    f"{ya_url}/resources/upload",
    headers=headers,
    params={
        "path": disk_file_path,
        "url": cat_img_url,
        "overwrite": "true",
    },
)
print("status:", resp.status_code, resp.text)
resp.raise_for_status()

print("Файл загружен на Яндекс.Диск:", disk_file_path)