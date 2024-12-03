from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import httplib2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain_core.runnables import RunnableConfig


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
        stripped_text = text
        if (stripped_text == "ABOUT"):
            flag = False
            break
        if (flag):
            visible_text_list.append(stripped_text)

    result_text = "\n".join(visible_text_list)

    return result_text


def response_html(link):
    driver = webdriver.Chrome()
    driver.get(link)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/p/']"))
        )
        return driver.page_source
    finally:
        driver.quit()


def compare_products(ids) -> str:
    '''
    This function compares flipkart products using web scraping a webpage of the comparisions.
    The webpage is loaded using the product ids of the products.
    '''
    http = httplib2.Http()
    link = "https://www.flipkart.com/product/compare?ids="

    counter = 0
    for id in ids:
        if (counter <= 3):
            link += id+','
            counter += 1
    link = link[:-1]
    print(link)

    response = response_html(link)

    # status, response = http.request(
    #     "https://www.flipkart.com/mobile/compare?ids=MOBGYT2HEYWFCG8Q,MOBHYFPPYRCQZMHG")
    # print((response))
    # with open("results.txt", "w", encoding="utf-8") as f:
    # f.write(text_from_html(response))

    return text_from_html(response)
