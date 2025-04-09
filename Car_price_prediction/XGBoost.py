import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# CSV dosyasını okuma
Data_set = pd.read_csv('Araba_bilgileri_önişleme1')

# Sütunları kontrol edin
print(Data_set.columns)

# Özellikler ve hedef değişken (sütun isimlerini kontrol ederek seçiyoruz)
X = Data_set[["Üretim-yılı", "Kilometre", "Yakıt-Tipi", "Boya-Değişen"]]
y = Data_set["Fiyat"]

# Kategorik ve sayısal özellikleri ayırma
categorical_features = ['Yakıt-Tipi']
numeric_features = ['Üretim-yılı', 'Kilometre', 'Boya-Değişen']

# Pipeline: One-Hot Encoding ve Ölçeklendirme
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

# XGBoost Regressor modelini tanımlama
xgb_model = XGBRegressor(objective='reg:squarederror', random_state=0)

# Pipeline oluşturma
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', xgb_model)])

# Hiperparametreler için Grid Search
param_grid = {
    'regressor__n_estimators': [100, 200],
    'regressor__max_depth': [3, 5],
    'regressor__learning_rate': [0.01, 0.1],
}

# Grid Search ile en iyi modeli seçme
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='r2')
grid_search.fit(X, y)

# En iyi hiperparametreleri ve modeli alma
best_model = grid_search.best_estimator_
print("En iyi hiperparametreler:", grid_search.best_params_)

# Veriyi eğitim ve test olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# En iyi modelle yeniden eğitme
best_model.fit(X_train, y_train)

# Test verisiyle tahmin yapma
y_pred = best_model.predict(X_test)

# Performans değerlendirme
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f'R^2 Doğruluk Oranı: {r2}')
print(f'Ortalama Mutlak Hata (MAE): {mae}')

# Kullanıcıdan giriş alma
Uretim_yili = int(input('İstediğiniz arabanın modelini (üretim yılı) giriniz: '))
Kilometre = int(input('İstediğiniz arabanın kilometresini giriniz: '))
Yakit_Tipi = int(input('İstediğiniz aracın yakıt tipini giriniz (1. dizel, 2. LPG & Benzin, 3. Benzin): '))
Boya_Degisen = int(input('İstediğiniz aracın boya ve değişen sayısını giriniz (bunların toplamını giriniz): '))

# Kullanıcıdan alınan veriyi bir DataFrame'e dönüştürme
input_data = pd.DataFrame({
    'Üretim-yılı': [Uretim_yili],
    'Kilometre': [Kilometre],
    'Yakıt-Tipi': [Yakit_Tipi],
    'Boya-Değişen': [Boya_Degisen]
})

# Tahmin için preprocessor ve modelden geçirme
predicted_price = best_model.predict(input_data)
print(f'{Uretim_yili} model arabanın tahmin edilen fiyatı: {predicted_price[0]:.2f} TL')



