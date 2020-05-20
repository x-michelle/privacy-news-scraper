#!/bin/python3

import requests
from bs4 import BeautifulSoup
import sys

htmlstart = """<!doctype html>
<html lang="en">
<head>
    <title>Privacy Links</title>
    <style>.container{ padding:9px 12px;} .menu a{align:center}</style>
</head>
<body>
<div class="menu" align="center">
    <a href="#eff">EFF Deeplinks Blog</a> | <a href="#pia">PIA Blog</a> | 
    <a href="#hackread">HackRead</a> | 
    <a href="#signal">Signal Blog</a> | 
    <a href="#tor">Tor Project blog</a> 
</div>
<div class="container">
"""


with open("links.html", "w") as f:
    f.write(htmlstart)

    try:
        result = requests.get("https://eff.org/deeplinks")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        f.write(f"\n\t<a name='eff'></a>\t<h4>{soup.title.text}</h4>\n")
        articles = 0

        # <h3 class="node__title"><a href="" rel="bookmark">
        for h3 in soup.find_all("h3"):
            a = h3.find('a', rel='bookmark')
            if articles < 10:
                f.write(f"\t{ str(a).replace('/deeplinks','https://eff.org/deeplinks') }<br>\n")
                articles = articles + 1
        print(f"fetched EFF blog links ({articles})")
    except:
        print(f"Unexpected error fetching EFF Blog: {sys.exc_info()[0]}")


    try:
        result = requests.get("https://privateinternetaccess.com/blog")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        f.write(f"\n\t<a name='pia'></a>\n\t<h4>{soup.title.text}</h4>\n")
        articles = 0

        # <h3><a>article link</a>
        for h3tag in soup.find_all('h3'):
            a = h3tag.find('a')
            # skip any self-serving articles
            if articles < 8 and "VPN" not in a.text :
                f.write(f"\t{a}<br>\n" )
                articles = articles + 1
        print(f"fetched PIA blog links ({articles})")
    except:
        print(f"Unexpected error eftching PIA blog: {sys.exc_info()[0]}")


    try:
        result = requests.get("https://hackread.com/surveillance")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        f.write(f"\n\t<a name='hackread'></a>\n\t<h4>{soup.title.text}</h4>\n")
        articles = 0
    
        # <h3 itemprop="name"><a itemprop="url" ...>
        for h3tag in soup.find_all('h3'):
            a = h3tag.find('a', itemprop='url')
            if articles < 5:
                f.write(f"\t{a}<br>\n" )
                articles = articles + 1
        print(f"fetched HackRead blog links ({articles})")
    except:
        print(f"Unexpected error: {sys.exc_info()[0]}")


    try:
        result = requests.get("https://signal.org/blog")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        f.write(f"\n\t<a name='signal'></a>\n\t<h4>{soup.title.text}</h4>\n")

        # <h3 class="..."> - print only first 4
        articles = 0
        for h3tag in soup.find_all("h3"):
            if articles < 4:
                a = h3tag.find('a')
                f.write("\t" + str(a).replace('/blog', 'https://signal.org/blog') + "<br>\n" )
                articles = articles + 1
        print(f"fetched Signal blog links ({articles})")
    except:
        print(f"Unexpected error fetching Signal blog: {sys.exc_info()[0]}")


    try:
        result = requests.get("https://blog.torproject.org")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        f.write(f"\n\t<a name='tor'></a>\n\t<h4>{soup.title.text}</h4>\n")

        # <h2 class="title"><a href="..." rel="bookmark">
        articles = 0
        for h3tag in soup.find_all("h2"):
            if articles < 5:
                a = h3tag.find('a', rel='bookmark')
                f.write("\t" + str(a).replace('href=/', 'https://blog.torproject.org/') + "<br>\n" )
                articles = articles + 1
        print(f"fetched Tor Project blog links ({articles})")
    except:
        print(f"Unexpected error fetching Tor blog: {sys.exc_info()[0]}")


    print("fetching privacy articles complete - load links.html to view results")
    f.write("</div><br>\n</body>\n</html>\n")

