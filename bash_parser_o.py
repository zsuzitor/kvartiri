from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url_page_1 ="http://irr.ru/real-estate/"
    r_1 = requests.get(url_page_1)
    soup_1 = BeautifulSoup(r_1.text, 'html.parser')
    #for item1_1 in soup_1.find_all('a href', 'mainPageBlockCategory__subTitle'):
        for item2_1 in item1_1.find_all('a href', 'mainPageBlockCategory__subTitle'):
            tek_page=item2_1.text
    url_page = 'http://krasnodar.irr.ru/real-estate/apartments-sale/new/studiya-im-evgenii-zhigulenko-ul-9-advert630802162.html'
    r = requests.get(url_page)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        header = soup.find('h1', 'productPage__title').text
        print(header)
    except:
        print("")
    try:
        cena=soup.find('div', 'productPage__price').text
        print(cena)
    except:
        print("")
    for item in soup.find_all('span', 'productPage__characteristicsItemValue'):
        pod_header = item.text
        print(pod_header)
    try:    
        opisanie_k=soup.find('p', 'productPage__descriptionText').text
        print(opisanie_k)
    except:
        print("")
    s4et=1
    for item in soup.find_all('div', 'productPage__infoColumnBlock'):
        print('info{}'.format(s4et))
        for item1 in item.find_all('li', 'productPage__infoColumnBlockText'):
            print(item1.text)
        s4et+=1
    print("______________________")
