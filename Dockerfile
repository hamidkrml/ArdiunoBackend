# Python imajını kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını kur (SQLite vb. gerekirse)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Portu aç
EXPOSE 5000

# Uygulamayı başlat
# Önce seed data çalıştırıp sonra app.py'yi başlatıyoruz
CMD ["sh", "-c", "python3 scripts/seed_data.py && python3 app.py"]
