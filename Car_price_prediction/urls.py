import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.arabam.com/ikinci-el?searchText=audi%20a6'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
ilanlar = soup.find_all('div', class_='listing-table-wrapper')
# Belirli bir ID'ye sahip ilanı bulalım
url1 = soup.find('tr', id='listing26774758').find('a')['href']

# Base URL ile birleştirip tam URL'yi elde edelim
base_url = "https://www.arabam.com"
full_url = base_url + url1






