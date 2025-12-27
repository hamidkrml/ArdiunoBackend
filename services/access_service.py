"""
Access Control Servisi
Otopark giriş yetkisini kontrol eder ve iş mantığını süzgeçten geçirir
"""
from models.user import UserModel
from services.log_service import LogService

class AccessService:
    @staticmethod
    def check_access(card_id_or_plate, ip_address=None, device_info=None):
        """
        Kart ID veya Plaka numarasına göre giriş yetkisi kontrolü yapar
        """
        # 1. Kullanıcıyı bul
        user = UserModel.get_by_card_id(card_id_or_plate)
        
        # 2. Yetki durumunu belirle
        access_granted = 1 if user else 0
        message = "Hoşgeldiniz" if access_granted else "Yetkisiz Erişim (Kayıt Bulunamadı)"
        user_id = user['id'] if user else None
        user_name = user['name'] if user else None

        # 3. Denemeyi logla
        LogService.record_access_attempt(
            card_id=card_id_or_plate,
            access_granted=access_granted,
            user_id=user_id,
            ip_address=ip_address,
            device_info=device_info,
            message=message
        )

        # 4. Yanıtı döndür
        return {
            "access": bool(access_granted),
            "message": message,
            "user_name": user_name
        }
