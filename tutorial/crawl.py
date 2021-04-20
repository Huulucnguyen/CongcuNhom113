from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import multiprocessing
import pandas as pd
import numpy as np
from pandas import DataFrame
import googletrans
from googletrans import Translator

def load_url_selenium_shopee(url):
    # Selenium
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(PATH,options=op)
    driver.get(url)
    time.sleep(5)
    height = driver.execute_script("return document.body.scrollHeight")
    new = 1000
    while(new < height):
        driver.execute_script("window.scrollTo(0, {0});".format(new))
        new+=1000
        time.sleep(2)
    full_lst = []

    check= True
    old_list = []

    while check:

        new_list = []
        product_reviews = driver.find_elements_by_css_selector("[class='shopee-product-rating']")

        for product in product_reviews:
            main = product.find_element_by_css_selector("[class='shopee-product-rating__main']")
            review = main.find_element_by_css_selector("[class='shopee-product-rating__content']").text
            if (review != "" or review.strip()):
                new_list.append(review)
                full_lst.append(review)
                print(review)
        if(old_list==new_list):
            check = False
        else:
            old_list=new_list
        try:
            button_next=WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.shopee-icon-button.shopee-icon-button--right ")))
            driver.execute_script("arguments[0].click();", button_next)
          
        finally:
            time.sleep(2)
    driver.quit() 
    return full_lst
def clean_data(lst):
    df = DataFrame(lst, columns = ["Comment"])
    df.drop_duplicates(subset = 'Comment',keep = False,inplace = True)
    df['Comment'] = df['Comment'].str.replace(",","", regex=False)
    df['Comment'] = df['Comment'].str.replace(".","", regex=False)
    df["Comment"]=df["Comment"].apply(lambda x: str(x).split(" "))
    for i in range(len(df)):
        for index,value in enumerate(df["Comment"].iloc[i]):
            if len(value) >6:
                df["Comment"].iloc[i][index] = ""
    df["Comment"]= df["Comment"].apply(lambda x:" ".join(map(str,x)))
    df["Comment"] = df["Comment"].apply(lambda x:x.strip())
    df['Comment'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Comment'], inplace=True)
    clean_list = df['Comment'].tolist()
    return clean_list

def translate_cmt(lst):
    translator = Translator(service_urls=['translate.googleapis.com'])
    translated_cmt = []
    #lst = ['Bụng cảm giác hơi bó còn ống quần thì rộng hơn ảnh mẫu k được đẹp', 'Form đẹp', 'Quần đẹp giao hàng nhanh', 'quần vừa  nhưng ống hơi dài phải mang đi cắt màu trắng nhưng vải ko bị mỏng quá mặc ko bị lộ Đóng cúc rồi thì phần mép khóa hơi ko khít nên cho 4* thôi nhé', 'Quần lên dáng khá là xinh ạ', 'Mình cao 1m58 48kg mặc vừa size S quần chất tương đối đẹp khá mềm', 'Quần chất hơi mỏng ko đứng dáng quần lắm', 'Áo chất đẹp lắm ạ']
    for cmt in lst:
        new_lst = []
        result = translator.translate(cmt,src='vi',dest='en')
        new_lst.append(result.text) 
        translated_cmt.append(new_lst)
    return translated_cmt

def get_list(url):
    web_list = load_url_selenium_shopee(url)
    cleaned_list = clean_data(web_list)
    translated_list =translate_cmt(cleaned_list)
    return translated_list
#print(get_list("https://shopee.vn/Qu%E1%BA%A7n-%C3%82u-Chi%E1%BA%BFt-Ly-20AGAIN-QAA0985-i.106719091.9413140222"))
    
