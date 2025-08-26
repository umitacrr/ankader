#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Routes - Kimlik doğrulama route'ları
"""

from flask import Blueprint, request, jsonify, g
from models import user_manager, activity_log_manager
from middleware import auth_required, log_activity
import base64
import time
import re

auth_bp = Blueprint('auth', __name__)

def validate_login_data(data):
    """Giriş verilerini doğrula"""
    errors = []
    
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '').strip()
    
    if not name:
        errors.append('Ad soyad zorunludur')
    
    if not phone:
        errors.append('Telefon numarası zorunludur')
    
    if not password:
        errors.append('Şifre zorunludur')
    elif len(password) < 6:
        errors.append('Şifre en az 6 karakter olmalıdır')
    
    return errors, name, phone, password

@auth_bp.route('/login', methods=['POST'])
@log_activity('login_attempt', 'Giriş denemesi')
def login():
    """Kullanıcı girişi"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        # Veri doğrulama
        errors, name, phone, password = validate_login_data(data)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Doğrulama hatası',
                'errors': errors
            }), 400
        
        # Kullanıcı kimlik doğrulaması
        user = user_manager.authenticate(name, phone, password)
        if not user:
            # Başarısız giriş logla
            activity_log_manager.log_activity(
                user_id=0,  # Bilinmeyen kullanıcı
                action='login_failed',
                description=f'Başarısız giriş denemesi: {name} - {phone}',
                details={
                    'ip': request.remote_addr,
                    'user_agent': request.headers.get('User-Agent', ''),
                    'name': name,
                    'phone': phone
                }
            )
            
            return jsonify({
                'success': False,
                'message': 'Geçersiz giriş bilgileri'
            }), 401
        
        # Token oluştur
        token_data = f"{user.id}:{int(time.time())}"
        token = base64.b64encode(token_data.encode()).decode()
        
        # Başarılı giriş logla
        activity_log_manager.log_login(
            user_id=user.id,
            ip=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        return jsonify({
            'success': True,
            'message': 'Giriş başarılı',
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'phone': user.phone,
                'role': user.role,
                'permissions': user.permissions,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/me', methods=['GET'])
@auth_required
def get_current_user():
    """Mevcut kullanıcı bilgilerini al"""
    try:
        user = g.user
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/change-password', methods=['PUT'])
@auth_required
@log_activity('password_change', 'Şifre değiştirme')
def change_password():
    """Şifre değiştir"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        current_password = data.get('current_password', '').strip()
        new_password = data.get('new_password', '').strip()
        
        # Veri doğrulama
        errors = []
        if not current_password:
            errors.append('Mevcut şifre zorunludur')
        if not new_password:
            errors.append('Yeni şifre zorunludur')
        elif len(new_password) < 6:
            errors.append('Yeni şifre en az 6 karakter olmalıdır')
        
        if errors:
            return jsonify({
                'success': False,
                'message': 'Doğrulama hatası',
                'errors': errors
            }), 400
        
        user = g.user
        
        # Mevcut şifre kontrolü
        if user.password != current_password:
            return jsonify({
                'success': False,
                'message': 'Mevcut şifre yanlış'
            }), 400
        
        # Yeni şifreyi güncelle
        update_result = user_manager.update_user(user.id, {
            'password': new_password
        })
        
        if not update_result['success']:
            return jsonify(update_result), 400
        
        return jsonify({
            'success': True,
            'message': 'Şifre başarıyla değiştirildi'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/log-activity', methods=['POST'])
@auth_required
def log_user_activity():
    """Kullanıcı aktivitesini logla"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        activity = data.get('activity', '').strip()
        details = data.get('details', {})
        
        if not activity:
            return jsonify({
                'success': False,
                'message': 'Aktivite bilgisi zorunludur'
            }), 400
        
        user = g.user
        
        # Aktiviteyi logla
        request_details = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', ''),
            **details
        }
        
        activity_log_manager.log_activity(
            user_id=user.id,
            action='user_activity',
            description=activity,
            details=request_details
        )
        
        return jsonify({
            'success': True,
            'message': 'Aktivite kaydedildi'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/verify-token', methods=['POST'])
@auth_required
def verify_token():
    """Token doğrula"""
    try:
        user = g.user
        
        return jsonify({
            'success': True,
            'message': 'Token geçerli',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@auth_required
@log_activity('logout', 'Çıkış yapıldı')
def logout():
    """Çıkış yap"""
    try:
        user = g.user
        
        # Çıkış logla
        activity_log_manager.log_logout(user.id)
        
        return jsonify({
            'success': True,
            'message': 'Başarıyla çıkış yapıldı'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/refresh-token', methods=['POST'])
@auth_required
def refresh_token():
    """Token yenile"""
    try:
        user = g.user
        
        # Yeni token oluştur
        token_data = f"{user.id}:{int(time.time())}"
        new_token = base64.b64encode(token_data.encode()).decode()
        
        return jsonify({
            'success': True,
            'message': 'Token yenilendi',
            'token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@auth_required
def get_profile():
    """Kullanıcı profili"""
    try:
        user = g.user
        
        # Son aktiviteler
        recent_activities = activity_log_manager.get_logs_by_user(user.id, limit=10)
        
        return jsonify({
            'success': True,
            'profile': {
                'user': user.to_dict(),
                'recent_activities': recent_activities,
                'login_count': len([
                    log for log in activity_log_manager.get_logs_by_user(user.id, limit=100)
                    if log['action'] == 'login'
                ])
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@auth_required
@log_activity('profile_update', 'Profil güncellendi')
def update_profile():
    """Profil güncelle"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        user = g.user
        
        # Güncellenebilir alanlar
        updatable_fields = ['name', 'phone']
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return jsonify({
                'success': False,
                'message': 'Güncellenecek alan bulunamadı'
            }), 400
        
        # Kullanıcıyı güncelle
        result = user_manager.update_user(user.id, update_data)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify({
            'success': True,
            'message': 'Profil başarıyla güncellendi',
            'user': result['user']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500
