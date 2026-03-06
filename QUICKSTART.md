# 🚀 Hızlı Başlangıç Rehberi

Bu rehber seni 5 dakikada hazır hale getirecek!

## 🆕 Son Güncellemeler (v2.0)

✅ **Daha uzun içerikler**: Artık 80-250 kelime arası (seviyeye göre)  
✅ **Görseller düzeltildi**: 3 farklı yöntemle görsel desteği  
✅ **Her çalıştırmada yeni makale**: Manuel test için timestamp bazlı ID  
✅ **Daha iyi hata kontrolü**: Kısa içerik otomatik tespiti  

---

## 📋 Adım Adım Kurulum

### 1️⃣ GitHub Repository Oluştur (1 dakika)

1. [github.com/new](https://github.com/new) adresine git
2. Repository name: `english-learning-rss` (veya istediğin isim)
3. ✅ **Public** seç (önemli!)
4. ✅ **Add a README file** seç
5. **Create repository** butonuna tıkla

### 2️⃣ Dosyaları Yükle (2 dakika)

1. Repository sayfasında **Add file** → **Upload files** butonuna tıkla
2. Bu 4 dosyayı sürükle-bırak:
   - `generate_rss.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
3. Ayrıca `.github/workflows/` klasörü oluştur:
   - **Add file** → **Create new file**
   - Dosya adı: `.github/workflows/daily-rss.yml`
   - `daily-rss.yml` dosyasının içeriğini yapıştır
4. **Commit changes** butonuna tıkla

### 3️⃣ Google API Key Al (1 dakika)

1. [ai.google.dev](https://ai.google.dev/) adresine git
2. **Get API key in Google AI Studio** butonuna tıkla
3. **Create API key** butonuna tıkla
4. API key'i kopyala (örn: `AIzaSyA...`)

### 4️⃣ GitHub'a API Key Ekle (30 saniye)

1. Repository'nde **⚙️ Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** butonuna tıkla
3. Name: `GEMINI_API_KEY`
4. Secret: Kopyaladığın API key'i yapıştır
5. **Add secret** butonuna tıkla

### 5️⃣ GitHub Pages Aktif Et (30 saniye)

1. **⚙️ Settings** → **Pages**
2. Source: **Deploy from a branch** seç
3. Branch: **main** ve **/ (root)** seç
4. **Save** butonuna tıkla

### 6️⃣ İlk Çalıştırma (30 saniye)

1. **Actions** sekmesine git
2. Sol tarafta **Daily English RSS Generator** seç
3. Sağ üstte **Run workflow** → **Run workflow** butonuna tıkla
4. Yeşil ✓ işareti çıkana kadar bekle (~30 saniye)

## 🎉 Tebrikler! Hazırsın!

### RSS Feed URL'in:
```
https://KULLANICI_ADIN.github.io/REPO_ADIN/feed.xml
```

**Örnek:** 
```
https://mehmet.github.io/english-learning-rss/feed.xml
```

### 📱 Feedly'ye Ekle

1. [feedly.com](https://feedly.com) → Giriş yap
2. Sol altta **+ Add Content**
3. Feed URL'ini yapıştır
4. **Follow** butonuna tıkla
5. Tamam! ✨

## ⏰ Çalışma Zamanı

- **Otomatik**: Her gün saat **12:00** (Türkiye saati)
- **Manuel**: Actions sekmesinden istediğin zaman çalıştırabilirsin

## 💡 İpuçları

### Farklı Saatte Çalışsın İstiyorsan

`.github/workflows/daily-rss.yml` dosyasını düzenle:

```yaml
schedule:
  - cron: '0 6 * * *'   # 09:00 Türkiye saati
  - cron: '0 15 * * *'  # 18:00 Türkiye saati
  - cron: '0 21 * * *'  # 00:00 Türkiye saati (gece yarısı)
```

### Test Etmek İçin

1. **Actions** sekmesi
2. **Run workflow** butonu
3. Anında çalışır!

## ❓ Sorun mu Var?

### "Workflow dosyası yok" hatası
→ `.github/workflows/daily-rss.yml` dosyasının doğru yerde olduğundan emin ol

### "API key geçersiz" hatası
→ Secrets kısmında `GEMINI_API_KEY` doğru girilmiş mi kontrol et

### "Feed boş görünüyor"
→ 5-10 dakika bekle (GitHub Pages yayınlama süresi)
→ URL'yi tarayıcıda aç, XML görüyorsan çalışıyor demektir

### Manuel çalıştır
→ Actions → Daily English RSS Generator → Run workflow

## 📞 Yardım

Takıldığın yer varsa:
1. README.md dosyasındaki detaylı açıklamalara bak
2. GitHub Issues'da soru sor

---

**Kolay gelsin! 🚀**
