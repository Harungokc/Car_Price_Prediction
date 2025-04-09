import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV dosyasını okuma
Data_set = pd.read_csv('Araba_bilgileri.csv')

# Gereksiz sütunları çıkarma
Data_set = Data_set.drop(['İlan-No', 'Marka', 'Model'], axis=1)

# Yakıt-Tipi sütununu etiketleme
from sklearn.preprocessing import LabelEncoder

label_encoder = {}
for column in ['Yakıt-Tipi']:
    le = LabelEncoder()
    Data_set[column] = le.fit_transform(Data_set[column])
    label_encoder[column] = le


Data_set['Fiyat'] = Data_set['Fiyat'].astype(str).str.replace(' TL', '', regex=False)
Data_set['Kilometre'] = Data_set['Kilometre'].astype(str).str.replace(' km', '', regex=False)

# Virgül ve noktaları kaldırma
Data_set['Fiyat'] = Data_set['Fiyat'].str.replace('.', '', regex=False)  # Noktaları kaldır
Data_set['Kilometre'] = Data_set['Kilometre'].str.replace('.', '', regex=False)  # Noktaları kaldır

# Sayısal değerlere dönüştürme
Data_set['Fiyat'] = pd.to_numeric(Data_set['Fiyat'], errors='coerce')
Data_set['Kilometre'] = pd.to_numeric(Data_set['Kilometre'], errors='coerce')


# 'Boya-Değişen' sütununu sınıflandıran fonksiyon
def classify_boyalı_değişen(boya_degisen):
    deger = 0

    if pd.isna(boya_degisen):
        return None  # NaN'lar None döner

    # Orijinal durum için 0 döner
    if 'orjinal' in boya_degisen.lower():
        return 0

    # Değişen sayısını kontrol et
    değişen = 0
    if 'değişen' in boya_degisen:
        try:
            değişen = int(boya_degisen.split('değişen')[0].strip())  # Değişen sayısını al
        except ValueError:
            pass
        deger += değişen

    # Boyalı sayısını kontrol et
    boyalı = 0
    if 'boyalı' in boya_degisen:
        try:
            boyalı = int(boya_degisen.split('boyalı')[0].strip().split()[-1])  # Boyalı sayısını al
        except ValueError:
            pass
        deger += boyalı

    if deger > 0:
        return deger

    # Belirtilmemiş, Takasa uygun ve Galeriden kontrolü
    if 'Belirtilmemiş' in boya_degisen:
        return None  # Ortalamayı atayacağız
    elif 'Takasa' in boya_degisen:
        return None  # Ortalamayı atayacağız
    elif 'Galeriden' in boya_degisen:
        return None  # Ortalamayı atayacağız

    elif 'Diğer' in boya_degisen:
        return None
    return 'diğer'



# 'Boya-Değişen' sütununu sınıflandırma fonksiyonunu uygulama
Data_set['Boya-Değişen'] = Data_set['Boya-Değişen'].apply(classify_boyalı_değişen)

# Numeric olmayan değerleri filtreleme (NaN ve 'Diğer' gibi)
numeric_values = Data_set['Boya-Değişen'].dropna()  # NaN'ları çıkartıyoruz
numeric_values = numeric_values[numeric_values.apply(lambda x: isinstance(x, (int, float)))]  # Sadece sayısal veriler

# Ortalamayı hesapla ve yuvarla
average_value = (numeric_values.mean())

# None veya NaN olan yerlere yuvarlanmış ortalama değeri atama
Data_set['Boya-Değişen'] = Data_set['Boya-Değişen'].apply(lambda x: average_value if pd.isna(x) else x)

# Boya-Değişen kolonunu 3'ten küçükler için 0, 3'ten büyükler için 1 olarak ayarlama
Data_set['Boya-Değişen'] = Data_set['Boya-Değişen'].apply(lambda x: 0 if x < 3 else 1)

# Kilometreye logaritmik dönüşüm uygulama
Data_set['Kilometre'] = np.log1p(Data_set['Kilometre'])

# Üretim yılı yerine aracın yaşını hesaplama (2024 yılına göre)
Data_set['Yaş'] = 2024 - Data_set['Üretim-yılı']
Data_set = Data_set.drop(columns=['Üretim-yılı'])  # Üretim yılı kolonunu kaldırma

# Sonuçları yazdır
print(Data_set.head(50))

df = pd.DataFrame(Data_set)
df.to_csv('Araba_bilgileri_önişleme1', index=False, encoding='utf-8')













