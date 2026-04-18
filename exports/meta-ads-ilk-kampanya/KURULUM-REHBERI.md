# META ADS MANAGER — ADIM ADIM KURULUM REHBERİ

**Kepekçi Optik İlk Kampanya** · 100 TL/gün · 3 Creative · 15 Metin Varyasyonu

---

## ÖNCE OKUYUN

Bu rehber Meta Ads Manager'ı ilk defa kullananlar için hazırlandı. Her adımda ne tıklayacağınız, ne yazacağınız, ne seçeceğiniz net olarak yazılı. Sırayla takip edin, atlamayın.

**Başlamadan önce hazır olması gerekenler:**
- [x] Meta Business Manager hesabı (kurulu)
- [x] Reklam hesabı (kurulu)
- [x] Kredi kartı tanımlı (kurulu)
- [x] Meta Pixel ikas'ta aktif (kurulu — 9 Nis 2026)
- [x] 3 PNG creative hazır (bu klasörde)
- [x] 15 reklam metni (REKLAM-METINLERI.txt)
- [x] Google Maps linki: https://maps.app.goo.gl/ksHZg9u8xMxkA23SA

**Toplam süre:** ~45 dakika (ilk kez yapıyorsanız)

**Strateji özeti:**
- 1 kampanya (başlangıç için yeterli)
- Amaç: Traffic (mağazaya web/harita trafiği)
- Bütçe: 100 TL/gün (aylık 3000 TL)
- Hedef: Kilis + 20 km, 25-55 yaş
- 3 creative × 5 metin = 15 reklam varyasyonu
- Süre: 30 gün (1 ay sonra performansa göre karar)

---

## ADIM 0 — META ADS MANAGER'A GİRİŞ

1. Tarayıcıdan şu adrese git: **https://adsmanager.facebook.com**
2. Facebook hesabınla giriş yap
3. Sol üst köşede **Ads Manager** yazısını gör, doğru yerdesin
4. Sol üstteki reklam hesabı adını kontrol et — "Reklam Verme (1010841349637081)" olmalı
5. Dil Türkçe değilse: Sağ üst → profil resmi → Ayarlar → Dil → Türkçe seç

---

## ADIM 1 — KAMPANYA OLUŞTUR

1. Sol üst → yeşil **"+ Oluştur"** (Create) butonuna tıkla
2. Açılan pencerede **"Manuel Oluşturma"** (Manual Creation) seç
3. **"Kampanya Hedefi Seçin"** ekranı açılacak
4. **"Trafik"** (Traffic) seçeneğini tıkla
5. Altta **"Devam"** (Continue) butonuna bas

### Kampanya Bilgileri:

| Alan | Değer | Nereye Yazılır |
|------|-------|----------------|
| Kampanya adı | `Kepekci Optik — Genel Trafik` | Üstteki metin kutusu |
| Özel reklam kategorileri | **Boş bırak** | Yok |
| Kampanya detayları | **Varsayılan** | Dokunma |
| Performans amacı | **Bağlantı tıklamalarını en üst düzeye çıkar** | Açılan menüden seç |
| A/B test | **Kapalı** | Anahtar kapalı kalsın |
| Advantage Campaign Budget | **KAPALI** | Anahtar kapalı kalsın (biz reklam seti seviyesinde bütçe vereceğiz) |

6. Sayfanın sağ altında **"İleri"** (Next) butonuna tıkla

---

## ADIM 2 — REKLAM SETİ (AD SET)

Şimdi hedef kitleyi ve bütçeyi tanımlayacağız.

### 2.1 Reklam Seti Adı
Üstteki metin kutusuna yaz:
```
Kilis 25-55 — Genel Hedef
```

### 2.2 Dönüşüm Konumu (Conversion Location)
**"Web sitesi"** (Website) seçili olmalı

### 2.3 Performans Amacı
**"Bağlantı tıklamalarını en üst düzeye çıkar"** seçili olmalı (otomatik gelir)

### 2.4 Bütçe ve Programlama

| Alan | Değer |
|------|-------|
| Bütçe türü | **Günlük bütçe** (Daily budget) |
| Bütçe tutarı | **100 TL** |
| Başlangıç tarihi | **Bugün** (otomatik seçili) |
| Bitiş tarihi | **Belirleme** (ileride durdurursun) |

### 2.5 Hedef Kitle (Audience) — EN ÖNEMLİ KISIM

#### Özel Hedef Kitleler (Custom Audiences)
**Boş bırak** (ilk kampanyada kullanmıyoruz)

#### Konum (Location)
1. Açılan haritada arama kutusuna yaz: **Kilis, Türkiye**
2. Çıkan öneriden "Kilis, Türkiye" seç
3. Konumun etrafında yuvarlak bir alan çıkacak
4. Yuvarlağın çapını (Radius) değiştir: **+20 km**
5. Kilis merkez + çevre köyler kapsama girsin
6. "Bu konumdaki insanlar" (People living in or recently in this location) seçili olsun

#### Yaş (Age)
- Minimum: **25**
- Maksimum: **55**

#### Cinsiyet (Gender)
**Tümü** (All) seçili

