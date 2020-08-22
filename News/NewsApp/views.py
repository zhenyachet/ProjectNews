from django.shortcuts import render
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen as uReq
import feedparser


# Getting news from CNN sport

my_url = 'https://edition.cnn.com/sport'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = Soup(page_html, "html.parser")
HeadTitles = page_soup.findAll("div", {"class": "cd__content"})
CNNTitles = []
i = 0
while i < 10:
    CNNTitles.append(HeadTitles[i].a.text)
    CNNTitles.append('https://edition.cnn.com' + HeadTitles[i].a["href"])
    i = i + 1




# Get Head Image from CNN Sport
PrimaryImg = page_soup.findAll("img", {"class":"media__image media__image--responsive"})[0]["data-src-full16x9"]



# Getting news from BBC sport
#
# my_url = 'https://www.bbc.com/sport'
# uClient = uReq(my_url)
# page_html = uClient.read()
# uClient.close()
# page_soup = Soup(page_html, "html.parser")
# HeadTitles = page_soup.findAll("div", {"class": "gs-c-promo gs-t-sport gs-c-promo--stacked@m gs-c-promo--inline gs-o-faux-block-link gs-u-pb gs-u-pb++@m gs-c-promo--flex"})
#
# BBCTitles = []
# i = 0
# while i < 10:
#     BBCTitles.append(HeadTitles[i]["data-bbc-title"])
#     BBCTitles.append(HeadTitles[i]["data-bbc-result"])
#     i = i + 1

def index(req):
    return render(req, 'NewsApp/index.html', {'PrimaryImg': PrimaryImg, 'CNNTitles': CNNTitles})


def rss(request):
    if request.GET.get("url"):
        url = request.GET["url"]
        feed = feedparser.parse(url)

    else:
        feed = None

    return render(request, 'NewsApp/reader.html', {
        'feed': feed
    })



 # Getting rss from blogfeedspot
#
my_url = 'https://blog.feedspot.com/world_news_rss_feeds'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = Soup(page_html, "html.parser")
HeadTitles = page_soup.findAll("div", {"class": "rss-block"})
title_in_anchor = page_soup.findAll("h2", {"class": "anchor"})
description_in_div = page_soup.findAll("p", {"class": "d"})
rss_list_title = []
rss_list_src = []
rss_list_img = []
rss_list_description = []
i = 0

while i < len(HeadTitles)-1:
    img = (HeadTitles[i].div.img['data-lazy-src'])
    src_container = HeadTitles[i].findAll("div", {"class": "data"})
    src = src_container[0].p.a['href']
    title = title_in_anchor[i].a.text
    description = description_in_div[i].text
    rss_list_title.append(title)
    rss_list_src.append(src)
    rss_list_img.append(img)
    rss_list_description.append(description)
    i += 1

data = [{'title': title, 'src': src, 'img': img, 'description': description} for title, src, img, description in zip(rss_list_title, rss_list_src, rss_list_img, rss_list_description)]


def resources(req):
    if req.method == "POST":
        url = req.POST["src"]
        feed = feedparser.parse(url)
        return render(req, 'NewsApp/reader.html', {'feed': feed})

    return render(req, 'NewsApp/rss_list.html', {"data": data})






