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

