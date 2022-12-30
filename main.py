import requests
from bs4 import BeautifulSoup
import re

def crawlPage(pg=1):
    url = "https://forum.gamer.com.tw/C.php?bsn=19017&snA=58772&page="+str(pg)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return response.text
    
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
    pg = crawlPage() + crawlPage(99999)
    d = rm(BeautifulSoup(pg, "html.parser"))
    d = list(set(d))
    for idx, cnt in enumerate(d):
        d[idx] = cnt.upper()
        if len(cnt) == 16:
            d[idx] = cnt[0:4] + "-" +cnt[4:8] + "-" + cnt[8:12] + "-" + cnt[12:]
    print(d)
        
    
if __name__ == "__main__":
    main()
