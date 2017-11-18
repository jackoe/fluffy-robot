import urllib.request
from bs4 import BeautifulSoup
from functools import reduce
import bs4
import sys

# (a, b), (c, d) -> (a+c, b + d)
def tuple_string_add(t1 ,t2):
    (y1, y2) = ("", "")
    if len(t2) == 2:
        (x2, y2) = t2
    elif len(t2) == 3:
        (x2, y21, y22) = t2
        y1 = y21 + y22
    else:
        (x21, y21, x22, y22) = t2
        x2 = x21 + x22
        y2 = y21 + y22
    (x1, y1) = t1
    return (x1+x2, y1+y2)

def tuple_list_flatten(l):
    return reduce(tuple_string_add, l, ("", ""))

def grab_soup_kanji_hiragana(soup):
    #if the paragraph tag is a string, it's just an empty string
    if type(soup) == str:
        return soup, soup
    #if it's a navigable string, it's just hiragana on its own
    elif type(soup) == bs4.element.NavigableString:
        hiragana = str(soup)
        return hiragana, hiragana
    else:
    #otherwise, it's a ruby tag, and we can grab the text
    #the first is the kanji, the second is hiragana
        if len(list(soup.strings)) == 1:
            soup_str = list(soup.strings)[0]
            return (soup_str, soup_str)
        return tuple(soup.strings)

# outputs tuple of strings
# (kanji_str, hirigana_str)
def parse_paragraph(paragraph_soup):
    words = [grab_soup_kanji_hiragana(word) for word in paragraph_soup]
    return (tuple_list_flatten(words))

# given the html, returns the sentences in the webpage
def grab_sentences(input_html):
    soup = BeautifulSoup(input_html, 'html.parser')
    soup = soup.find(id="newsarticle")
    for x in soup.find_all("span") + soup.find_all('a'):
        x.unwrap()
    parsed_graphs = [parse_paragraph(x) for x in soup]
    return tuple_list_flatten(parsed_graphs)


urls = sys.stdin.read().splitlines()
#urls = ["http://www3.nhk.or.jp/news/easy/k10011198291000/k10011198291000.html"]
# GET request howto from the following
# https://stackoverflow.com/questions/645312/what-is-the-quickest-way-to-http-get-in-python
parsed_pages = [grab_sentences(urllib.request.urlopen(url).read()) for url in urls]
(all_kanji, all_hiragana) = (tuple_list_flatten(parsed_pages))
all_kanji    =    all_kanji.replace('\n', '').split('。')
all_hiragana = all_hiragana.replace('\n', '').split('。')

output_sentences = zip(all_kanji, all_hiragana)
with open('kanji_hiragana.txt', 'w') as f:
    for kanji, hiragana in output_sentences:
        f.write(kanji + '\n' + hiragana + '\n')
