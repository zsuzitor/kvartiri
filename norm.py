from bs4 import BeautifulSoup
import requests
import time
import json
import re

if __name__ == '__main__':
    data={}
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
        last_url=koli4_str.find("a").attrs["href"]
        last_url_1=last_url[:-(len(last_url)-last_url.find("page")-4)]
        print(last_url)
        print(koli4_str.text)
        i1=int(koli4_str.text)
        i=0
        while i < i1:
            i+=1
            print(i)
            odin_url_nomer_str="http://irr.ru"+last_url_1+str(i)+"/"
            print(odin_url_nomer_str)
            r_123 = requests.get(odin_url_nomer_str)
            soup_123 = BeautifulSoup(r_123.text, 'html.parser')
            for item2_1 in soup_123.find_all('div', 'listing__itemTitleWrapper'):
                for a_elm in item2_1.find_all("a"):  
                    url_page = a_elm.attrs["href"]
                    print(url_page)
                    r = requests.get(url_page)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    try:
                        header = soup.find('h1', 'productPage__title').text
                        header=re.sub('\s+',' ',header)
                        data["header"]=header
                        print(header)
                    except:
                        print("")
                    try:
                        cena=soup.find('div', 'productPage__price').text
                        cena=re.sub('\s+',' ',cena)
                        data["cena"]=cena
                        print(cena)
                    except:
                        print("")
                    pod_header_str_o=""
                    for item in soup.find_all('span', 'productPage__characteristicsItemValue'):
                        pod_header = item.text
                        pod_header=re.sub('\s+',' ',pod_header)
                        pod_header_str_o+=pod_header+" "
                        print(pod_header)
                    data["pod_header"]=pod_header_str_o
                    try:    
                        opisanie_k=soup.find('p', 'productPage__descriptionText').text
                        opisanie_k=re.sub('\s+',' ',opisanie_k)
                        data["opisanie"]=opisanie_k
                        print(opisanie_k)
                    except:
                        print("")
                    s4et=1
                    temp=""
                    for item in soup.find_all('div', 'productPage__infoColumnBlock'):
                        print('info{}'.format(s4et))
                        for item1 in item.find_all('li', 'productPage__infoColumnBlockText'):
                            temp+=item1.text+" "
                        temp=re.sub('\s+',' ',temp)
                        print(temp)
                        data["dop_info"+str(s4et)]=temp
                        temp=""
                        s4et+=1
                    try:
                        with open('data.json', 'a', encoding='utf-8') as fh:
                            fh.write(json.dumps(data, ensure_ascii=False))
                        data={}
                    except:
                        print("===================ERROR========================")
                        time.sleep(10)
                    print("______________________")
