# 🧹 Kapsamlı Sistem Temizleyici

Bilgisayarınızdaki **tüm uygulama verilerini, logları, cache'leri ve geçmişi** temizleyen kapsamlı bir temizlik aracı. Oyunlar, tarayıcılar, uygulamalar - her şeyi temizler ve yeni bir kullanıcı gibi başlamanızı sağlar.

## ✨ Özellikler

### 🌐 Tarayıcı Temizliği
- **Chrome**: Cache, cookies, geçmiş, sekmeler, IndexedDB, Local Storage
- **Microsoft Edge**: Cache, cookies, geçmiş
- **Brave**: Cache, geçmiş
- Tüm tarayıcı verileri temizlenir

### 🎮 Oyun Temizliği
- **Steam**: HTML cache, logs, app cache
- **Epic Games**: Logs, config dosyaları
- **Ubisoft**: Logs, cache
- **Riot Games**: Tüm veriler
- **GOG Galaxy**: Logs, cache
- Oyun kayıtları ve logları temizlenir

### 📱 Uygulama Temizliği
- **Discord**: Cache, logs, GPU cache
- **Spotify**: Storage, data
- **VS Code**: Cache, logs
- **Slack**: Cache, logs
- **Zoom**: Logs
- Tüm uygulama cache'leri ve logları

### 💻 Sistem Temizliği
- Windows Temp dosyaları
- Kullanıcı Temp dosyaları
- Recent Files (Son açılan dosyalar)
- Windows Prefetch
- Tüm log dosyaları (.log, .txt, .out, .err, vb.)

## 🚀 Kullanım

### Temel Kullanım

```bash
python log_cleaner.py
```

Bu komut tüm sistem temizliğini başlatır. **ÖNEMLİ**: Silmeden önce onay ister.

### Önce Görmek İstiyorsanız

```bash
python log_cleaner.py --dry-run
```

Bu modda sadece ne silineceği gösterilir, hiçbir şey silinmez. Önce bunu çalıştırmanız önerilir!

### Yardım

```bash
python log_cleaner.py --help
```

## ⚠️ ÖNEMLİ UYARILAR

1. **GERİ ALINAMAZ**: Bu işlem geri alınamaz! Önemli verilerinizi mutlaka yedekleyin.

2. **Temizlenen Veriler**:
   - ✅ Tarayıcı geçmişi, cookies, cache
   - ✅ Oyun kayıtları ve logları
   - ✅ Uygulama cache'leri
   - ✅ Temp dosyalar
   - ✅ Recent files
   - ✅ Tüm log dosyaları

3. **Korunan Veriler**:
   - ✅ Windows sistem dosyaları
   - ✅ Program Files altındaki kritik dosyalar
   - ✅ Sistem32, SysWOW64 gibi korumalı dizinler

4. **Öneri**: İlk kullanımda mutlaka `--dry-run` parametresi ile çalıştırın ve ne silineceğini görün.

## 📋 Temizlenen Kategoriler

### Tarayıcılar
- Chrome cache, cookies, history, sekmeler
- Edge cache, cookies, history
- Brave cache, history
- Tüm tarayıcı verileri

### Oyunlar
- Steam logs ve cache
- Epic Games logs
- Ubisoft logs ve cache
- Riot Games verileri
- GOG Galaxy logs ve cache

### Uygulamalar
- Discord cache ve logs
- Spotify storage
- VS Code cache ve logs
- Slack cache ve logs
- Zoom logs

### Sistem
- Windows Temp
- User Temp
- Recent Files
- Prefetch
- Tüm log dosyaları

## 🔒 Güvenlik

- Sistem kritik dosyaları korunur
- Silmeden önce onay ister
- Dry-run modu ile önizleme yapabilirsiniz
- Hata durumlarını raporlar

## 📊 Çıktı Örneği

```
🧹 Kapsamlı Sistem Temizliği Başlatılıyor...
======================================================================
📂 🌐 Tarayıcı Verileri (Chrome/Edge/Brave)
======================================================================
📁 Chrome Cache: 2.45 GB
   ✅ Silindi: 2.45 GB
📁 Chrome History: 15.23 MB
   ✅ Silindi: 15.23 MB
...

✨ TEMİZLİK TAMAMLANDI
======================================================================
📊 Toplam Silinen: 45 öğe
💾 Toplam Temizlenen Alan: 5.23 GB
```

## 🛠️ Gereksinimler

- Python 3.6 veya üzeri
- Windows 10/11 (diğer sistemler için kısıtlı destek)
- Yönetici yetkileri (bazı dosyalar için gerekli olabilir)

## 💡 İpuçları

1. **İlk Kullanım**: Mutlaka `--dry-run` ile başlayın
2. **Yedekleme**: Önemli verilerinizi yedekleyin
3. **Tarayıcı**: Şifreleriniz kaybolabilir, şifre yöneticisi kullanın
4. **Oyunlar**: Oyun kayıtlarınız silinebilir, cloud save kullanın

## 📝 Notlar

- Bazı dosyalar kullanımda olduğu için silinemeyebilir (normal)
- Yönetici yetkileri ile çalıştırmak daha fazla dosya temizlemenize olanak sağlar
- İşlem uzun sürebilir (özellikle büyük cache'ler varsa)

## ⚡ Hızlı Başlangıç

```bash
# 1. Önce ne silineceğini görün
python log_cleaner.py --dry-run

# 2. Onayladıktan sonra gerçek temizliği yapın
python log_cleaner.py
```

---

**⚠️ DİKKAT**: Bu araç güçlü bir temizlik aracıdır. Kullanmadan önce mutlaka önemli verilerinizi yedekleyin!
