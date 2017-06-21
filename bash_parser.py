from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    # ссылка для парсинга
    url_page = 'http://krasnodar.irr.ru/real-estate/apartments-sale/new/studiya-im-evgenii-zhigulenko-ul-9-advert630802162.html'
   # print("0")
    # получаем содержимое страницы
    r = requests.get(url_page)
    # преобразуем текст в структуру BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # находим тег div с id='body'
    body = soup.find('div', id='body')
    
    #if body is None:
        # если нет такого блока, то выходим
        #print("0")
        #exit()
    for item in soup.find_all('span', 'productPage__characteristicsItemValue'):
    # итерируемся по всем div блокам с классом quote
    #company = soup.select('h1.productPage__title js-productPageTitle productPage__title_lines_1')[0].text.strip()
    #print("1")
        #rate_block = item.find('span', 'productPage__characteristicsItemValue')
    #print("2")
        rate = item.text
        print(rate)
