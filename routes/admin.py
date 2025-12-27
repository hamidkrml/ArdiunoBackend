from flask import Blueprint, jsonify
from models.user import UserModel
from models.log import LogModel
from database.connection import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    """Genel otopark istatistiklerini döner"""
    try:
        users = UserModel.get_all()
        logs = LogModel.get_recent(limit=100)
        
        # Basit istatistikler
        total_users = len(users)
        total_logs = len(logs)
        granted_access = len([log for log in logs if log['access_granted'] == 1])
        denied_access = total_logs - granted_access
        
        return jsonify({
            "total_users": total_users,
            "total_logs": total_logs,
            "today_granted": granted_access,
            "today_denied": denied_access
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
def get_users():
    """Kayıtlı kullanıcı listesini döner"""
    try:
        users = UserModel.get_all()
        # Row nesnelerini dict'e çevir
        user_list = [dict(user) for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users', methods=['POST'])
def add_user():
    """Yeni bir araç/kullanıcı ekler"""
    from flask import request
    try:
        data = request.json
        card_id = data.get('card_id')
        name = data.get('name')
        
        if not card_id or not name:
            return jsonify({"error": "Plaka/Kart ID ve İsim zorunludur"}), 400
            
        new_id = UserModel.create(
            card_id=card_id,
            name=name,
            phone=data.get('phone'),
            email=data.get('email'),
            vehicle_plate=card_id # Genellikle aynı kullanılır
        )
        return jsonify({"message": "Kullanıcı başarıyla eklendi", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Kullanıcıyı siler (Soft delete)"""
    try:
        success = UserModel.delete(user_id)
        if success:
            return jsonify({"message": "Kullanıcı başarıyla silindi"}), 200
        return jsonify({"error": "Kullanıcı bulunamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/logs', methods=['GET'])
def get_logs():
    """Son erişim kayıtlarını döner"""
    try:
        logs = LogModel.get_recent(limit=50)
        # Row nesnelerini dict'e çevir
        log_list = [dict(log) for log in logs]
        return jsonify(log_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    """Tek bir log kaydını siler"""
    try:
        success = LogModel.delete(log_id)
        if success:
            return jsonify({"message": "Log kaydı silindi"}), 200
        return jsonify({"error": "Log bulunamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/logs/unauthorized', methods=['DELETE'])
def clear_unauthorized_logs():
    """Tüm yetkisiz erişim kayıtlarını siler"""
    try:
        count = LogModel.delete_unauthorized()
        return jsonify({"message": f"{count} adet yetkisiz erişim kaydı silindi"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/logs/all', methods=['DELETE'])
def clear_all_logs():
    """Tüm log geçmişini temizler"""
    try:
        LogModel.clear_all()
        return jsonify({"message": "Tüm log geçmişi temizlendi"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
