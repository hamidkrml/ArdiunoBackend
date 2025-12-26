"""
Veritabanı Şema Yönetimi
Tabloları otomatik oluşturur ve yönetir
"""
from database.connection import get_db
import os


def init_database():
    """
    Veritabanını başlatır ve gerekli tabloları oluşturur
    İlk çalıştırmada otomatik olarak çağrılır
    """
    with get_db() as db:
        # Users tablosu - Kayıtlı kullanıcılar ve kart ID'leri
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                vehicle_plate TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Logs tablosu - Erişim kayıtları
        db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id TEXT NOT NULL,
                access_granted INTEGER NOT NULL,
                user_id INTEGER,
                ip_address TEXT,
                device_info TEXT,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # İndeksler - Performans için
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_card_id 
            ON users(card_id)
        """)
        
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_timestamp 
            ON logs(timestamp)
        """)
        
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_card_id 
            ON logs(card_id)
        """)
        
        db.commit()
        
        print("✅ Veritabanı tabloları başarıyla oluşturuldu/kontrol edildi")


def reset_database():
    """
    Veritabanını sıfırlar - UYARI: Tüm verileri siler!
    Test ve geliştirme amaçlı kullanılmalıdır
    """
    with get_db() as db:
        db.execute("DROP TABLE IF EXISTS logs")
        db.execute("DROP TABLE IF EXISTS users")
        db.commit()
        print("⚠️  Veritabanı sıfırlandı")
    
    # Tabloları yeniden oluştur
    init_database()


def get_table_info():
    """
    Veritabanı tablo bilgilerini döndürür
    
    Returns:
        dict: Tablo isimleri ve satır sayıları
    """
    with get_db() as db:
        cursor = db.cursor()
        
        # Users tablosundaki kayıt sayısı
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users_count = cursor.fetchone()['count']
        
        # Logs tablosundaki kayıt sayısı
        cursor.execute("SELECT COUNT(*) as count FROM logs")
        logs_count = cursor.fetchone()['count']
        
        return {
            "users": users_count,
            "logs": logs_count
        }
