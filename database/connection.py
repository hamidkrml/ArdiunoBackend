"""
SQLite Veritabanı Bağlantı Yöneticisi
Context manager ile güvenli veritabanı bağlantısı sağlar
"""
import sqlite3
from contextlib import contextmanager
import os

# Veritabanı dosya yolu
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'parking.db')


def get_connection():
    """
    SQLite veritabanı bağlantısı oluşturur
    
    Returns:
        sqlite3.Connection: Veritabanı bağlantısı
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Row nesnesi olarak sonuç döner (dict gibi)
    return conn


@contextmanager
def get_db():
    """
    Context manager ile veritabanı bağlantısı yönetimi
    
    Kullanım:
        with get_db() as db:
            db.execute("SELECT * FROM users")
    
    Yields:
        sqlite3.Connection: Veritabanı bağlantısı
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()  # Başarılı işlemleri commit et
    except Exception as e:
        conn.rollback()  # Hata durumunda rollback yap
        raise e
    finally:
        conn.close()  # Her durumda bağlantıyı kapat


def execute_query(query, params=None):
    """
    Tek seferlik sorgu çalıştırır
    
    Args:
        query (str): SQL sorgusu
        params (tuple, optional): Sorgu parametreleri
    
    Returns:
        list: Sorgu sonuçları (SELECT için)
        int: Etkilenen satır sayısı (INSERT, UPDATE, DELETE için)
    """
    with get_db() as db:
        cursor = db.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # SELECT sorguları için sonuçları döndür
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        
        # INSERT, UPDATE, DELETE için etkilenen satır sayısını döndür
        return cursor.rowcount
