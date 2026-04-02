# AI Video Üretim Teknikleri — PDF'den Öğrenilenler

Kaynak: "AI ile Video Üretimi" (sakevoid & vibeeval, 334 sayfa)

---

## 7 Katmanlı Prompt Yapısı (Video İçin)

Her AI video prompt'u bu 7 katmanda yazılır:

1. **Konu** — Kim/ne var, fiziksel detaylar (yaş, kıyafet, renk)
2. **Sahne** — Mekan, objeler, arka plan detayları
3. **Hareket** — Karakter + nesne + ortam hareketleri (yön, hız)
4. **Kamera** — Açı, hareket, lens (close-up, wide, tracking, dolly)
5. **Işık** — Yön, renk, şiddet (golden hour, stüdyo, backlight)
6. **Atmosfer** — Mood, his (sinematik, huzurlu, dramatik)
7. **Teknik** — Çözünürlük, FPS, stil referansı (4K, 24fps, film grain)

### Kamera Açıları
| Açı | Kullanım | Verdiği His |
|-----|----------|-------------|
| Close-up | Yüz ifadesi, duygu | Samimiyet, gerilim |
| Medium shot | Karakter + ortam | Doğal, dengeli |
| Wide shot | Mekan tanıtımı | Büyüklük, epik |
| Low angle | Aşağıdan yukarı | Güç, hakimiyet |
| Bird's eye | Üstten görünüm | Kontrol, perspektif |

### Kamera Hareketleri
| Hareket | Açıklama | Kullanım |
|---------|----------|----------|
| Static | Sabit | Sakinlik, gözlem |
| Pan | Yatay dönme | Mekan tarama |
| Dolly-in | Sahneye yaklaşma | Odaklanma, gerilim |
| Tracking | Karakteri takip | Aksiyon |
| Crane | Yukarı/aşağı | Sinematik, epik |

---

## AI Video Araçları (2026)

| Araç | En İyi Olduğu Alan | Fiyat |
|------|---------------------|-------|
| **Kling 2.6** | Karakter tutarlılığı (Elements), en kapsamlı | Ücretsiz / $10/ay |
| **Veo 3.1** | Sinematik kalite, 4K, 148s extend | $7.99/ay |
| **Runway Gen-4.5** | 60s tek seferde, stil kontrolü | $12/ay |
| **Sora 2** | Hikaye anlatımı, narratif derinlik | $20/ay |
| **Seedance 2.0** | Beat-sync müzik videosu, lip-sync | ByteDance |
| **Pika 2.5** | Hızlı üretim, SFX | Ücretsiz + Pro |

### Kepekçi Optik İçin Önerilen Araç Kombinasyonu
**Ücretsiz başlangıç:** Kling (ücretsiz 66 kredi/gün) + CapCut (montaj)
**İdeal:** Kling Pro ($10/ay) + CapCut + Claude

---

## Reels/TikTok İçerik Yapısı

### Hook-Body-CTA Formatı
| Bölüm | Süre | İçerik |
|-------|------|--------|
| **Hook** | 0-3s | Dikkat çekici soru/görsel/şok |
| **Body** | 3-12s | Ana içerik, bilgi, çözüm |
| **CTA** | 12-15s | Net aksiyon çağrısı |

### Hook Türleri (İlk 3 Saniye = Videonun %70'i)
1. **Soru:** "Hiç progresif camla hem uzağı hem yakını net gördüğünüzü düşünün!"
2. **İddia:** "Bu cam teknolojisi gözlük kullanımını sonsuza dek değiştirdi."
3. **Şok:** "Çocukların %30'unda miyopi var — ve artıyor!"
4. **Gizem:** "Kimsenin bilmediği bir şey göstereceğim…"
5. **Sayı:** "3 adımda doğru gözlük seçmenin yolu."

### İçerik Template'leri (Kepekçi Optik İçin)
1. **"Biliyor muydun?"** — Optik bilgi/şok
2. **"Önce & Sonra"** — Bulanık görüş vs net görüş
3. **"3 Şey"** — Listicle format
4. **"POV"** — "POV: İlk kez progresif cam takıyorsun"

---

## 5 Adımlı Video Prodüksiyon Pipeline

```
1. STRATEJİ & BRIEF — Ne, neden, kimin için?
2. STORYBOARD & SCRIPT — 6 karelik şablon, shot list
3. ÜRETİM — Kling/Veo ile video klipleri üret
4. DÜZENLEME — CapCut: montaj + altyazı + logo + müzik
5. YAYIN — Format, hashtag, zamanlama, A/B test
```

---

## Kling Prompt Kuralları (ÖNEMLİ)

- **40-50 kelime optimal** — daha uzun prompt modeli karıştırır
- **İNGİLİZCE yaz** — Türkçe prompt kaliteyi düşürür
- **5-7 element yeterli** — fazlası overload yaratır
- **Hareket yönünü belirt:** spesifik ol
- **Negatif prompt HER ZAMAN ekle:**
  ```
  blurry, low quality, distorted, deformed hands, extra fingers,
  morphing, glitch, watermark, text overlay, static, frozen
  ```
- **Öznel sıfat KULLANMA:** "beautiful" yerine görsel detay ver

---

## Image-to-Video (Ürün Fotoğrafından Video)

```
The [product] slowly rotates on a [surface], [lighting description],
[background element movement], smooth continuous motion, commercial quality
```

**Altın Kurallar:**
1. Sadece neyin hareket edeceğini yaz
2. Hareketin yönünü ve hızını belirt
3. Sahneyi tekrar tanımlama — görsel zaten bilgiyi içeriyor

---

## Reklam Video Yapısı

| Bölüm | Süre | İçerik |
|-------|------|--------|
| Hook | 0-3s | Dikkat çekici görsel/soru |
| Problem | 3-7s | Hedef kitlenin ağrı noktası |
| Solution | 7-12s | Ürünün çözümü göster |
| CTA | 12-15s | Net aksiyon çağrısı |

---

## Kalite Kontrol Checklist (Video Yayınlamadan Önce)

1. ☐ Artifact kontrolü (bozuk objeler) — KRİTİK
2. ☐ El/parmak anomalileri — KRİTİK
3. ☐ Ses-görüntü senkronizasyonu — KRİTİK
4. ☐ Renk tutarlılığı
5. ☐ Metin okunabilirliği (mobilde test)
6. ☐ Logo/branding doğru mu?
7. ☐ CTA görünür mü?
8. ☐ Platform formatı doğru mu? (9:16 veya 1:1)
9. ☐ Mobil önizleme yapıldı mı?

---

## Kepekçi Optik Workflow

```
1. Konu belirlenir (ör: "progresif cam")
2. Claude ile 7 katmanlı prompt yazılır
3. Kling'de video üretilir (ücretsiz 66 kredi/gün)
4. CapCut'ta montaj:
   - Logo watermark (Kepekçi Optik)
   - Türkçe altyazı
   - Marka renkleri (turkuaz #2EC4B6 + amber #F4A261)
   - Müzik + ses efektleri
5. Export: 9:16 (Reels) veya 1:1 (Post)
6. Instagram + Google İşletme Profili'ne paylaş
```
