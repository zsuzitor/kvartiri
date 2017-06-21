from bs4 import BeautifulSoup
import requests
import time

if __name__ == '__main__':
    GLAVNAYA_STROKA=""
    url_page_1 ="http://irr.ru/real-estate/"
    r_1 = requests.get(url_page_1)
    soup_1 = BeautifulSoup(r_1.text, 'html.parser')
    for item1_1_bloki in soup_1.find_all('div', 'mainPageBlockCategory__wrapper'):
        odin_div_a="http://irr.ru"+item1_1_bloki.find_all("a")[0].attrs["href"]
        url_page_2 =odin_div_a
        r_2 = requests.get(url_page_2)
        soup_2 = BeautifulSoup(r_2.text, 'html.parser')

        koli4_str1=soup_2.find_all('li', 'pagination__pagesItem')
        koli4_str=koli4_str1[len(koli4_str1)-1]
        #/real-estate/apartments-sale/page1000/
        last_url=koli4_str.find("a").attrs["href"]
        last_url_1=last_url[:-(len(last_url)-last_url.find("page")-4)]#############
        print(last_url)
        print(koli4_str.text)
        i1=int(koli4_str.text)
        #last_url.find("page")
        i=0
        while i < i1:
        ##http://irr.ru/real-estate/apartments-s1000/
            i+=1
            print(i)
            odin_url_nomer_str="http://irr.ru"+last_url_1+str(i)+"/"
            print(odin_url_nomer_str)
        #time.sleep(10)
            r_123 = requests.get(odin_url_nomer_str)
            soup_123 = BeautifulSoup(r_123.text, 'html.parser')
            for item2_1 in soup_123.find_all('div', 'listing__itemTitleWrapper'):
                for a_elm in item2_1.find_all("a"):  
                    url_page = a_elm.attrs["href"]
                    GLAVNAYA_STROKA+=url_page
                    print(url_page)
                    r = requests.get(url_page)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    try:
                        header = soup.find('h1', 'productPage__title').text
                        GLAVNAYA_STROKA+=header
                        print(header)
                    except:
                        print("")
                    try:
                        cena=soup.find('div', 'productPage__price').text
                        GLAVNAYA_STROKA+=cena
                        print(cena)
                    except:
                        print("")
                    for item in soup.find_all('span', 'productPage__characteristicsItemValue'):
                        pod_header = item.text
                        GLAVNAYA_STROKA+=pod_header
                        print(pod_header)
                    try:    
                        opisanie_k=soup.find('p', 'productPage__descriptionText').text
                        GLAVNAYA_STROKA+=opisanie_k
                        print(opisanie_k)
                    except:
                        print("")
                    s4et=1
                    for item in soup.find_all('div', 'productPage__infoColumnBlock'):
                        print('info{}'.format(s4et))
                        for item1 in item.find_all('li', 'productPage__infoColumnBlockText'):
                            GLAVNAYA_STROKA+=item1.text
                            print(item1.text)
                        s4et+=1
                    try:
                        f = open('text.txt', 'a')
                        f.write(GLAVNAYA_STROKA + '\n'+"______________________")
                        GLAVNAYA_STROKA=""
                        f.close()
                    except:
                        print("===================ERROR========================")
                        time.sleep(10)
                    print("______________________")
