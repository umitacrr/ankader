#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Model - Kullanıcı Modeli
"""

from datetime import datetime
import re
from typing import Dict, Any, Optional

class User:
    """Kullanıcı modeli"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name', '').strip()
        self.phone = kwargs.get('phone', '').strip()
        self.password = kwargs.get('password', '')
        self.role = kwargs.get('role', 'admin')
        self.is_active = kwargs.get('is_active', True)
        self.last_login = kwargs.get('last_login')
        self.created_by = kwargs.get('created_by')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        
        # Varsayılan izinler
        default_permissions = {
            'members': {'read': True, 'write': True, 'delete': False},
            'events': {'read': True, 'write': True, 'delete': False},
            'budget': {'read': True, 'write': True, 'delete': False},
            'admin': {'read': False, 'write': False, 'delete': False}
        }
        
        self.permissions = kwargs.get('permissions', default_permissions)
        
        # ACAR rolü için tüm izinleri ver
        if self.role == 'ACAR':
            self.permissions = {
                'members': {'read': True, 'write': True, 'delete': True},
                'events': {'read': True, 'write': True, 'delete': True},
                'budget': {'read': True, 'write': True, 'delete': True},
                'admin': {'read': True, 'write': True, 'delete': True}
            }
    
    def validate(self) -> Dict[str, Any]:
        """Kullanıcı verilerini doğrula"""
        errors = []
        
        # Ad kontrolü
        if not self.name or len(self.name.strip()) == 0:
            errors.append('Ad soyad zorunludur')
        elif len(self.name) > 100:
            errors.append('Ad soyad maksimum 100 karakter olabilir')
        
        # Telefon kontrolü
        if not self.phone:
            errors.append('Telefon numarası zorunludur')
        elif not self._validate_phone():
            errors.append('Geçerli bir telefon numarası girin')
        
        # Şifre kontrolü
        if not self.password:
            errors.append('Şifre zorunludur')
        elif len(self.password) < 6:
            errors.append('Şifre en az 6 karakter olmalıdır')
        
        # Rol kontrolü
        valid_roles = ['ACAR', 'admin', 'moderator']
        if self.role not in valid_roles:
            errors.append(f'Geçersiz rol. Geçerli roller: {", ".join(valid_roles)}')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def _validate_phone(self) -> bool:
        """Telefon numarası formatını kontrol et"""
        # Türkiye telefon numarası formatı: 05xxxxxxxxx
        pattern = r'^(\+90|0)?5\d{9}$'
        return bool(re.match(pattern, self.phone))
    
    def to_dict(self, include_password: bool = False) -> Dict[str, Any]:
        """Kullanıcıyı dictionary'ye çevir"""
        user_dict = {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'permissions': self.permissions
        }
        
        if include_password:
            user_dict['password'] = self.password
        
        return user_dict
    
    def update_last_login(self):
        """Son giriş zamanını güncelle"""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()
    
    def has_permission(self, module: str, action: str) -> bool:
        """Kullanıcının belirli bir modül ve eylem için izni var mı kontrol et"""
        if module not in self.permissions:
            return False
        
        if action not in self.permissions[module]:
            return False
        
        return self.permissions[module][action]
    
    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', role='{self.role}')"
    
    def __repr__(self):
        return self.__str__()


class UserManager:
    """Kullanıcı yönetimi için yardımcı sınıf"""
    
    def __init__(self):
        # Bellekte kullanıcı verilerini tut (gerçek uygulamada veritabanı kullanılmalı)
        self.users = []
        self._next_id = 1
        
        # Varsayılan ACAR kullanıcısını ekle
        self.create_default_admin()
    
    def create_default_admin(self):
        """Varsayılan ACAR kullanıcısını oluştur"""
        admin_user = User(
            id=self._next_id,
            name='ACAR',
            phone='05000000000',
            password='acar2024!',
            role='ACAR',
            is_active=True
        )
        
        validation = admin_user.validate()
        if validation['is_valid']:
            self.users.append(admin_user)
            self._next_id += 1
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni kullanıcı oluştur"""
        user_data['id'] = self._next_id
        user = User(**user_data)
        
        validation = user.validate()
        if not validation['is_valid']:
            return {
                'success': False,
                'errors': validation['errors']
            }
        
        # Telefon numarası benzersizlik kontrolü
        if self.get_user_by_phone(user.phone):
            return {
                'success': False,
                'errors': ['Bu telefon numarası zaten kullanılıyor']
            }
        
        self.users.append(user)
        self._next_id += 1
        
        return {
            'success': True,
            'user': user.to_dict()
        }
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID'ye göre kullanıcı bul"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """Telefon numarasına göre kullanıcı bul"""
        for user in self.users:
            if user.phone == phone:
                return user
        return None
    
    def authenticate(self, name: str, phone: str, password: str) -> Optional[User]:
        """Kullanıcı kimlik doğrulaması"""
        for user in self.users:
            if (user.name.lower() == name.lower() and 
                user.phone == phone and 
                user.password == password and 
                user.is_active):
                user.update_last_login()
                return user
        return None
    
    def get_all_users(self) -> list:
        """Tüm kullanıcıları getir"""
        return [user.to_dict() for user in self.users if user.is_active]
    
    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Kullanıcı bilgilerini güncelle"""
        user = self.get_user_by_id(user_id)
        if not user:
            return {
                'success': False,
                'errors': ['Kullanıcı bulunamadı']
            }
        
        # Güncellenebilir alanları güncelle
        updatable_fields = ['name', 'phone', 'role', 'is_active', 'permissions']
        for field in updatable_fields:
            if field in update_data:
                setattr(user, field, update_data[field])
        
        user.updated_at = datetime.now()
        
        validation = user.validate()
        if not validation['is_valid']:
            return {
                'success': False,
                'errors': validation['errors']
            }
        
        return {
            'success': True,
            'user': user.to_dict()
        }
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Kullanıcıyı sil (soft delete)"""
        user = self.get_user_by_id(user_id)
        if not user:
            return {
                'success': False,
                'errors': ['Kullanıcı bulunamadı']
            }
        
        if user.role == 'ACAR':
            return {
                'success': False,
                'errors': ['ACAR kullanıcısı silinemez']
            }
        
        user.is_active = False
        user.updated_at = datetime.now()
        
        return {
            'success': True,
            'message': 'Kullanıcı başarıyla silindi'
        }


# Global kullanıcı yöneticisi
user_manager = UserManager()
