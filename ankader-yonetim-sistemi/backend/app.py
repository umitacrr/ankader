#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANKADER Dernek Yönetim Sistemi Backend API
Python Flask uygulaması
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from routes import auth_bp, members_bp, events_bp, admin_bp
from models import user_manager, activity_log_manager

# Flask uygulaması oluştur
app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir

# Blueprint'leri kaydet
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(members_bp, url_prefix='/api/members')
app.register_blueprint(events_bp, url_prefix='/api/events')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

@app.route('/', methods=['GET'])
def home():
    """Ana sayfa endpoint'i"""
    return jsonify({
        "message": "ANKADER Dernek Yönetim Sistemi Backend API",
        "version": "1.0.0",
        "status": "Çalışıyor",
        "framework": "Python Flask",
        "endpoints": {
            "auth": "/api/auth/*",
            "members": "/api/members/*",
            "events": "/api/events/*",
            "admin": "/api/admin/*",
            "test": "/api/test"
        }
    })

@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint'i"""
    return jsonify({
        "success": True,
        "message": "ANKADER Backend çalışıyor!",
        "timestamp": datetime.now().isoformat(),
        "framework": "Python Flask",
        "total_users": len(user_manager.users),
        "total_logs": len(activity_log_manager.logs)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Sağlık kontrolü endpoint'i"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "user_manager": "active",
            "member_manager": "active", 
            "event_manager": "active",
            "activity_log_manager": "active"
        }
    })

@app.errorhandler(404)
def not_found(error):
    """404 hatası için handler"""
    return jsonify({
        "success": False,
        "message": "Route bulunamadı",
        "available_endpoints": [
            "/api/auth/login",
            "/api/auth/me",
            "/api/members",
            "/api/events", 
            "/api/admin/dashboard"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 hatası için handler"""
    return jsonify({
        "success": False,
        "message": "Sunucu hatası"
    }), 500

@app.errorhandler(401)
def unauthorized(error):
    """401 hatası için handler"""
    return jsonify({
        "success": False,
        "message": "Yetkilendirme gerekli"
    }), 401

@app.errorhandler(403)
def forbidden(error):
    """403 hatası için handler"""
    return jsonify({
        "success": False,
        "message": "Bu işlem için yetkiniz yok"
    }), 403

if __name__ == '__main__':
    print("🚀 ANKADER Backend sunucusu Python Flask ile başlatılıyor...")
    print("📋 Ana yönetici bilgileri:")
    print("   - Ad: ACAR")
    print("   - Telefon: 05000000000")
    print("   - Şifre: acar2024!")
    print("🌐 Test URL: http://localhost:5000/api/test")
    print("💻 Framework: Python Flask")
    
    # Flask sunucusunu başlat
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
