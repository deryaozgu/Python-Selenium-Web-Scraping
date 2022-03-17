import os

from selenium import webdriver
import time
from category import Category

if __name__ == '__main__':
    browser = webdriver.Chrome("C:\Program Files\driver\chromedriver.exe")
    browser.get("https://door11.com/")
    time.sleep(2)
    seasons_list = []
    #ilk kategori kategoriler dışında onun alınması
    new_seasons=browser.find_element_by_id("menu-item-195234").find_element_by_tag_name("a")
    seasons_list.insert(0,new_seasons.get_attribute("href"))
    time.sleep(1)
    #diğer kategorilerin listeye eklenmesi
    seasons=browser.find_element_by_class_name("sub-menu").find_elements_by_tag_name("li")
    for i in seasons:
        seasons_list.append(i.find_element_by_tag_name("a").get_attribute("href"))
    #kategorilerin classa yollanma işlemi
    sayac=0
    os.mkdir("photos")
    for link in seasons_list:
        if(link == "https://door11.com/fashion/collections/spring-2021-menswear/"):
            continue
        isim= Category(link,browser)
        isim.gotolink()
        isim.subcategory()
        isim.sub_subcategory()
        isim.txt()
    isim.dt_frame()
    browser.close()



