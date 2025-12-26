#!/bin/bash

# IoT Akıllı Otopark Sistemi - GitHub Issues Oluşturma Script'i
# Bu script Issue #3'ten #8'e kadar tüm issue'ları otomatik oluşturur

echo "🚀 GitHub Issues oluşturuluyor..."
echo "================================"

# Issue #3: Model Katmanı
echo "📝 Issue #3 oluşturuluyor..."
gh issue create \
  --title "Issue #3: Model Katmanı" \
  --body "**Hedef:** Veri modelleri ve CRUD operasyonlarını oluştur

**Görevler:**
- [ ] models/user.py - User modeli ve CRUD işlemleri
- [ ] models/log.py - Log modeli ve CRUD işlemleri

**Dosyalar:**
- \`models/user.py\`
- \`models/log.py\`

**Bağımlılıklar:**
- Issue #2 (Veritabanı Katmanı) tamamlanmış olmalı" \
  --label "feature" \
  --label "backend"

echo "✅ Issue #3 oluşturuldu"
echo ""

# Issue #4: Servis Katmanı
echo "📝 Issue #4 oluşturuluyor..."
gh issue create \
  --title "Issue #4: Servis Katmanı (İş Mantığı)" \
  --body "**Hedef:** İş mantığı servislerini oluştur

**Görevler:**
- [ ] services/access_service.py - Kart ID kontrolü ve erişim izni mantığı
- [ ] services/log_service.py - Log kayıt işlemleri

**Dosyalar:**
- \`services/access_service.py\`
- \`services/log_service.py\`

**Bağımlılıklar:**
- Issue #3 (Model Katmanı) tamamlanmış olmalı" \
  --label "feature" \
  --label "backend"

echo "✅ Issue #4 oluşturuldu"
echo ""

# Issue #5: API Endpoints
echo "📝 Issue #5 oluşturuluyor..."
gh issue create \
  --title "Issue #5: API Endpoints (Routes)" \
  --body "**Hedef:** ESP32 için /check_access endpoint'i oluştur

**Görevler:**
- [ ] routes/access.py - /check_access endpoint
- [ ] GET request ile card_id parametresi
- [ ] JSON response dönme
- [ ] Error handling

**Endpoint:**
- \`GET /check_access?card_id=<CARD_ID>\`

**Response Formatı:**
\`\`\`json
{
  \"access\": true,
  \"message\": \"Hoşgeldiniz\",
  \"user_name\": \"Ahmet Yılmaz\"
}
\`\`\`

**Dosyalar:**
- \`routes/access.py\`

**Bağımlılıklar:**
- Issue #4 (Servis Katmanı) tamamlanmış olmalı" \
  --label "feature" \
  --label "api"

echo "✅ Issue #5 oluşturuldu"
echo ""

# Issue #6: Test ve Dummy Data
echo "📝 Issue #6 oluşturuluyor..."
gh issue create \
  --title "Issue #6: Test ve Dummy Data" \
  --body "**Hedef:** Veritabanına test verileri ekle ve API'yi test et

**Görevler:**
- [ ] scripts/seed_data.py - Dummy kullanıcılar ekleyen script
- [ ] En az 3 örnek kullanıcı ekle
- [ ] API endpoint'lerini test et
- [ ] Postman collection hazırla (opsiyonel)

**Test Kullanıcıları:**
1. Kart ID: ABC123 - Ahmet Yılmaz
2. Kart ID: XYZ789 - Ayşe Demir
3. Kart ID: DEF456 - Mehmet Kaya

**Dosyalar:**
- \`scripts/seed_data.py\`

**Test Komutları:**
\`\`\`bash
python -m scripts.seed_data
curl \"http://localhost:5000/check_access?card_id=ABC123\"
\`\`\`

**Bağımlılıklar:**
- Issue #5 (API Endpoints) tamamlanmış olmalı" \
  --label "testing" \
  --label "scripts"

echo "✅ Issue #6 oluşturuldu"
echo ""

# Issue #7: Dokümantasyon
echo "📝 Issue #7 oluşturuluyor..."
gh issue create \
  --title "Issue #7: Dokümantasyon" \
  --body "**Hedef:** Profesyonel README ve API dokümantasyonu hazırla

**Görevler:**
- [ ] README.md - Proje tanıtımı, kurulum, kullanım
- [ ] API_DOCUMENTATION.md - Detaylı API dokümantasyonu
- [ ] ESP32 entegrasyonu örnekleri
- [ ] Ekran görüntüleri (Postman testleri)

**README İçeriği:**
- Proje açıklaması
- Özellikler
- Kurulum adımları
- Kullanım örnekleri
- API referansı
- ESP32 Arduino kodu örneği
- Katkıda bulunma rehberi

**Dosyalar:**
- \`README.md\`
- \`API_DOCUMENTATION.md\`

**Bağımlılıklar:**
- Issue #6 (Test) tamamlanmış olmalı" \
  --label "documentation"

echo "✅ Issue #7 oluşturuldu"
echo ""

# Issue #8: Production Ready
echo "📝 Issue #8 oluşturuluyor..."
gh issue create \
  --title "Issue #8: Production Ready & İyileştirmeler" \
  --body "**Hedef:** Projeyi production için hazırla ve iyileştirmeler yap

**Görevler:**
- [ ] Environment variables (.env dosyası)
- [ ] Config dosyası (config.py)
- [ ] Error handling iyileştirmeleri
- [ ] Logging sistemi
- [ ] Input validation
- [ ] Rate limiting (opsiyonel)
- [ ] CORS konfigürasyonu
- [ ] Database connection pooling

**Dosyalar:**
- \`.env.example\`
- \`config.py\`
- \`utils/logger.py\`
- \`utils/validators.py\`

**Güvenlik:**
- SQL injection koruması (parametreli sorgular)
- XSS koruması
- Rate limiting

**Bağımlılıklar:**
- Issue #7 (Dokümantasyon) tamamlanmış olmalı" \
  --label "enhancement" \
  --label "security"

echo "✅ Issue #8 oluşturuldu"
echo ""

echo "================================"
echo "🎉 Tüm Issue'lar başarıyla oluşturuldu!"
echo ""
echo "📋 Oluşturulan Issue'lar:"
echo "  - Issue #3: Model Katmanı"
echo "  - Issue #4: Servis Katmanı"
echo "  - Issue #5: API Endpoints"
echo "  - Issue #6: Test ve Dummy Data"
echo "  - Issue #7: Dokümantasyon"
echo "  - Issue #8: Production Ready"
echo ""
echo "✨ GitHub'da kontrol edebilirsiniz!"
