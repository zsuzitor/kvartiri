from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url_page_1 ="http://irr.ru/real-estate/"
    r_1 = requests.get(url_page_1)
    soup_1 = BeautifulSoup(r_1.text, 'html.parser')
    for item1_1_bloki in soup_1.find_all('div', 'mainPageBlockCategory__wrapper'):
        odin_div_a="http://irr.ru"+item1_1_bloki.find_all("a")[0].attrs["href"]
        print(odin_div_a)
        url_page_2 =odin_div_a
        r_2 = requests.get(url_page_2)
        soup_2 = BeautifulSoup(r_2.text, 'html.parser')
        for item2_1 in soup_2.find_all('div', 'listing__itemTitleWrapper'):
            print("+++")
            for a_elm in item2_1.find_all("a"):
                print("----")
                
                url_page = a_elm.attrs["href"]
                print(url_page)
                r = requests.get(url_page)
                soup = BeautifulSoup(r.text, 'html.parser')
