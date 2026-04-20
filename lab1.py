import requests
from bs4 import BeautifulSoup
def parse_iphone_prices():
    url = 'https://omsk.kingstore.link/catalog/iphone/iphone-16/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # Ищем все элементы с ценами
    price_elements = soup.find_all(['span', 'div', 'p'],
                                   class_=lambda x: x and (
                                               'price' in x.lower() or 'cost' in x.lower() or 'цена' in x.lower()))
    prices = []
    for element in price_elements:     # Извлекаем числовые значения цен
        text = element.get_text().strip()
        clean_text = ''.join(c for c in text if c.isdigit() or c == ',') # Убираем лишние символы
        if clean_text:
            try:
                # Преобразуем в число
                price = float(clean_text.replace(',', '.'))
                if 10000 < price < 200000:  # Фильтр цен на iPhone
                    prices.append(price)
            except ValueError:
                continue
    # Удаляем дубликаты
    unique_prices = list(set(prices))
    if unique_prices:
        min_price = min(unique_prices)
        max_price = max(unique_prices)
        avg_price = sum(unique_prices) / len(unique_prices)
        print(f"Найдено {len(unique_prices)} уникальных цен")
        print(f"Мин цена: {min_price:.0f} руб.")
        print(f"Макс цена: {max_price:.0f} руб.")
        print(f"Ср цена: {avg_price:.0f} руб.")
        print("\nВсе цены:", [f"{p:.0f}" for p in sorted(unique_prices)])
    else:
        print("Неправильно, попробуйте еще раз")
if __name__ == '__main__':
    parse_iphone_prices()