#### Detaylı Hedefleme (Detailed Targeting)
"Detaylı hedefleme ekle" butonuna tıkla ve tek tek şunları ara ve ekle:
- **Gözlük** (Eyeglasses)
- **Güneş gözlüğü** (Sunglasses)
- **Moda** (Fashion)
- **Sağlık ve zindelik** (Health and wellness)

> NOT: Bazı ilgi alanları gelmeyebilir, önerilenlerden en yakınını seç.

#### Diller (Languages)
- **Türkçe** ekle

### 2.6 Yerleştirmeler (Placements)
**"Advantage+ yerleşimleri"** (Advantage+ placements) seçili olsun — Meta otomatik optimize eder.

### 2.7 İleri Butonu
Sayfanın sağ altında **"İleri"** (Next) butonuna bas.

---

## ADIM 3 — REKLAM 1 (AD 1 — Brand Awareness)

Şimdi ilk reklamı oluşturacağız.

### 3.1 Reklam Adı
Üstteki metin kutusuna yaz:
```
AD1 Brand Awareness — Varyasyon 1.1
```

### 3.2 Kimlik (Identity)
- Facebook Sayfası: **Kepekçi Optik** (senin sayfan)
- Instagram Hesabı: **@kepekcioptik** (bağlı)

### 3.3 Reklam Kurulumu (Ad Setup)
**"Manuel yükleme"** (Manual upload) seçili olsun

### 3.4 Format
**Tek Resim veya Video** (Single image or video) seç

### 3.5 Medya (Media)
1. **"Medya ekle"** → **"Görsel ekle"** (Add media → Add image)
2. Bilgisayardan seç: **AD1-Brand-Awareness.png** (bu klasörde)
3. Yüklenmesini bekle (birkaç saniye)
4. Meta bazen görseli kırpabilir — "Kırp" (Crop) ekranı çıkarsa "1:1" (kare) seçip onayla

### 3.6 Metin (Text)

**Birincil Metin (Primary Text):** REKLAM-METINLERI.txt dosyasından kopyala-yapıştır:

```
Kilis'te gözlüğün adresi Kepekçi Optik. Dünyaca ünlü markalar, miyop önleyici çocuk camları ve SGK reçete hizmeti tek adreste. Gözünüz bizde olsun. 👓
```

**Başlık (Headline):**
```
Kilis'in Gözlükçüsü
```

**Açıklama (Description):**
```
Dünyaca ünlü markalar · SGK reçete
```

### 3.7 Hedef (Destination)
- Web sitesi URL'si:
```
https://maps.app.goo.gl/ksHZg9u8xMxkA23SA
```
- Görünen bağlantı (Display link): **boş bırak**

### 3.8 Çağrı (Call to Action)
Açılır menüden: **"Yol Tarifi Al"** (Get Directions) seç

### 3.9 Tracking
- URL parameters: **boş bırak**
- Meta Pixel: **Kepekçi Optik Pixel** seçili olmalı (otomatik gelir)

### 3.10 Yayınla
Sağ altta **"Yayınla"** (Publish) butonuna basma henüz! Önce "Taslak olarak kaydet" (Save as Draft) seç — diğer 14 reklamı da hazırlayacağız.

---

## ADIM 4 — REKLAM 2-15 (ÇOĞALTMA YÖNTEMİ)

Tek tek baştan kurmak yerine AD1'i çoğaltıp metinleri değiştireceğiz. Çok daha hızlı.

### 4.1 Çoğaltma
1. AD1'in üstündeki **"Kopyala"** (Duplicate) butonuna tıkla (3 nokta menüsünde)
2. "Aynı reklam setinde kopyala" (Duplicate in same ad set) seç
3. Yeni reklam: "AD1 Brand Awareness — Varyasyon 1.1 — Kopya" adıyla oluşur

### 4.2 AD1 Varyasyon 1.2'yi Hazırla
1. Kopyalanmış reklamı tıkla (düzenlemeye geçer)
2. Adı değiştir: `AD1 Brand Awareness — Varyasyon 1.2`
3. Birincil Metin'i sil ve 1.2'yi yapıştır:
```
Çocuğunuzun gözleri değerli. Miyop önleyici çocuk camı çözümleri, dünyaca ünlü markalar ve profesyonel danışmanlık için Kepekçi Optik'e bekleriz. 👁️
```
4. Başlık: `Gözünüz Bizde Olsun`
5. Açıklama: `Miyop önleyici çocuk camı`
6. Görsel AYNI kalsın (dokunma)
7. URL ve CTA aynı kalsın (dokunma)
8. Taslak olarak kaydet

### 4.3 AD1 Varyasyon 1.3, 1.4, 1.5'i de aynı yöntemle hazırla
Her seferinde:
- AD1'i çoğalt
- Adı güncelle (1.3, 1.4, 1.5)
- Birincil Metin, Başlık, Açıklama'yı REKLAM-METINLERI.txt'den kopyala
- Görsel değişmesin
- Taslak kaydet

