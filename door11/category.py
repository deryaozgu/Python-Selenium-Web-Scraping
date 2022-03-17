import os
import time
from telnetlib import EC
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request

class Category:
    text = ""
    link = ""
    browser = ""
    subcategory_list_link = []
    subcategory_list_name = []
    sub_subcategory_list = []
    src=[]
    sub_category=""
    category = []
    sb_category = []
    sayac=0

    def __init__(self, link, browser):
        self.link = link
        self.browser = browser

    def gotolink(self):
        self.browser.get(self.link)
        time.sleep(2)

    def subcategory(self):
        x=2
        while True:
          if  "Next Page »" in self.browser.page_source:
             subCategory = self.browser.find_elements_by_class_name("entry-title")
             for i in subCategory:
                 self.subcategory_list_link.append(i.find_element_by_tag_name("a").get_attribute("href"))
                 self.subcategory_list_name.append(i.find_element_by_tag_name("a").text)
             time.sleep(2)
             new_link=self.link+"page/"+str(x)+"/"
             self.browser.get(new_link)
             x=x+1
          else:
              subCategory = self.browser.find_elements_by_class_name("entry-title")
              for i in subCategory:
                  self.subcategory_list_link.append(i.find_element_by_tag_name("a").get_attribute("href"))
                  self.subcategory_list_name.append(i.find_element_by_tag_name("a").text)
              time.sleep(4)
              break
        for i in self.subcategory_list_name:
             print(i)


    def sub_subcategory(self):
        self.text = self.browser.find_element_by_class_name("page-title").text
        a = 0
        os.makedirs("photos/"+self.text, mode=0o755, exist_ok=True)
        for i in self.subcategory_list_name:
            self.sub_subcategory_list.append(i)
            self.sub_category=i
            os.makedirs("photos/" + self.text + "/" + self.sub_category, mode=0o755, exist_ok=True)
            time.sleep(2)
            self.browser.get(self.subcategory_list_link[a])
            time.sleep(4)
            element = self.browser.find_element_by_tag_name("body")
            for i in range(30):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            time.sleep(3)
            div = self.browser.find_elements_by_class_name("pgcsimplygalleryblock-masonry-item-wrap")
            x=1
            for i in div:
                s=i.find_element_by_tag_name("img").get_attribute("src")
                self.sub_subcategory_list.append(s)
                time.sleep(0.3)
                self.src.append(s)
                time.sleep(0.3)
                urllib.request.urlretrieve(s,
                                           "photos/" + self.text + "/" + self.sub_category + "/" + str(x) + ".jpg")
                time.sleep(0.7)
                self.sayac+=1
                x+=1
            a += 1
            print(self.sayac)
            self.data_frame(self.sayac)
            self.sayac=0
            time.sleep(2)
        time.sleep(3)

    def data_frame(self,sayi):
        time.sleep(1)
        for i in range (0,sayi):
            self.category.append(self.text)
            self.sb_category.append(self.sub_category)

    def txt(self):
        with open(self.text + ".txt", "w", encoding="UTF-8") as file:
            for k in self.sub_subcategory_list:
                file.write(k + "\n")
        self.sub_subcategory_list.clear()
        self.subcategory_list_link.clear()
        self.subcategory_list_name.clear()

    def dt_frame(self):
        df_list = {"category": self.category,
                   "sb": self.sb_category,
                   "url": self.src}
        dataframe = pd.DataFrame(df_list)
        print(dataframe)

