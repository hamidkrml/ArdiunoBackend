"""
Seed Data Script
Veritabanına test amaçlı örnek kullanıcılar ekler
"""
import sys
import os

# Proje kök dizinini Python path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import UserModel
from database.schema import init_database

def seed_data():
    print("🧹 Veritabanı kontrol ediliyor...")
    init_database()
    
    print("🌱 Örnek kullanıcılar ekleniyor...")
    
    # Test verileri
    dummy_users = [
        {
            "card_id": "ABC123",
            "name": "Ahmet Yılmaz",
            "phone": "5551234567",
            "email": "ahmet@gmail.com",
            "vehicle_plate": "34ABC123"
        },
        {
            "card_id": "XYZ789",
            "name": "Ayşe Demir",
            "phone": "5559876543",
            "email": "ayse@gmail.com",
            "vehicle_plate": "06XYZ789"
        },
        {
            "card_id": "34ABC123", # Plaka ile giriş testi için
            "name": "Plaka Test Kullanıcısı",
            "phone": "5550000000",
            "email": "test@test.com",
            "vehicle_plate": "34ABC123"
        }
    ]
    
    for user in dummy_users:
        try:
            # Önce var mı diye bak (tekrar eklememek için)
            existing = UserModel.get_by_card_id(user['card_id'])
            if not existing:
                user_id = UserModel.create(**user)
                print(f"✅ Eklendi: {user['name']} (ID: {user_id})")
            else:
                print(f"⏩ Zaten mevcut: {user['name']}")
        except Exception as e:
            print(f"❌ Hata: {user['name']} eklenemedi. {str(e)}")

    print("\n✨ Seed işlemi tamamlandı!")
    print("Sistemi test etmek için 'python app.py' yazarak sunucuyu başlatabilirsiniz.")

if __name__ == "__main__":
    seed_data()
