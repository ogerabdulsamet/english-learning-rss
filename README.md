# 📚 Günlük İngilizce Öğrenme RSS Feed

Günlük otomatik İngilizce öğrenme içerikleri üreten, Google Gemini AI destekli RSS feed sistemi.

## ✨ Özellikler

- 🤖 **Google Gemini AI** ile günlük özgün içerik üretimi
- 📊 **6 Seviye**: A1, A2, B1, B2, C1, C2 (her gün farklı seviye)
- 🎯 **12 Farklı Konu**: Teknoloji, seyahat, sağlık, iş, vb.
- 🖼️ **Otomatik Fotoğraf**: Her içerik için Unsplash'tan ilgili görsel
- 🇹🇷 **Türkçe Çeviri**: Her paragrafın tam Türkçe çevirisi
- 💡 **Kelime Hazinesi**: Her içerikte 3-5 önemli kelime/kalıp ve açıklamaları
- 📱 **RSS Uyumlu**: Feedly, Inoreader gibi tüm RSS okuyucularla uyumlu
- ⚡ **GitHub Actions**: Tamamen ücretsiz, otomatik günlük güncelleme

## 🚀 Kurulum

### 1. GitHub Repository Oluştur

1. GitHub'da yeni bir repository oluştur (örn: `english-learning-rss`)
2. Public olarak ayarla (GitHub Pages için gerekli)

### 2. Dosyaları Yükle

Bu dosyaları repository'ne yükle:
```
.
├── .github/
│   └── workflows/
│       └── daily-rss.yml
├── generate_rss.py
├── requirements.txt
└── README.md
```

### 3. Google Gemini API Key Al

