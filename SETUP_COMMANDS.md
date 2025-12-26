# Git ve GitHub Issue Setup Komutları

## 1️⃣ İlk Commit ve Push

```bash
# Tüm dosyaları stage'e al
git add .

# İlk commit
git commit -m "feat: Issue #1 ve #2 tamamlandı - Temel altyapı ve veritabanı katmanı

- Proje klasör yapısı oluşturuldu (modüler mimari)
- requirements.txt, .gitignore, app.py hazırlandı
- SQLite veritabanı bağlantı yöneticisi (connection.py)
- Otomatik tablo oluşturma (schema.py - users, logs)
- Tüm modül klasörleri ve __init__.py dosyaları eklendi"

# Remote repository ekle
git remote add origin git@github.com:hamidkrml/ArdiunoBackend.git

# Branch adını main yap
git branch -M main

# GitHub'a push et
git push -u origin main
```

---

## 2️⃣ GitHub Issues Oluşturma (GitHub CLI ile)

### Önce GitHub CLI yükleyin (eğer yoksa):

```bash
# macOS için
brew install gh

# GitHub CLI ile login olun
gh auth login
```

### Ardından Issue'ları otomatik oluşturun:

```bash
# Issue #3
gh issue create \
  --title "Issue #3: Model Katmanı" \
  --body "**Hedef:** Veri modelleri ve CRUD operasyonlarını oluştur

**Görevler:**
- [ ] models/user.py - User modeli ve CRUD işlemleri
- [ ] models/log.py - Log modeli ve CRUD işlemleri

**Dosyalar:**
- \`models/user.py\`
- \`models/log.py\`" \
  --label "feature"

# Issue #4
gh issue create \
  --title "Issue #4: Servis Katmanı (İş Mantığı)" \
  --body "**Hedef:** İş mantığı servislerini oluştur

**Görevler:**
- [ ] services/access_service.py - Kart ID kontrolü ve erişim izni mantığı
- [ ] services/log_service.py - Log kayıt işlemleri

**Dosyalar:**
- \`services/access_service.py\`
- \`services/log_service.py\`" \
  --label "feature"

# Issue #5
gh issue create \
  --title "Issue #5: API Endpoints (Routes)" \
  --body "**Hedef:** ESP32 için /check_access endpoint'i oluştur

**Görevler:**
- [ ] routes/access.py - /check_access endpoint
- [ ] GET request ile card_id parametresi
- [ ] JSON response dönme

**Endpoint:**
- \`GET /check_access?card_id=<CARD_ID>\`

**Response Formatı:**
\`\`\`json
{
  \"access\": true/false,
  \"message\": \"Hoşgeldiniz\" / \"Yetkisiz Erişim\",
  \"user_name\": \"Ahmet Yılmaz\"
}
\`\`\`

**Dosyalar:**
- \`routes/access.py\`" \
  --label "feature"

# Issue #6
gh issue create \
  --title "Issue #6: Test ve Dummy Data" \
  --body "**Hedef:** Veritabanına test verileri ekle ve API'yi test et

**Görevler:**
- [ ] scripts/seed_data.py - Dummy kullanıcılar ekleyen script
- [ ] En az 3 örnek kullanıcı ekle
- [ ] API endpoint'lerini test et

**Dosyalar:**
- \`scripts/seed_data.py\`

**Test Komutu:**
\`\`\`bash
python -m scripts.seed_data
curl \"http://localhost:5000/check_access?card_id=ABC123\"
\`\`\`" \
  --label "testing"

# Issue #7
gh issue create \
  --title "Issue #7: Dokümantasyon" \
  --body "**Hedef:** Profesyonel README ve API dokümantasyonu hazırla

**Görevler:**
- [ ] README.md - Proje tanıtımı, kurulum, kullanım
- [ ] API_DOCUMENTATION.md - Detaylı API dokümantasyonu
- [ ] ESP32 entegrasyonu örnekleri

**Dosyalar:**
- \`README.md\`
- \`API_DOCUMENTATION.md\`" \
  --label "documentation"

# Issue #8
gh issue create \
  --title "Issue #8: Production Ready" \
  --body "**Hedef:** Projeyi production için hazırla

**Görevler:**
- [ ] Environment variables (.env dosyası)
- [ ] Config dosyası (config.py)
- [ ] Error handling iyileştirmeleri
- [ ] Logging sistemi
- [ ] Rate limiting (opsiyonel)

**Dosyalar:**
- \`.env.example\`
- \`config.py\`" \
  --label "enhancement"
```

---

## 3️⃣ Issue Kapatma (Her Issue tamamlandığında)

```bash
# Commit yaparken issue numarasını ekleyin
git commit -m "feat: Issue #3 tamamlandı - Model katmanı oluşturuldu

closes #3"

# Push yapınca otomatik kapanır
git push
```

---

## 4️⃣ Alternatif: Manuel GitHub Web UI

Eğer GitHub CLI kullanmak istemezseniz:

1. GitHub repository'nize gidin
2. "Issues" tab'ına tıklayın
3. "New Issue" butonuna basın
4. Yukarıdaki bilgileri kopyala-yapıştır yapın

---

## 📌 Notlar

- ✅ **Issue #1** ve **#2** zaten tamamlandı (kodları yazdık)
- ⏳ **Issue #3-8** bekliyor
- 🔄 Her Issue için ayrı commit yapacağız
- 🎯 Commit mesajında `closes #N` yazarsanız otomatik kapanır
