import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from langchain_core.tools import tool

BASE_URL = "https://www.flipkart.com"

# print(response)


@tool
def product_list_lookup(keywords) -> str:
    '''
    Make a search query using a list of keywords and fetch the most suitable link for the product

    Args:
        keywords: list of string
    '''
    http = httplib2.Http()
    prev = None
    query = ""
    if (isinstance(keywords, list)):
        for words in keywords:
            for word in words.split(" "):
                query += word+"+"
        query = query[:-1]
    elif (isinstance(keywords, str)):
        for word in keywords.split(" "):
            query += word+"+"
        query = query[:-1]
    status, response = http.request('http://www.flipkart.com/search?q='+query, headers = {'User-agent': 'your bot 0.1'})
    print(status)
    counter = 0

    with open("results.txt", "w", encoding="utf-8") as f:
        for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                l = link['href'].split("&lid")
                if len(l) >= 2 and counter <= 5 and ("/p/" in l[0]) and l[0] != prev:
                    # f.write(BASE_URL+l[0]+"\n")
                    return (BASE_URL+l[0])
                    counter += 1
                    prev = l[0]
