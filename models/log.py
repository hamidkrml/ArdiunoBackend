"""
Log Veri Modeli
Giriş-çıkış kayıtlarını ve yetkisiz erişim denemelerini yönetir
"""
from database.connection import get_db

class LogModel:
    @staticmethod
    def create(card_id, access_granted, user_id=None, ip_address=None, device_info=None, message=None):
        """Yeni bir erişim loğu oluşturur"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO logs (card_id, access_granted, user_id, ip_address, device_info, message) VALUES (?, ?, ?, ?, ?, ?)",
                (card_id, access_granted, user_id, ip_address, device_info, message)
            )
            return cursor.lastrowid

    @staticmethod
    def get_recent(limit=50):
        """Son kayıtları getirir"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT l.*, u.name as user_name FROM logs l LEFT JOIN users u ON l.user_id = u.id ORDER BY l.timestamp DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()

    @staticmethod
    def get_by_card_id(card_id, limit=20):
        """Belirli bir kartın geçmişini getirir"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM logs WHERE card_id = ? ORDER BY timestamp DESC LIMIT ?",
                (card_id, limit)
            )
            return cursor.fetchall()

    @staticmethod
    def delete(log_id):
        """Tek bir loğu siler"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
            return cursor.rowcount

    @staticmethod
    def delete_unauthorized():
        """Sadece yetkisiz erişim denemelerini siler"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM logs WHERE access_granted = 0")
            return cursor.rowcount

    @staticmethod
    def clear_all():
        """Tüm log geçmişini temizler"""
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM logs")
            return cursor.rowcount
