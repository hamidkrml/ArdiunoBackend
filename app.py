"""
IoT Akıllı Otopark Sistemi - Ana Uygulama
Flask backend servisi ana giriş noktası
"""
from flask import Flask
from flask_cors import CORS

def create_app():
    """Flask uygulamasını oluşturur ve yapılandırır"""
    app = Flask(__name__)
    
    # CORS ayarları - ESP32'den gelen isteklere izin ver
    CORS(app)
    
    # Uygulama yapılandırması
    app.config['JSON_AS_ASCII'] = False  # Türkçe karakter desteği
    app.config['JSON_SORT_KEYS'] = False
    
    # Veritabanı tabloları oluştur (ilk çalıştırmada)
    with app.app_context():
        from database.schema import init_database
        init_database()
    
    # Blueprint'leri kaydet
    from routes.access import access_bp
    app.register_blueprint(access_bp)
    
    # Ana sayfa endpoint'i
    @app.route('/')
    def index():
        return {
            "message": "IoT Akıllı Otopark Sistemi API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "check_access": "/check_access?card_id=<CARD_ID>"
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("🚗 IoT Akıllı Otopark Sistemi Başlatılıyor...")
    print("=" * 50)
    print("📡 API Endpoint: http://127.0.0.1:5000")
    print("📋 Dokümantasyon: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
