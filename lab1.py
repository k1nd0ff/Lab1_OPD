import requests
from bs4 import BeautifulSoup
import re
url = "https://omsk.kingstore.link/catalog/iphone/iphone-16/"
not_bot = {"totally_not_bot": "Mozilla/5.0"} #чтобы сайт не заблокировал вход
response = requests.get(url, headers=not_bot)
response.raise_for_status() #Проверка на ошибки на сайте
main = BeautifulSoup(response.text, "html.parser")

prices = main.find_all("div", class_="index-products-body-item__button-price")#находит цены в коде элемента сайта
price = []

for i in prices: #добавляем цены в список
    price_text = i.get_text(strip=True)
    num = re.sub(r"\D", "", price_text)#оставляет только цену
    if num:
        price.append(int(num))

print("минимальная цена:",min(price))
print("Максимальная цена:", max(price))
print("Средняя цена:",sum(price)//len(price))