1. [Google AI Studio](https://makersuite.google.com/app/apikey)'ya git
2. "Create API Key" butonuna tıkla
3. API key'ini kopyala (ücretsiz!)

### 4. GitHub Secrets Ayarla

1. Repository'nde **Settings** → **Secrets and variables** → **Actions**'a git
2. **New repository secret** butonuna tıkla
3. Name: `GEMINI_API_KEY`
4. Value: Kopyaladığın API key'i yapıştır
5. **Add secret** butonuna tıkla

### 5. GitHub Pages'i Aktifleştir

1. Repository'nde **Settings** → **Pages**'e git
2. Source: **Deploy from a branch** seç
3. Branch: **main** (veya **master**) ve **/ (root)** seç
4. **Save** butonuna tıkla

### 6. İlk Çalıştırma

1. **Actions** sekmesine git
2. Sol menüden **Daily English RSS Generator** seç
3. Sağ üstteki **Run workflow** → **Run workflow** butonuna tıkla
4. İşlem tamamlanınca (yeşil ✓) RSS feed'in hazır!

## 📡 RSS Feed URL'in

Feed URL'in şu formatta olacak:
```
https://KULLANICI_ADIN.github.io/REPO_ADIN/feed.xml
```

Örnek:
```
https://ahmetdogan.github.io/english-learning-rss/feed.xml
```

## 📱 RSS Okuyucuya Ekleme

### Feedly
1. [Feedly](https://feedly.com/)'ye git
2. Sol altta **+ Add Content** butonuna tıkla
3. Feed URL'ini yapıştır
4. **Follow** butonuna tıkla

### Inoreader
1. [Inoreader](https://www.inoreader.com/)'a git
2. **Add subscription** (sol menüde)
3. Feed URL'ini gir
4. **Subscribe** butonuna tıkla

### Diğer RSS Okuyucular
- **NewsBlur**: + Add → Feed URL
- **The Old Reader**: Subscribe → Feed URL
- **RSS Guard**, **NetNewsWire**: Add Feed → URL gir

## ⚙️ Özelleştirme

### Çalışma Saatini Değiştirme

`.github/workflows/daily-rss.yml` dosyasında:
```yaml
schedule:
  - cron: '0 9 * * *'  # Bu satırı değiştir
```

Cron formatı: `dakika saat * * *` (UTC saat dilimi)
- `0 6 * * *` = Her gün 06:00 UTC (09:00 Türkiye)
- `0 12 * * *` = Her gün 12:00 UTC (15:00 Türkiye)
- `0 18 * * *` = Her gün 18:00 UTC (21:00 Türkiye)

### Konuları Değiştirme

`generate_rss.py` dosyasında `TOPICS` listesini düzenle:
```python
TOPICS = [
    "Technology and Innovation",
    "Travel and Culture",
    # Yeni konular ekle...
]
```

### Feed Başlık/Açıklama

`generate_rss.py` dosyasında:
```python
FEED_TITLE = 'Daily English Learning Feed'  # Burası değiştir
FEED_DESCRIPTION = 'Günlük İngilizce öğrenme içerikleri'  # Burası değiştir
```

## 🔍 Nasıl Çalışır?

1. **Her gün saat 09:00 UTC'de** (12:00 Türkiye saati) GitHub Actions otomatik çalışır
2. **Günün seviyesi** belirlenir (haftanın gününe göre döngüsel: Pazartesi A1, Salı A2, vb.)
3. **Günün konusu** belirlenir (yılın gününe göre döngüsel)
4. **Google Gemini AI** ile özgün içerik üretilir:
   - İngilizce paragraf (100-150 kelime)
   - Türkçe çeviri
   - Önemli kelimeler ve kalıplar
5. **Unsplash'tan** konuya uygun fotoğraf eklenir
6. **RSS feed dosyası** (`feed.xml`) güncellenir
7. **GitHub Pages** üzerinden yayınlanır
8. **RSS okuyucun** otomatik güncelleme alır!

## 📊 İçerik Seviyeleri

| Seviye | Gün | Açıklama |
|--------|-----|----------|
| A1 | Pazartesi | Başlangıç - Temel kelimeler ve basit cümleler |
| A2 | Salı | Temel - Günlük konular ve sık kullanılan ifadeler |
| B1 | Çarşamba | Orta Öncesi - Daha karmaşık cümleler |
| B2 | Perşembe | Orta - Detaylı açıklamalar |
| C1 | Cuma | İleri - Nüanslı ve akıcı dil |
| C2 | Cumartesi | Yetkin - Native seviyesine yakın |

## 🛠️ Sorun Giderme

### Feed güncellenmiyor
1. **Actions** sekmesine git
2. Son workflow'un durumunu kontrol et
3. Kırmızı X varsa, detaylara tıkla ve hatayı oku
4. Genellikle API key sorunu olur → Secrets'ı kontrol et

### Feed boş görünüyor
1. İlk çalıştırmadan sonra 5-10 dakika bekle (GitHub Pages yayınlama süresi)
2. Feed URL'ini tarayıcıda aç, XML görünüyorsa çalışıyor demektir

### Manuel çalıştırma
1. **Actions** → **Daily English RSS Generator**
2. **Run workflow** → **Run workflow** butonuna tıkla

## 💰 Maliyet

Tamamen **ÜCRETSIZ**! 🎉

- ✅ GitHub Actions: 2,000 dakika/ay (bu proje ~1 dakika/gün kullanır)
- ✅ Google Gemini API: Günde 60 istek ücretsiz (bu proje 1 istek/gün kullanır)
- ✅ GitHub Pages: Sınırsız ücretsiz hosting
- ✅ Unsplash: Ücretsiz fotoğraflar

## 📝 Örnek İçerik

```
[B1] Technology Shapes Our Future

📖 English Text:
Technology has transformed how we communicate, work, and learn. 
Smartphones connect us instantly to people worldwide. Artificial 
intelligence helps doctors diagnose diseases more accurately. These 
innovations make our lives more convenient, but we must use them 
wisely and responsibly.

🇹🇷 Türkçe Çeviri:
Teknoloji, iletişim kurma, çalışma ve öğrenme şeklimizi değiştirdi...

💡 Key Vocabulary & Phrases:
- transform: değiştirmek, dönüştürmek
  Example: Digital tools transform education.
...
```

## 🎯 Kullanım İpuçları

1. **Düzenli Okuma**: Her gün aynı saatte RSS okuyucunu kontrol et
2. **Aktif Öğrenme**: Kelimeleri not defterine yaz
3. **Tekrar**: Eski içerikleri periyodik olarak gözden geçir
4. **Yüksek Sesle Okuma**: İngilizce paragrafı yüksek sesle oku (telaffuz pratiği)

## 🤝 Katkıda Bulunma

İyileştirme önerilerin varsa:
1. Issue aç
2. Pull request gönder
3. Yıldız ver ⭐

## 📄 Lisans

MIT License - İstediğin gibi kullan, değiştir, paylaş!

## 📧 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

**Keyifli öğrenmeler! 🚀📚**
