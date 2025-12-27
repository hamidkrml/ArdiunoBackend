"""
User Veri Modeli
Kullanıcı bilgilerini ve veritabanı CRUD operasyonlarını yönetir
"""
from database.connection import get_db

class UserModel:
    @staticmethod
    def get_by_card_id(card_id):
        """Kart ID'ye göre kullanıcı getirir"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE card_id = ? AND is_active = 1", (card_id,))
            return cursor.fetchone()

    @staticmethod
    def create(card_id, name, phone=None, email=None, vehicle_plate=None):
        """Yeni kullanıcı oluşturur"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (card_id, name, phone, email, vehicle_plate) VALUES (?, ?, ?, ?, ?)",
                (card_id, name, phone, email, vehicle_plate)
            )
            return cursor.lastrowid

    @staticmethod
    def get_all():
        """Tüm aktif kullanıcıları getirir"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE is_active = 1")
            return cursor.fetchall()

    @staticmethod
    def update(user_id, data):
        """Kullanıcı bilgilerini günceller"""
        keys = [f"{k} = ?" for k in data.keys()]
        query = f"UPDATE users SET {', '.join(keys)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        params = list(data.values()) + [user_id]
        
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(query, params)
            return cursor.rowcount

    @staticmethod
    def delete(user_id):
        """Kullanıcıyı pasife çeker (Soft delete)"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("UPDATE users SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
            return cursor.rowcount
