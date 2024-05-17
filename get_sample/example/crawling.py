import pandas as pd
from urllib.request import urlopen
from icecream import ic

from bs4 import BeautifulSoup

class ScrapBugs:
    
    def __init__(self) -> None:
        pass

    def scrap(self) -> dict:
        print('ScrapBugs scrap() called')
        url = "https://music.bugs.co.kr/chart/track/realtime/total?wl_ref=M_contents_03_01"
        html_doc = urlopen(url)
        soup = BeautifulSoup(html_doc, 'lxml')
        list1 = self.find_music(soup, 'title')
        list2 = self.find_music(soup, 'artist')
        a = [i if i == 0 or i == 0 else i for i in range(1)]
        b = [i if i == 0 or i == 0 else i for i in range(1)]
        c = [(i, j) for i, j in enumerate(a)]
        d = {i : j for i, j in zip(list1, list2)}
        l = [i + j for i, j in zip(list1, list2)]
        l2 = list(zip(list1, list2))
        d1 = dict(zip(list1, list2))
        pd.DataFrame(l2, columns=['title', 'artist']).to_csv('./get_sample/example/data/bugs.csv', index=False)
        return d1
    
    def find_music(self, soup: BeautifulSoup, tag: str) -> list:
        list = soup.find_all('p', {'class': tag})
        return [i.get_text().replace("\n", "") for i in list]

if __name__ == '__main__':
    sb = ScrapBugs()
    sb.scrap()