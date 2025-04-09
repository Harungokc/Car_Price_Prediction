import pandas as pd
import numpy
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

Data = []

driver = webdriver.Chrome()
driver.get('https://www.arabam.com/')
time.sleep(2)


search_box = driver.find_element(By.ID, "search-input-desktop")
search_box.send_keys('Audi A6')


search_button = driver.find_element(By.XPATH, "//*[@id='wrapper']/header/div[4]/div/div/div[1]/div/button")
search_button.click()

time.sleep(5)

search_button1 = driver.find_element(By.XPATH, "//*[@id='listing26774758']")
search_button1.click()

time.sleep(5)

pirice_element = driver.find_element(By.CLASS_NAME, "product-price")
pirice = pirice_element.text

print(pirice)

property_items = driver.find_elements(By.CLASS_NAME, "property-item")

for item in property_items:
    # property-key ve property-value elemanlarını bulalım
    property_key = item.find_element(By.CLASS_NAME, "property-key").text
    property_value = item.find_element(By.CLASS_NAME, "property-value").text

    # Veriyi ekrana yazdıralım ve listeye ekleyelim
    print(f"{property_key}: {property_value}")
    Data.append({property_key: property_value})

# Tarayıcıyı kapatalım
driver.quit()

# Verileri pandas DataFrame'e çevirelim ve bir tablo olarak gösterelim
df = pd.DataFrame(Data)
print(df)


