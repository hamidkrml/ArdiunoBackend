# 🚀 IoT Akıllı Otopark Sistemi - Hızlı Başlangıç

## 📋 Adım Adım Kurulum

### 1. GitHub Issues Oluşturma

```bash
# GitHub CLI yüklü mü kontrol edin
gh --version

# Eğer yüklü değilse (macOS):
brew install gh

# GitHub'a login olun
gh auth login

# Tüm Issue'ları otomatik oluştur
./create_issues.sh
```

### 2. İlk Commit ve Push

```bash
# Tüm dosyaları ekle
git add .

# Commit yap
git commit -m "feat: Issue #1 ve #2 tamamlandı - Temel altyapı ve veritabanı"

# Remote ekle (eğer eklenmemişse)
git remote add origin git@github.com:hamidkrml/ArdiunoBackend.git

# Main branch'e çevir
git branch -M main

# Push et
git push -u origin main
```

### 3. Python Virtual Environment Kurulumu

```bash
# Virtual environment oluştur
python3 -m venv venv

# Aktif et
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate     # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 4. Uygulamayı Çalıştır

```bash
# Flask uygulamasını başlat
python app.py
```

Tarayıcıda açın: http://127.0.0.1:5000

---

## 🔄 Her Issue İçin Workflow

### Issue #3 - Model Katmanı

```bash
# Kodları yaz: models/user.py, models/log.py
# Test et
# Commit yap
git add models/
git commit -m "feat: Issue #3 tamamlandı - Model katmanı oluşturuldu

closes #3"
git push
```

### Issue #4 - Servis Katmanı

```bash
# Kodları yaz: services/access_service.py, services/log_service.py
# Test et
# Commit yap
git add services/
git commit -m "feat: Issue #4 tamamlandı - Servis katmanı oluşturuldu

closes #4"
git push
```

### Issue #5 - API Endpoints

```bash
# Kodları yaz: routes/access.py
# Test et
# Commit yap
git add routes/
git commit -m "feat: Issue #5 tamamlandı - API endpoints hazır

closes #5"
git push
```

### Issue #6 - Test ve Dummy Data

```bash
# Kodları yaz: scripts/seed_data.py
# Test et
python -m scripts.seed_data
curl "http://localhost:5000/check_access?card_id=ABC123"

# Commit yap
git add scripts/
git commit -m "feat: Issue #6 tamamlandı - Test verileri ve testler hazır

closes #6"
git push
```

### Issue #7 - Dokümantasyon

```bash
# Dokümantasyon yaz: README.md, API_DOCUMENTATION.md
# Commit yap
git add README.md API_DOCUMENTATION.md
git commit -m "docs: Issue #7 tamamlandı - Dokümantasyon hazır

closes #7"
git push
```

### Issue #8 - Production Ready

```bash
# Production dosyalarını ekle: .env.example, config.py, utils/
# Commit yap
git add .
git commit -m "feat: Issue #8 tamamlandı - Production ready

closes #8"
git push
```

---

## 📊 Proje Durumu

- ✅ Issue #1: Temel Altyapı
- ✅ Issue #2: Veritabanı Katmanı
- ⏳ Issue #3: Model Katmanı
- ⏳ Issue #4: Servis Katmanı
- ⏳ Issue #5: API Endpoints
- ⏳ Issue #6: Test ve Dummy Data
- ⏳ Issue #7: Dokümantasyon
- ⏳ Issue #8: Production Ready

---

## 🛠️ Yararlı Komutlar

```bash
# Veritabanını sıfırla
python -c "from database.schema import reset_database; reset_database()"

# Dummy data ekle
python -m scripts.seed_data

# API test et
curl "http://localhost:5000/check_access?card_id=ABC123"

# Tüm issue'ları listele
gh issue list

# Belirli bir issue'yu kapat
gh issue close 3
```

---

## 📞 Yardım

Herhangi bir sorunla karşılaşırsanız:
1. `git status` ile durumu kontrol edin
2. `python app.py` ile uygulamayı çalıştırın
3. Hata loglarını kontrol edin
