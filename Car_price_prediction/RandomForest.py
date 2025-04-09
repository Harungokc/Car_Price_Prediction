import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,r2_score

# CSV dosyasını okuma
data = pd.read_csv('Araba_bilgileri_önişleme')

data = pd.read_csv('Araba_bilgileri_önişleme1')

df = pd.DataFrame(data)

# Bağımsız ve bağımlı değişkenleri ayırma
X = df[["Üretim-yılı", "Kilometre", "Yakıt-Tipi", "Boya-Değişen"]]
y = df["Fiyat"]

# Eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Veriyi standartlaştırma
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# RandomForestRegressor modelini oluşturma ve eğitme
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Test verisi ile tahmin yapma
y_pred = model.predict(X_test)

# Doğruluk metrikleri
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'ortalama kare hata {mse}')
print(f'R^2 skoru doğruluk oranı  {r2}')

# Kullanıcıdan giriş alma
Uretim_yili = int(input('İstediğiniz arabanın modelini (üretim yılı) giriniz: '))
Kilometre = int(input('İstediğiniz arabanın kilometresini giriniz: '))
Yakit_Tipi = int(input('İstediğiniz aracın yakıt tipini giriniz (1. dizel, 2. LPG & Benzin, 3. Benzin): '))
Boya_Degisen = int(input('İstediğiniz aracın boya ve değişen sayısını giriniz (bunların toplamını giriniz): '))

# Tahmin için kullanıcı verisini hazırlama
giris_verisi = pd.DataFrame({
    'Üretim-yılı': [Uretim_yili],
    'Kilometre': [Kilometre],
    'Yakıt-Tipi': [Yakit_Tipi],
    'Boya-Değişen': [Boya_Degisen]
})

# Tahmin yapma
tahmin = model.predict(giris_verisi)

print(f"Tahmini fiyat: {tahmin[0]:,.2f} TL")



