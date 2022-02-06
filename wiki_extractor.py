# Importing Modules
import wikipedia
from scrapy import Selector
import requests
import html2text
import json

# wiki class will extract all related wikipedia pages provided the keyword and also extract perform extraction of paragraph content
class wiki:
    def __init__(self,keyword,num_urls,output):
        self.__keyword = keyword
        self.__num_urls = num_urls
        self.__output = output
    def outList(self):
        link_list = []
        key_list = wikipedia.search(self.__keyword,results=self.__num_urls)
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.bypass_tables = False
        xpat = "/html/body/div[3]/div[3]/div[5]/div[1]/p[2]"
        for i in key_list:
            page = wikipedia.page(i)
            url = page.url
            html = requests.get(url).content
            sel = Selector(text=html)
            p = sel.xpath(xpat).extract()
            para = h.handle(p[0]).replace("\n"," ").replace("*","")
            link_list.append({"url":url,"paragraph":para})
        with open(self.__output, "w") as final:
            json.dump(link_list, final)
            
__keyword = input("Enter keyword : ")
__num_urls = int(input("Enter number of urls : "))
__output = input("Enter name of json file : ")
obj = wiki(__keyword,__num_urls,__output)
obj.outList()
