import requests
from bs4 import BeautifulSoup
import time
import json

dist_url = "https://www.readthistwice.com"
# myheaders = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "br, gzip, deflate",
#     "Host": "www.readthistwice.com",
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
# }


def getCatas(dist_url):
    res = requests.get(dist_url)
    soup = BeautifulSoup(res.text, "html.parser")
    catas_tags = soup.find_all("a", attrs={"class": "styles_category__rFlhj"})
    catas = []

    i = 0
    for c in catas_tags:
        cata = {}
        cata["cata_name"] = c.contents[0].string
        if len(c.contents) == 2:
            cata["cata_description"] = c.contents[1].string
        catas.append(cata)
    return catas


def getSubCatas(dist_cata_url):
    res = requests.get(dist_cata_url)
    soup = BeautifulSoup(res.text, "html.parser")
    sub_catas_tags = soup.find_all("a", attrs={"class": "styles_main__jCYUz"})
    sub_catas = []
    for c in sub_catas_tags:
        sub_cata = {}
        sub_cata["link"] = c["href"]
        sub_cata["cata_name"] = c.contents[2].contents[0].contents[0].string
        sub_catas.append(sub_cata)
    return sub_catas


def getBookList(dist_list_url):
    res = requests.get(dist_list_url)
    soup = BeautifulSoup(res.text, "html.parser")
    book_tags = soup.find_all(
        "div", attrs={"class": "styles_container__aEhha styles_book__4EnzQ"})
    book_list = []
    for bt in book_tags:
        book = {}
        for bc in bt.children:
            if bc.has_attr('class') and bc["class"][0] == "styles_main__veBBl":
                info = bc.contents[1]
                book["name"] = info.contents[0].string
                book["author"] = info.contents[2].contents[0].string
            elif bc.has_attr('class') and bc["class"][0] == "styles_description__xIoZP":
                book["description"] = bc.string
        book_list.append(book)
    return book_list


if __name__ == "__main__":
    catas = getCatas(dist_url+"/books")
    l = 0
    for c in catas:
        c["sub_cata"] = getSubCatas(
            dist_url+"/books/"+c["cata_name"].replace(" ", "-").replace("&", "and"))
        for d in c["sub_cata"]:
            time.sleep(0.5)
            d["book_list"] = getBookList(dist_url+d["link"])
            print("finished subcata: "+d["cata_name"])
        l += len(c["sub_cata"])
        print("****finished cata: "+c["cata_name"]+"****")
    with open("books.json", "w") as bf:
        json.dump(catas, bf)
    print("all finished")
