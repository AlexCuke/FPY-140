import ya  
import cat

cat1 = cat.CatAPi()
text1 = cat1.get_input()

while text1 != "q":
    url1 = cat1.get_url()
    print(url1)
    ya1 = ya.YaDisk(text1)
    ya1.ya_create()
    ya1.upload_from_url(url1)
    ya1.get_cat_metadata()
    text1 = cat1.get_input()
else:
    print("Спасибо за работу!")