### 4.4 AD2 (Güneş Gözlüğü) Varyasyonları
1. İlk varyasyonu baştan kur (AD1 gibi):
   - Reklam adı: `AD2 Gunes Gozlugu — Varyasyon 2.1`
   - Görsel: **AD2-Gunes-Gozlugu.png** yükle
   - Metin 2.1'i REKLAM-METINLERI.txt'den kopyala
2. Sonra çoğaltma yöntemiyle 2.2, 2.3, 2.4, 2.5'i hazırla

### 4.5 AD3 (Dünyaca Ünlü Markalar) Varyasyonları
1. İlk varyasyonu baştan kur:
   - Reklam adı: `AD3 Dunyaca Unlu Markalar — Varyasyon 3.1`
   - Görsel: **AD3-Dunyaca-Unlu-Markalar.png** yükle
   - Metin 3.1'i kopyala
2. Çoğaltma ile 3.2, 3.3, 3.4, 3.5'i hazırla

### 4.6 Kontrol Listesi
Bitirdiğinde toplam reklam sayısı: **15**
- 5 adet AD1 (aynı görsel, farklı metinler)
- 5 adet AD2 (aynı görsel, farklı metinler)
- 5 adet AD3 (aynı görsel, farklı metinler)

---

## ADIM 5 — YAYINLAMA

1. Tüm 15 reklam hazır olduğunda sağ altta **"Tümünü Yayınla"** (Publish All) butonuna tıkla
2. Meta bir onay penceresi açar — "Yayınla" tıkla
3. Reklamlar "İnceleme aşamasında" (In Review) statüsüne geçer
4. **~15 dakika – 2 saat** içinde Meta incelemeyi tamamlar
5. Onaylanırsa "Aktif" (Active) statüsüne geçer ve yayınlanır

---

## ADIM 6 — İLK 24 SAAT

### Yapılacaklar:
1. **İlk 2 saat:** Reklamların durumunu kontrol et (Aktif / Reddedildi / İnceleme)
2. **Reddedilen varsa:** Meta sebep yazar — metni/görseli düzelt, tekrar gönder
3. **6 saat sonra:** İlk gösterim sayılarını gör (kaç kişi gördü, kaç kişi tıkladı)
4. **24 saat sonra:** İlk CTR (Click Through Rate) verisi gelir
   - İyi CTR: **%1+** (yerel mağaza için)
   - Düşük CTR: **<%0.5** (metin veya görsel değiştirmek gerekebilir)

### DOKUNMA!
İlk 3 gün **HİÇBİR ŞEYE DOKUNMA**. Meta algoritmasının öğrenme aşaması var. Sık değişiklik yapmak algoritmayı sıfırlar.

---

## ADIM 7 — 1 HAFTA SONRA

1. **Meta Ads Analyzer skill'ini kullan** — ben ekran görüntüsünden analiz yaparım
2. Kazanan metinleri belirle (hangi varyasyon en çok tıklandı)
3. Kaybeden metinleri durdur
4. Bütçeyi kazanan metinlere kaydır
5. Yeni metin varyasyonları dene (opsiyonel)

---

## ACİL DURUMLAR

### Reklam reddedildi
- Sebebi oku (Meta sana yazar)
- Yaygın sebepler:
  - **Çok fazla metin görseldeki** → görseldeki metin %20'den fazla olmasın
  - **Sağlık iddiası** → "göz muayenesi", "numarayı düzeltir" gibi ifadeler yasak
  - **Yanıltıcı içerik** → abartılı vaatler
- Düzelt ve tekrar gönder

### Hiç gösterim almıyor
- Hedef kitle çok dar olabilir — yaş aralığını genişlet (20-65)
- Bütçe çok düşük olabilir — 100 TL/gün yeterli, sabret

### Çok pahalı (yüksek CPM)
- İlk 3 gün sabret — algoritma öğreniyor
- 1 hafta sonra hâlâ pahalıysa hedef kitleyi genişlet

### Reklamı durdur
- Kampanya sayfasında reklamın yanındaki anahtarı kapat
- Para çekilmez, yeniden açabilirsin

---

## BENDEN YARDIM ALMAK

Herhangi bir adımda takılırsan:
1. **Ekran görüntüsü al** (Win + Shift + S)
2. Bana ver: "Şu adımda takıldım, ne yapayım?"
3. Sana adım adım söylerim

Yayın sonrası haftalık performans için:
1. Meta Ads Manager'dan CSV export al (veya ekran görüntüsü)
2. Bana gönder: "Haftalık raporu analiz et"
3. Meta Ads Analyzer skill ile kazanan/kaybeden analizi yaparım

---

## ÖZET KART (EKLENDİ)

| Parametre | Değer |
|-----------|-------|
| **Kampanya amacı** | Trafik |
| **Bütçe** | 100 TL/gün |
| **Aylık bütçe** | 3000 TL |
| **Konum** | Kilis + 20 km |
| **Yaş** | 25-55 |
| **Creative sayısı** | 3 |
| **Metin varyasyonu** | 15 (3×5) |
| **Hedef URL** | https://maps.app.goo.gl/ksHZg9u8xMxkA23SA |
| **CTA** | Yol Tarifi Al |
| **Süre** | 30 gün (ilk değerlendirme) |

---

İyi şanslar 🍀
