# 🚗 IoT Akıllı Otopark Sistemi - Kurulum Rehberi

Bu proje iki ana parçadan oluşur: **Backend (Beyin)** ve **AI Client (Göz)**.

---

## 🏗️ 1. Adım: Backend (Docker) - BEYİN
Backend, veritabanını ve yetki kontrolünü yönetir. Docker üzerinden saniyeler içinde kurulur.

**Gereksinim:** Bilgisayarında [Docker Desktop](https://www.docker.com/products/docker-desktop/) kurulu olmalıdır.

1.  Terminali aç ve proje klasörüne gir.
2.  Şu komutu çalıştır:
    ```bash
    docker-compose up -d
    ```
3.  **Bitti!** Artık backend `http://localhost:5005` adresinde çalışıyor.

---

## 📸 2. Adım: AI Client (Python) - GÖZ
Bu parça kameradan plakayı okur ve Docker'daki beyne sorar.

**Gereksinim:** Bilgisayarında Python 3.9+ kurulu olmalıdır.

1.  Terminalde `client` klasörüne gir: `cd client`
2.  Sanal ortam oluştur ve aktif et:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Gerekli kütüphaneleri kur:
    ```bash
    pip install -r requirements_client.txt
    ```
4.  Sistemi başlat:
    ```bash
    python3 plate_reader.py
    ```

---

## ⚙️ 3. Adım: ESP32 Kamerayı Bağlamak
Eğer gerçek bir ESP32-CAM kullanacaksan:

1.  `client/plate_reader.py` dosyasını aç.
2.  `STREAM_URL = 0` olan satırı bul.
3.  Onu şu şekilde değiştir: `STREAM_URL = "http://SENIN_ESP_IP_ADRESIN:81/stream"`

---

## 🎯 Kullanım İpuçları
*   **Mavi Kutu:** Plakayı (veya kağıdı) ekrandaki mavi kutunun içine göster.
*   **Doğrulama:** Sistem, aynı plakayı en az 3 kez kararlı şekilde okuyana kadar işlem yapmaz (hata payını sıfırlamak için).
*   **Çıkış:** Durdurmak için `q` tuşuna basabilirsin.

---
*Hazırlayan: Antigravity AI* 🚀
