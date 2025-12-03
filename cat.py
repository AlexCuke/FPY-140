import requests
import conf

class CatAPi:
    def __init__(self):
        self.text = ""
        self.base_url=conf.cat_url
        
    def get_input(self):
        self.text = input("Введите текст или 'q' для выхода: ").strip()
        return self.text

    def get_url(self):
        # Кодируем пробелы и т.п.
        return f"{self.base_url}/{requests.utils.quote(self.text)}?fontSize={conf.fontsize}&fontColor={conf.color}"