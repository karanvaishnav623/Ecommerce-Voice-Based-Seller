from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import httplib2
from langchain_core.tools import tool


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(html_content, flag=True):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_elements = soup.findAll(text=True)

    visible_texts = filter(tag_visible, text_elements)
    visible_text_list = []

    for text in visible_texts:
        stripped_text = text.strip()
        if (stripped_text == "ABOUT"):
            flag = False
            break
        if (flag):
            visible_text_list.append(stripped_text)

    result_text = "\n".join(visible_text_list)

    return result_text


@tool
def specific_product_review(link) -> str:
    '''
    The function looks for a reviews of a specific product 
    and scrapes its information using the link.

    Args:
        link: string
    '''
    http = httplib2.Http()
    links = link.split("/p/")
    link = links[0] + "/product-reviews/" + links[1]
    status, response = http.request(link)
    # print(status)
    # print(response)

    return text_from_html(response)

# print(specific_product_review('https://www.flipkart.com/acer-nitro-amd-ryzen-5-hexa-core-7535hs-16-gb-512-gb-ssd-windows-11-home-6-graphics-nvidia-geforce-rtx-3050-anv15-41-gaming-laptop/p/itm6491e522f1157?pid=COMGZN7ZYP8MDPHR'))
