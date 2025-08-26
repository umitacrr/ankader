#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Middleware - Kimlik doğrulama ve yetkilendirme middleware'i
"""

from functools import wraps
from flask import request, jsonify, g
import base64
import time
from typing import List, Callable, Any
from models import user_manager, activity_log_manager

def decode_token(token: str) -> dict:
    """Token'ı decode et"""
    try:
        # Basit base64 token (gerçek uygulamada JWT kullanılmalı)
        decoded = base64.b64decode(token).decode()
        user_id, timestamp = decoded.split(':')
        
        # Token 24 saat geçerli
        token_age = time.time() - int(timestamp)
        if token_age > 86400:  # 24 saat = 86400 saniye
            return None
        
        return {
            'user_id': int(user_id),
            'timestamp': int(timestamp)
        }
    except Exception:
        return None

def get_token_from_request() -> str:
    """Request'ten token'ı al"""
    auth_header = request.headers.get('Authorization', '')
    
    if auth_header.startswith('Bearer '):
        return auth_header.replace('Bearer ', '')
    
    return ''

def auth_required(f: Callable) -> Callable:
    """Kimlik doğrulama gerekli decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token bulunamadı, erişim reddedildi'
            }), 401
        
        decoded = decode_token(token)
        if not decoded:
            return jsonify({
                'success': False,
                'message': 'Geçersiz veya süresi dolmuş token'
            }), 401
        
        user = user_manager.get_user_by_id(decoded['user_id'])
        if not user:
            return jsonify({
                'success': False,
                'message': 'Kullanıcı bulunamadı'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Hesap deaktif durumda'
            }), 401
        
        # Kullanıcıyı global context'e ekle
        g.user = user
        g.token_data = decoded
        
        return f(*args, **kwargs)
    
    return decorated_function

def role_required(*roles: List[str]) -> Callable:
    """Belirli roller için yetkilendirme decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        @auth_required
        def decorated_function(*args, **kwargs):
            user = g.user
            
            if user.role not in roles:
                return jsonify({
                    'success': False,
                    'message': f'Bu işlem için yetkiniz yok. Gerekli roller: {", ".join(roles)}'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def permission_required(resource: str, action: str) -> Callable:
    """Belirli izin için yetkilendirme decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        @auth_required
        def decorated_function(*args, **kwargs):
            user = g.user
            
            # ACAR her şeyi yapabilir
            if user.role == 'ACAR':
                return f(*args, **kwargs)
            
            if not user.has_permission(resource, action):
                return jsonify({
                    'success': False,
                    'message': f'{resource} {action} işlemi için yetkiniz yok'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def admin_required(f: Callable) -> Callable:
    """Admin yetkisi gerekli decorator"""
    return role_required('ACAR', 'admin')(f)

def acar_required(f: Callable) -> Callable:
    """ACAR yetkisi gerekli decorator"""
    return role_required('ACAR')(f)

def log_activity(action: str, description: str = '', target_id: int = None, 
                target_type: str = None, details: dict = None) -> Callable:
    """Aktivite logla decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Orijinal fonksiyonu çalıştır
            result = f(*args, **kwargs)
            
            # Eğer kullanıcı varsa aktiviteyi logla
            if hasattr(g, 'user') and g.user:
                try:
                    # Request bilgilerini topla
                    request_details = details or {}
                    request_details.update({
                        'ip': request.remote_addr,
                        'user_agent': request.headers.get('User-Agent', ''),
                        'method': request.method,
                        'endpoint': request.endpoint
                    })
                    
                    activity_log_manager.log_activity(
                        user_id=g.user.id,
                        action=action,
                        description=description or f'{action} işlemi gerçekleştirildi',
                        target_id=target_id,
                        target_type=target_type,
                        details=request_details
                    )
                except Exception as e:
                    print(f"Aktivite loglama hatası: {e}")
            
            return result
        
        return decorated_function
    return decorator

def get_current_user():
    """Mevcut kullanıcıyı döndür"""
    return getattr(g, 'user', None)

def get_current_user_id():
    """Mevcut kullanıcı ID'sini döndür"""
    user = get_current_user()
    return user.id if user else None

def is_authenticated():
    """Kullanıcı kimlik doğrulaması yapılmış mı?"""
    return hasattr(g, 'user') and g.user is not None

def has_role(*roles: List[str]) -> bool:
    """Kullanıcının belirtilen rollerden biri var mı?"""
    user = get_current_user()
    if not user:
        return False
    return user.role in roles

def has_permission(resource: str, action: str) -> bool:
    """Kullanıcının belirtilen izni var mı?"""
    user = get_current_user()
    if not user:
        return False
    
    # ACAR her şeyi yapabilir
    if user.role == 'ACAR':
        return True
    
    return user.has_permission(resource, action)

def check_api_key(api_key: str) -> bool:
    """API key kontrolü (isteğe bağlı)"""
    # Basit API key kontrolü
    valid_api_keys = [
        'ankader-api-key-2024',
        'development-key'
    ]
    return api_key in valid_api_keys

def api_key_required(f: Callable) -> Callable:
    """API key gerekli decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key', '')
        
        if not api_key:
            return jsonify({
                'success': False,
                'message': 'API key gerekli'
            }), 401
        
        if not check_api_key(api_key):
            return jsonify({
                'success': False,
                'message': 'Geçersiz API key'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def optional_auth(f: Callable) -> Callable:
    """İsteğe bağlı kimlik doğrulama decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        
        if token:
            decoded = decode_token(token)
            if decoded:
                user = user_manager.get_user_by_id(decoded['user_id'])
                if user and user.is_active:
                    g.user = user
                    g.token_data = decoded
        
        return f(*args, **kwargs)
    
    return decorated_function

# Rate limiting için basit memory store
_request_counts = {}

def rate_limit(max_requests: int, window_seconds: int) -> Callable:
    """Rate limiting decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = int(time.time())
            window_start = current_time - window_seconds
            
            # Eski kayıtları temizle
            _request_counts[client_ip] = [
                req_time for req_time in _request_counts.get(client_ip, [])
                if req_time > window_start
            ]
            
            # Request sayısını kontrol et
            if len(_request_counts.get(client_ip, [])) >= max_requests:
                return jsonify({
                    'success': False,
                    'message': 'Çok fazla istek. Lütfen bekleyin.'
                }), 429
            
            # Yeni request'i ekle
            if client_ip not in _request_counts:
                _request_counts[client_ip] = []
            _request_counts[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
