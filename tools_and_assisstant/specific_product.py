from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import httplib2
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(html_content, flag=True):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_elements = soup.findAll(string=True)

    visible_texts = filter(tag_visible, text_elements)
    visible_text_list = []

    for text in visible_texts:
        stripped_text = text.strip()
        if (stripped_text == "Buy together" or 
            stripped_text == "Frequently Bought Together"):
            break
        elif (stripped_text == "Product Description"):
            flag = False
        elif (stripped_text == "Specifications"):
            flag = True
        if (flag):
            visible_text_list.append(stripped_text)

    result_text = "\n".join(visible_text_list)

    return result_text


@tool
def specific_product_info(link) -> str:
    '''
    The function looks for a reviews of a specific product 
    and scrapes its information using the link.
    Args:
        link: string
    '''
    http = httplib2.Http()
    status, response = http.request(link)
    return text_from_html(response)
