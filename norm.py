from bs4 import BeautifulSoup
import requests
import time
import json
import re

def go_play():
    koli4estvo_zapisey=0
    url_page_1 ="http://russia.irr.ru/real-estate/"
    r_1 = requests.get(url_page_1)
    soup_1 = BeautifulSoup(r_1.text, 'html.parser')
    #страница со всеми разделами
    tip_obyavleniya=""
    tip_gilya_str="Жилая недвижимость"
    tip_gilya_int=0
    for item1_1_bloki in soup_1.find_all('div', 'mainPageBlockCategory__wrapper'):
        if tip_gilya_int==3 or tip_gilya_int==4:
            tip_gilya_str="Коммерческая недвижимость"
        if tip_gilya_int==5 or tip_gilya_int==6:
            tip_gilya_str="Загородная недвижимость"
        if tip_gilya_int==7 or tip_gilya_int==8:
            tip_gilya_str="Гаражи и стоянки"
        tip_gilya_int+=1
        tip_obyavleniya=item1_1_bloki.find_all("a")[0].text
        odin_div_a="http://irr.ru"+item1_1_bloki.find_all("a")[0].attrs["href"]
        url_page_2 =odin_div_a
        r_2 = requests.get(url_page_2)
        soup_2 = BeautifulSoup(r_2.text, 'html.parser')
        koli4_str1=soup_2.find_all('li', 'pagination__pagesItem')
        koli4_str=koli4_str1[len(koli4_str1)-1]
        last_url=koli4_str.find("a").attrs["href"]
        last_url_1=last_url[:-(len(last_url)-last_url.find("page")-4)]
        i1=int(koli4_str.text)
        i=0
        #по страницам снизу
        while i < i1:
            i+=1
            odin_url_nomer_str="http://irr.ru"+last_url_1+str(i)+"/"
            r_123 = requests.get(odin_url_nomer_str)
            soup_123 = BeautifulSoup(r_123.text, 'html.parser')
            #по списку с КВ
            for item2_1 in soup_123.find_all('div', 'listing__itemTitleWrapper'):
                for a_elm in item2_1.find_all("a"):  
                    url_page = a_elm.attrs["href"]
                    r = requests.get(url_page)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    #СТРАНИЦА
                    data_error={}
                    data={}
                    koli4estvo_error=0 
                    data["тип_жилья"]=tip_gilya_str
                    data["тип_объявления"]=tip_obyavleniya
                    data["url_page"]=url_page
                    try:
                        list_img=[]
                        for image in soup.find('div', class_='lineGallery js-lineProductGallery').find_all('meta'):
                            list_img.append(image.attrs['content'])
                        data["картинки"]=list_img
                    except:
                        koli4estvo_error+=1
                        data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="картинки"
                        print("")
                    try:
                        karta=soup.find('div', 'js-productPageMap')
                        karta=str(karta)
                        karta=re.sub('.*\{','',karta)
                        karta=re.sub('\}.*','',karta)
                        data["карта"]=karta
                    except:
                        koli4estvo_error+=1
                        data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="карта"
                        print("")
                      
                    try:
                        header = soup.find('h1', 'productPage__title').text
                        header=re.sub('\s+',' ',header)
                        data["хэдер"]=header
                    except:
                        koli4estvo_error+=1
                        data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="хэдер"
                        print("")
                    try:
                        cena=soup.find('div', 'productPage__price').text
                        cena=re.sub('\s+',' ',cena)
                        data["цена"]=cena
                    except:
                        koli4estvo_error+=1
                        data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="цена"
                        print("")
                    try:
                        data['номер']=re.sub('\s+',' ',soup.find('div', 'productPage__phoneText').text)
                        tt1=soup.find('div', 'productPage__inlineWrapper')
                    except:
                        koli4estvo_error+=1
                        data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="номер"
                        print("")
                    try:
                        
                        data['имя']=re.sub('\s+',' ',tt1.find('div', 'productPage__infoTextBold').text)
                    except:
                        koli4estvo_error+=1
                        data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="имя"
                        #print("")
                    for item in soup.find_all('div', 'productPage__infoItem'):
                        try:
                            tt2=re.sub('\s+','',item.text)
                            if tt2.find("Место:")!=-1:
                                data["место"]=re.sub('\s+',' ',item.find('div', 'productPage__infoTextBold').text)
                            if tt2=="Объявлениенасайтепродавца":
                                data["ссылка"]=re.sub('\s+',' ',item.find('a').attrs["href"])
                        except:
                            koli4estvo_error+=1
                            data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="Место/ссылка"
                            print("1234567")
                    for item in soup.find_all('div', 'productPage__characteristicsItem'):
                        try:
                            i_temp1=item.find('span', 'productPage__characteristicsItemValue')
                            i_temp1=re.sub('\s+',' ',i_temp1.text)
                            i_temp2=item.find('span', 'productPage__characteristicsItemTitle')
                            i_temp2=re.sub('\s+',' ',i_temp2.text)
                            data[str(i_temp2)]=i_temp1
                        except:
                            koli4estvo_error+=1
                            data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="подхэдер"
                            print("")
                    try:    
                        opisanie_k=soup.find('p', 'productPage__descriptionText').text
                        opisanie_k=re.sub('\s+',' ',opisanie_k)
                        data["описание"]=opisanie_k
                    except:
                        koli4estvo_error+=1
                        data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="описание"
                        print("")
                    s4et=1
                    for item in soup.find_all('div', 'productPage__infoColumnBlock'):
                        data_info=[]
                        for item1 in item.find_all('li', 'productPage__infoColumnBlockText'):
                            data_info.append(re.sub('\s+',' ',item1.text))
                        try:
                            data["доп_инфа"+str(s4et)]=data_info
                        except:
                            koli4estvo_error+=1
                            data_error[str(koli4estvo_zapisey)+":"+str(koli4estvo_error)]="доп_инфа"
                            print("")
                        s4et+=1
                    try:
                        koli4estvo_zapisey+=1
                        print(koli4estvo_zapisey)
                        print("ERROR="+str(koli4estvo_error))
                        if koli4estvo_error>0:
                            data_error["url"]=url_page
                            with open('data_error.json', 'a', encoding='utf-8') as fh:
                                fh.write(json.dumps(data_error, ensure_ascii=False))
                        yield data
                    except:
                        print("===================ERROR========================")
                        data_error[str(koli4estvo_zapisey)+":"+"save"]="save"
                        time.sleep(10)
                    
                    print("______________________")


if __name__ == '__main__':
    data=go_play()
    for i in data:
        with open('data.json', 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(i, ensure_ascii=False))
        data={}
                            
        
        
    
    
