import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


def urleler(url):
    # Arabam.com'daki ID'leri bir listeye koyuyoruz
    ids = []


    # Çekilecek URL'leri depolamak için bir liste
    urls = []

    # URL'den sayfayı alıp parse ediyoruz
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tüm ID'ler için döngü ile URL'leri çekiyoruz
    base_url = "https://www.arabam.com"

    for id in ids:
        listing = soup.find('tr', id=id)
        if listing:  # Eğer listing None değilse işlem yap
            relative_url = listing.find('a')['href']
            full_url = base_url + relative_url
            urls.append(full_url)
        else:
            print(f"ID {id} bulunamadı.")

    return urls




def araba_bilgileri(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    Data = []

    try:
        price = soup.find('div', class_='product-price').find('div',{'data-testid': 'desktop-information-price'}).text.strip()
    except AttributeError:
        price = np.nan

    try:
        ilan_no = soup.find('div', class_='property-item').find('div', id='js-hook-copy-text').text.strip()
    except AttributeError:
        ilan_no = np.nan

    try:
        uretim_yili = soup.find_all('div', class_='property-item')[5].find('div', class_='property-value').text.strip()
    except AttributeError:
        uretim_yili = np.nan

    try:
        marka = soup.find_all('div', class_='property-item')[2].find('div', class_='property-value').text.strip()
    except AttributeError:
        marka = np.nan

    try:
        model = soup.find_all('div', class_='property-item')[3].find('div', class_='property-value').text.strip()
    except AttributeError:
        model = np.nan

    try:
        kilometre = soup.find_all('div', class_='property-item')[6].find('div', class_='property-value').text.strip()
    except ArithmeticError:
        kilometre = np.nan

    try:
        yakit_tipi = soup.find_all('div', class_='property-item')[8].find('div', class_='property-value').text.strip()
    except ArithmeticError:
        yakit_tipi = np.nan

    try:
        boya_degisen = soup.find_all('div', class_='property-item')[17].find('div', class_='property-value').text.strip()
    except (IndexError, AttributeError):
        boya_degisen = np.nan

    try:
        kimden = soup.find_all('div', class_='property-item')[19].find('div', class_='property-value').text.strip()
    except (IndexError, AttributeError):
        kimden = np.nan


    car_info = {
        "Fiyat": price,
        "İlan No": ilan_no,
        "Üretim yılı": uretim_yili,
        "Marka": marka,
        "Model": model,
        "Kilometre": kilometre,
        "Yakıt Tipi": yakit_tipi,
        "Boya - Değişen": boya_degisen
    }


    Data.append(car_info)
    print(Data)

    return Data

# Ana URL
url = 'https://www.arabam.com/ikinci-el?searchText=audi%20a6&page=13'
urls = urleler(url)

all_data = []

# Her URL için araba bilgilerini al
for url in urls:
    car_data = araba_bilgileri(url)
    all_data.extend(car_data)


# DataFrame oluştur ve CSV dosyasına yaz
df = pd.DataFrame(all_data)
df.to_csv('Araba_bilgileri1.csv', index=False, encoding='utf-8')









