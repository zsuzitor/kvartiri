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
    #страница со всеми разделами
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
        #по страницам снизу
        while i < i1:
            i+=1
            print(i)
            odin_url_nomer_str="http://irr.ru"+last_url_1+str(i)+"/"
            print(odin_url_nomer_str)
            r_123 = requests.get(odin_url_nomer_str)
            soup_123 = BeautifulSoup(r_123.text, 'html.parser')
            #по списку с КВ
            for item2_1 in soup_123.find_all('div', 'listing__itemTitleWrapper'):
                for a_elm in item2_1.find_all("a"):  
                    url_page = a_elm.attrs["href"]
                    print(url_page)
                    r = requests.get(url_page)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    #СТРАНИЦА
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
                    data['nomer']=re.sub('\s+',' ',soup.find('div', 'productPage__phoneText').text)
                    #productPage__infoTextBold
                    tt1=soup.find('div', 'productPage__inlineWrapper')
                    data['name']=re.sub('\s+',' ',tt1.find('div', 'productPage__infoTextBold').text)

                    for item in soup.find_all('div', 'productPage__infoItem'):
                        tt2=re.sub('\s+','',item.text)
                        #print("1========================1")
                        #print(tt2)
                        #time.sleep(5)
                        if tt2.find("Место:")!=-1:
                            data["mesto"]=re.sub('\s+',' ',item.find('div', 'productPage__infoTextBold').text)
                            
                        if tt2=="":
                            
                            data["ssilka"]=re.sub('\s+',' ',item.find('a').attrs["href"])

                    for item in soup.find_all('div', 'productPage__characteristicsItem'):
                        i_temp1=item.find('span', 'productPage__characteristicsItemValue')
                        i_temp1=re.sub('\s+',' ',i_temp1.text)
                        i_temp2=item.find('span', 'productPage__characteristicsItemTitle')
                        i_temp2=re.sub('\s+',' ',i_temp2.text)
                        data[str(i_temp2)]=i_temp1
                    try:    
                        opisanie_k=soup.find('p', 'productPage__descriptionText').text
                        opisanie_k=re.sub('\s+',' ',opisanie_k)
                        data["opisanie"]=opisanie_k
                        print(opisanie_k)
                    except:
                        print("")
                    s4et=1
                    #temp=""
                    for item in soup.find_all('div', 'productPage__infoColumnBlock'):
                        print('info{}'.format(s4et))
                        data_info=[]
                        for item1 in item.find_all('li', 'productPage__infoColumnBlockText'):
                            data_info.append(re.sub('\s+',' ',item1.text))
                        #for x555 in data_info:
                            #print(x555)
                        data["dop_info"+str(s4et)]=data_info
                        s4et+=1
                    try:
                        with open('data.json', 'a', encoding='utf-8') as fh:
                            fh.write(json.dumps(data, ensure_ascii=False))
                        data={}
                    except:
                        print("===================ERROR========================")
                        time.sleep(10)
                    print("______________________")
