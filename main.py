import requests
from bs4 import BeautifulSoup
import re

def crawlPage(pg):
    url = "https://forum.gamer.com.tw/C.php?bsn=19017&snA=58772&page="+str(pg)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(response.text, "html.parser")

def rm(pg):
    d = []
    each_floor = pg.find_all(class_=["c-article__content", "comment_content"])
    for afloor in each_floor:
        for aline in afloor:
            aline = re.findall(("[A-Za-z0-9!]"*4 + "-?")*3+"[A-Za-z0-9!]"*4, str(aline.text))
            for result in aline:
                if result.count("-") in (0, 3):
                    d += [result]
    return d

def main():
    pg = crawlPage(1)
    total_page = re.findall(">(\d)<", str(pg.find(class_="BH-pagebtnA")))[-1]
    d = rm(pg)

    for i in range(2, int(total_page)+1):
        pg = crawlPage(i)
        d += rm(pg)
    d = set(d)
    print(d)


        
    
if __name__ == "__main__":
    main()
