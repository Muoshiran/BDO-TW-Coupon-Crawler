import requests
from bs4 import BeautifulSoup
import re

def crawlPage(pg=1):
    url = "https://forum.gamer.com.tw/C.php?bsn=19017&snA=58772&page="+str(pg)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return response.text  # str
    
def rm(pg):
    d = []
    each_floor = str(pg.find_all(class_=["c-article__content", "comment_content"]))
    # Seperate the contents of the html tag into single line and remove the tag
    while True:
        start_tag = each_floor.find("<")
        end_tag = each_floor.find(">")

        if start_tag not in [None, -1] and end_tag not in [None, -1]:
            each_floor = each_floor.replace(each_floor[start_tag:end_tag+1], "\n")  # <.+?> to \n
            start_tag = end_tag = None  # reset the index

        if start_tag == -1 or end_tag == -1:  # break when there are no < >
            break
    
    for result in re.findall(("[A-Za-z0-9!]"*4 + "-?")*3+"[A-Za-z0-9!]"*4, each_floor):
        if result.count("-") in (0, 3):  # avoid weird result  aaaa-aaaa3234wsax
            result = result.upper()

            if len(result) == 16:  # not follow the format
                result = result[0:4] + "-" + result[4:8] + "-" + result[8:12] + "-" + result[12:]  # 5, 9, 13 is -
            if result not in d:  # avoid duplicate
                d += [result]
    return d  # list

def main():
    pg = crawlPage() + crawlPage(99999)  # return str
    d = rm(BeautifulSoup(pg, "html.parser"))  # return list
    print(d)
        
    
if __name__ == "__main__":
    main()
