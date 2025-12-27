"""
Erişim Kontrol Routes
Dış cihazlardan gelen (ESP32, AI Client) istekleri karşılar
"""
from flask import Blueprint, request, jsonify
from services.access_service import AccessService

# Blueprint tanımı
access_bp = Blueprint('access', __name__)

@access_bp.route('/check_access', methods=['GET'])
def check_access():
    """
    Erişim kontrol endpoint'i
    Parametre: ?card_id=<CARD_ID_OR_PLATE>
    """
    # 1. Parametre kontrolü
    card_id = request.args.get('card_id')
    
    if not card_id:
        return jsonify({
            "access": False,
            "message": "Hata: 'card_id' parametresi eksik!"
        }), 400

    # IP ve Cihaz bilgilerini al (loglama için)
    ip_address = request.remote_addr
    device_info = request.headers.get('User-Agent')

    # 2. Servis katmanını çağır
    try:
        result = AccessService.check_access(
            card_id_or_plate=card_id,
            ip_address=ip_address,
            device_info=device_info
        )
        
        # 3. Yanıt döndür
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "access": False,
            "message": f"Sunucu Hatası: {str(e)}"
        }), 500

@access_bp.route('/status', methods=['GET'])
def status():
    """Sistem durum kontrolü"""
    return jsonify({
        "status": "online",
        "service": "Arduino Backend API",
        "version": "1.0.0"
    }), 200
