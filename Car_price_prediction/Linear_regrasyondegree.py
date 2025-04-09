import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score

# CSV dosyasını okuma
Data_set = pd.read_csv('Araba_bilgileri_önişleme')

# Kullanıcıdan giriş alma
Uretim_yili = int(input('İstediğiniz arabanın modelini (üretim yılı) giriniz: '))
Kilometre = int(input('İstediğiniz arabanın kilometresini giriniz: '))
Yakit_Tipi = int(input('İstediğiniz aracın yakıt tipini giriniz (1. dizel, 2. LPG & Benzin, 3. Benzin): '))
Boya_Degisen = int(input('İstediğiniz aracın boya ve değişen sayısını giriniz (bunların toplamını giriniz): '))

# Özellikler ve hedef değişken
X = Data_set[["Üretim-yılı", "Kilometre", "Yakıt-Tipi", "Boya-Değişen"]]
y = Data_set["Fiyat"]

# Veriyi eğitim ve test olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Veriyi standartlaştırma
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Polinomsal özellik eklemek (2. derece ve 3. derece için ayrı ayrı)
poly_2 = PolynomialFeatures(degree=2)
poly_3 = PolynomialFeatures(degree=3)

# 2. derece polinomsal özellikler
X_train_poly_2 = poly_2.fit_transform(X_train)
X_test_poly_2 = poly_2.transform(X_test)

# 3. derece polinomsal özellikler
X_train_poly_3 = poly_3.fit_transform(X_train)
X_test_poly_3 = poly_3.transform(X_test)

# Modeli oluşturma ve eğitme (2. derece polinom)
model_poly_2 = LinearRegression()
model_poly_2.fit(X_train_poly_2, y_train)

# Modeli oluşturma ve eğitme (3. derece polinom)
model_poly_3 = LinearRegression()
model_poly_3.fit(X_train_poly_3, y_train)

# Test verisi ile tahmin yapma (2. derece)
y_pred_poly_2 = model_poly_2.predict(X_test_poly_2)

# Test verisi ile tahmin yapma (3. derece)
y_pred_poly_3 = model_poly_3.predict(X_test_poly_3)

# MSE'yi hesaplama (2. derece)
mse_poly_2 = mean_squared_error(y_test, y_pred_poly_2)
r2 = r2_score(y_test, y_pred_poly_2)
print(f'2. derece Polinom için Mean Squared Error: {mse_poly_2}')
print(f'2. derece polinom için doğruluk oranı {r2} ')

# MSE'yi hesaplama (3. derece)
mse_poly_3 = mean_squared_error(y_test, y_pred_poly_3)
r2_poly3 = r2_score(y_test, y_pred_poly_3)
print(f'3. derece Polinom için Mean Squared Error: {mse_poly_3}')
print(f'3. derece polinom için doğruluk oranı {r2_poly3}')

# Kullanıcıdan alınan verileri hazırlama
giris_verisi = pd.DataFrame({
    "Üretim-yılı": [Uretim_yili],
    "Kilometre": [Kilometre],
    "Yakıt-Tipi": [Yakit_Tipi],
    "Boya-Değişen": [Boya_Degisen]
})

# Kullanıcıdan alınan verileri standartlaştırma
giris_verisi_scaled = sc.transform(giris_verisi)

# Kullanıcı verileri için 2. derece polinomsal tahmin yapma
giris_verisi_poly_2 = poly_2.transform(giris_verisi_scaled)
tahmini_fiyat_poly_2 = model_poly_2.predict(giris_verisi_poly_2)
print(f'{Uretim_yili} model arabanın tahmin edilen fiyatı (2. derece): {tahmini_fiyat_poly_2[0]:,.2f} TL')

# Kullanıcı verileri için 3. derece polinomsal tahmin yapma
giris_verisi_poly_3 = poly_3.transform(giris_verisi_scaled)
tahmini_fiyat_poly_3 = model_poly_3.predict(giris_verisi_poly_3)
print(f'{Uretim_yili} model arabanın tahmin edilen fiyatı (3. derece): {tahmini_fiyat_poly_3[0]:,.2f} TL')

