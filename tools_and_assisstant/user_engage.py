from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import httplib2
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

@tool
def user_engager() -> str:
    '''
    The function returns information about the summarization of the overall conversations
    '''
    return "Got it. I am looking for the relevent data. PLease let me know if you need any help."
