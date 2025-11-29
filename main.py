import requests
import json
import os
import tempfile

# Кот от CATAAS 
text = input("Введите текст: ").strip()
url = f"https://cataas.com/cat/says/{text}?json=true"

print("Соединениt с сайтом cataas.com установлено")
response = requests.get(url)
response.raise_for_status()
data = response.json()
print(f"JSON с данными кота получен") # Сохранить JSON в файл 

cat_img_url =data["url"]
img_response = requests.get(cat_img_url)
img_response.raise_for_status()
file_size = len(img_response.content)
data["file_size_bytes"] = file_size

json_filename = f"{text}.json"


#Соединяем с яндесом
api_key = os.getenv("YADISK_TOKEN")
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

# Загрузить файл Картинки
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
if resp.status_code != 202:
    print("Ошибка загрузки на Диск:", resp.status_code, resp.text)
    resp.raise_for_status()
print("Файл загружен  на Яндекс.Диск:", disk_file_path)
disk_json_path = folder_path + "/" + f"{text}.json"

print("Загружаем файл JSON на Яндекс.Диск")

# 1. Запрашиваем href для загрузки
r = requests.get(
    f"{ya_url}/resources/upload",
    headers=headers,
    params={"path": disk_json_path, "overwrite": "true"},
)
r.raise_for_status()
href = r.json()["href"]  # ссылка для PUT [web:21][web:7]

# 2. Пишем JSON во временный файл и отправляем его
with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as tmp:
    # пишем JSON как текст в байтовый файл
    json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    tmp.write(json_bytes)
    tmp.flush()
    tmp.seek(0)  # перемотать в начало, важно [web:24][web:33]

    put_r = requests.put(href, data=tmp)
    put_r.raise_for_status()

print("JSON загружен на Яндекс.Диск:", disk_json_path)