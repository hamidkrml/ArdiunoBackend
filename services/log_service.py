"""
Log Servisi
Erişim kayıtlarını yönetir ve modeller arası koordinasyonu sağlar
"""
from models.log import LogModel

class LogService:
    @staticmethod
    def record_access_attempt(card_id, access_granted, user_id=None, ip_address=None, device_info=None, message=None):
        """
        Bir erişim denemesini veritabanına kaydeder
        """
        try:
            log_id = LogModel.create(
                card_id=card_id,
                access_granted=access_granted,
                user_id=user_id,
                ip_address=ip_address,
                device_info=device_info,
                message=message
            )
            return log_id
        except Exception as e:
            # Gerçek bir uygulamada burada logger.error kullanılmalı
            print(f"Log kaydı sırasında hata oluştu: {str(e)}")
            return None

    @staticmethod
    def get_access_history(limit=50):
        """Son erişim geçmişini getirir"""
        return LogModel.get_recent(limit)
