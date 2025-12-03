def d_load(resp, ff, create_path):
    if resp.status_code in [200, 201, 202]:
        if ff == "file":
            print(f"Файл загружен на Яндекс.Диск: {create_path}")
        elif ff == "folder":
            print(f"Папка {create_path} создана")
        elif ff == "json":
            print("Файл json загружен на Яндекс.Диск.")
    else:
        if ff == "file":
            print("Ошибка загрузки файла, код:", resp.status_code)
        elif ff == "folder":
            print("Ошибка создания папки: код", resp.status_code)
        elif ff == "json":
            print("Ошибка загрузки файла, код:", resp.status_code)
