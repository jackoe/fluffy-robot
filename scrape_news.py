import urllib.request
from bs4 import BeautifulSoup
import bs4
# pip3 install beautifulsoup4
import sys

def grab_soup_kanji(soup):
    # if the paragraph tag is a string, it's just an empty string
    if type(soup) == str:
        return soup
    #print(soup, type(soup))
    elif type(soup) == bs4.element.NavigableString:
        return str(soup)
    else:
        print(soup.span)
        print([x for x in soup])
        #print(soup.find_all("ruby"))
    #if soup.unicode[:6] == "ruby":
    #    print(soup)
    #elif type(soup) is bs4.element.Tag
    #   print(type(soup), soup.ruby)
    #print(type(soup), 'DONE')
    #print(soup.find_all('ruby'))
#    print(soup, "TYPE", type(soup), "\n")
#    print([type(x) for x in soup])
    return ""

def grab_soup_hiragana(soup):
    return ""
    

# takes paragraph as soup tag
# outputs list (of sentences) of tuples
# (kanji_str, hirigana_str)
def parse_paragraph(paragraph_soup):
    #print(type(paragraph_soup))
    words = [(grab_soup_kanji(word), grab_soup_hiragana(word)) 
                for word in paragraph_soup]
    

def grab_sentences(input_html):
    soup = BeautifulSoup(input_html, 'html.parser')
    soup = soup.find(id="newsarticle")
    parsed_graphs = [parse_paragraph(x) for x in soup]


#urls = sys.stdin.read().splitlines()
urls = ["http://www3.nhk.or.jp/news/easy/k10011198291000/k10011198291000.html"]
# GET request howto from the following
# https://stackoverflow.com/questions/645312/what-is-the-quickest-way-to-http-get-in-python
for url in urls:
    grab_sentences(urllib.request.urlopen(url).read())

