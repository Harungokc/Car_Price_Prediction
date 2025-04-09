# 🚗 Araç Fiyat Tahmini Projesi (Audi A6)

## 📌 Proje Tanımı

Bu proje, arabam.com üzerindeki ikinci el **Audi A6** araç ilanlarından veri toplayarak, bu verilerle araçların tahmini piyasa değerini hesaplayan bir **makine öğrenmesi uygulamasıdır**. Projede kullanılan tüm veriler, web kazıma (web scraping) yöntemiyle toplanmış ve çeşitli algoritmalarla değerlendirilmiştir.

> ⚠️ **Not: Bu proje sadece eğitim ve analiz amaçlıdır. Ticari amaçla kullanılmamakta ve herhangi bir veri satışı yapılmamaktadır.**

---

## 🔍 Proje Amacı

- İkinci el araçların teknik ve fiziksel özelliklerine dayanarak tahmini satış fiyatını hesaplayabilen bir model geliştirmek.
- Fiyat tahmini algoritmalarının doğruluğunu farklı yöntemlerle karşılaştırmak.
- Web scraping, veri ön işleme ve regresyon modelleme adımlarını tek bir projede birleştirerek uçtan uca bir makine öğrenmesi süreci sunmak.

---

## 🌐 Web Scraping Yöntemleri

### 📄 1. `BeautifulSoup` Kullanımı
- **Statik içerik** barındıran sayfalardan veri almak için kullanılmıştır.
- `requests` kütüphanesi ile sayfa içeriği çekilir, `BeautifulSoup` ile parse edilir.
- Sayfadaki `<div class='property-item'>`, `<span class='product-price'>` gibi elemanlardan:
  - Fiyat
  - Marka
  - Model
  - Kilometre
  - Yakıt türü
  - Boya / Değişen bilgileri çekilmiştir.

### 🧭 2. `Selenium` Kullanımı
- Dinamik sayfalarda (JavaScript ile yüklü içerikler) çalışmak için kullanılmıştır.
- Kullanıcı simülasyonu (arama, tıklama, veri görselleştirme) yapılmıştır.
- Özellikle ilan detay sayfalarında, butonlarla erişilen bilgiler bu yolla alınmıştır.

### 🔗 3. URL Oluşturma
- İlanlara ait `tr id="listing...` yapılarına ulaşarak ilan URL’leri otomatik olarak birleştirilmiştir.

---

## 🧼 Veri Ön İşleme Aşamaları

1. **Gereksiz sütunlar** kaldırıldı (İlan No, Marka, Model).
2. **Fiyat** ve **kilometre** metin olarak geldiği için:
   - TL, km ifadeleri temizlendi.
   - Nokta (.) gibi ayraçlar kaldırıldı.
   - Sayısal verilere dönüştürüldü.
3. **Yakıt türü**, `LabelEncoder` ile sayısal hale getirildi.
4. **Boya-Değişen** kolonuna özel:
   - Metne dayalı analizle "kaç parça değişmiş" hesaplandı.
   - Değeri 3'ten fazla olanlar `1` (hasarlı), 3'ten az olanlar `0` (temiz) olarak etiketlendi.
5. **Yaş** kolonu: `2024 - üretim yılı` olarak hesaplandı.
6. **Log dönüşümü** kilometre için uygulandı.

---

## 🧠 Kullanılan Makine Öğrenimi Modelleri

Aşağıdaki modellerle fiyat tahmini yapılmıştır:

- 📊 **Linear Regression**
- 🌲 **Random Forest Regressor**
- 🔵 **K-Nearest Neighbors (KNN)**
- 📈 **Naive Bayes (Regresyon uyarlamasıyla test edildi)**
- 💻 **Support Vector Regression (isteğe bağlı eklenebilir)**

Her modelin `MSE (Ortalama Kare Hata)` ve `R² (Doğruluk Skoru)` metrikleriyle başarısı ölçülmüştür.

---

## 🎯 Model Performans Kriterleri

| Model Adı            | Ortalama Kare Hata (MSE) | R² Skoru (Doğruluk) |
|----------------------|---------------------------|----------------------|
| Random Forest        | 61390644851.7168          | 0.9640759278813739   |
| Linear Regression    | 220683873485.44965        | 0.8708620278275616   |
| KNN Regressor        | 114044682745.11765        | 0.9332642714932018   |
| Naive Bayes (deneme) | 1307676731862.7646        | 0.23478449629001552  |
| XGBoost              | 463432.80592105264        | 0.7967350357574976   |
| Linear Regression (2. derece) | 69112808113.41727| 0.9574713947633131   |
| Linear Regression (3. derece) | 437849444017.82556| 0.7305690990419778   |

> 📌 En iyi sonuç **Random Forest Regressor** ile elde edilmiştir. Bu model hem doğruluğu hem de esnekliğiyle öne çıkmaktadır.

---

## 💡 Örnek Kullanım: Tahmin Aracı

Kullanıcıdan alınan girişler ile tahmini araç fiyatı hesaplanabilir:

```python
Uretim_yili = 2014
Kilometre = 125000
Yakit_Tipi = 1  # Dizel
Boya_Degisen = 1  # Hasarsız

tahmin = model.predict([[Uretim_yili, Kilometre, Yakit_Tipi, Boya_Degisen]])
print(f"Tahmini fiyat: {tahmin[0]:,.2f} TL")

📈 Görselleştirme
Gerçek ve tahmin edilen fiyatlar karşılaştırıldı.
Scatter plot ile model başarısı görselleştirildi.

🧪 Teknik Altyapı
Python 3
Pandas / NumPy
Scikit-learn
BeautifulSoup / Requests / Selenium
Matplotlib / Seaborn

🔐 Etik & Lisans
📢 Bu proje sadece kişisel ve eğitimsel amaçlarla yapılmıştır.

arabam.com sitesi üzerinden elde edilen veriler, açık erişimli olarak sunulmuş ilan verileridir.
Hiçbir şekilde veri satışı veya ticari kazanç amacı güdülmemektedir.
Web scraping işlemleri minimum sayıda, düşük yoğunlukla yapılmış; sunucuya zarar vermeyecek şekilde tasarlanmıştır.

👨‍💻 Geliştirici:
Harun Gökce
📬 GitHub: Harungokc

