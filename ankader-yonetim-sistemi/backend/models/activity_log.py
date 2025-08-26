#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ActivityLog Model - Aktivite Log Modeli
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

class ActivityLog:
    """Aktivite log modeli"""
    
    VALID_ACTIONS = [
        'login',
        'logout', 
        'password_change',
        'user_activity',
        'member_create',
        'member_update',
        'member_delete',
        'event_create',
        'event_update',
        'event_delete',
        'budget_create',
        'budget_update',
        'budget_delete',
        'admin_action'
    ]
    
    VALID_TARGET_TYPES = ['User', 'Member', 'Event', 'Budget']
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.user_id = kwargs.get('user_id')
        self.action = kwargs.get('action', '')
        self.description = kwargs.get('description', '')
        self.target_id = kwargs.get('target_id')
        self.target_type = kwargs.get('target_type')
        self.details = kwargs.get('details', {})
        self.created_at = kwargs.get('created_at', datetime.now())
    
    def validate(self) -> Dict[str, Any]:
        """Aktivite log verilerini doğrula"""
        errors = []
        
        # Kullanıcı ID kontrolü
        if not self.user_id:
            errors.append('Kullanıcı ID zorunludur')
        
        # Aksiyon kontrolü
        if not self.action:
            errors.append('Aksiyon zorunludur')
        elif self.action not in self.VALID_ACTIONS:
            errors.append(f'Geçersiz aksiyon. Geçerli aksiyonlar: {", ".join(self.VALID_ACTIONS)}')
        
        # Açıklama uzunluk kontrolü
        if self.description and len(self.description) > 500:
            errors.append('Açıklama maksimum 500 karakter olabilir')
        
        # Target type kontrolü
        if self.target_type and self.target_type not in self.VALID_TARGET_TYPES:
            errors.append(f'Geçersiz hedef tipi. Geçerli tipler: {", ".join(self.VALID_TARGET_TYPES)}')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def is_expired(self, expire_days: int = 180) -> bool:
        """Log süresi dolmuş mu? (varsayılan 6 ay)"""
        if not self.created_at:
            return False
        
        expire_date = self.created_at + timedelta(days=expire_days)
        return datetime.now() > expire_date
    
    def to_dict(self) -> Dict[str, Any]:
        """Log'u dictionary'ye çevir"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'description': self.description,
            'target_id': self.target_id,
            'target_type': self.target_type,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __str__(self):
        return f"ActivityLog(id={self.id}, user_id={self.user_id}, action='{self.action}')"
    
    def __repr__(self):
        return self.__str__()


class ActivityLogManager:
    """Aktivite log yönetimi için yardımcı sınıf"""
    
    def __init__(self):
        self.logs = []
        self._next_id = 1
    
    def create_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni aktivite log'u oluştur"""
        log_data['id'] = self._next_id
        activity_log = ActivityLog(**log_data)
        
        validation = activity_log.validate()
        if not validation['is_valid']:
            return {
                'success': False,
                'errors': validation['errors']
            }
        
        self.logs.append(activity_log)
        self._next_id += 1
        
        # Eski logları temizle (6 aydan eski)
        self._cleanup_expired_logs()
        
        return {
            'success': True,
            'log': activity_log.to_dict()
        }
    
    def log_activity(self, user_id: int, action: str, description: str = '', 
                    target_id: int = None, target_type: str = None, 
                    details: Dict[str, Any] = None) -> bool:
        """Aktivite logla (kısa yol)"""
        log_data = {
            'user_id': user_id,
            'action': action,
            'description': description,
            'target_id': target_id,
            'target_type': target_type,
            'details': details or {}
        }
        
        result = self.create_log(log_data)
        return result['success']
    
    def get_logs_by_user(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Kullanıcıya göre logları getir"""
        user_logs = [log for log in self.logs if log.user_id == user_id]
        user_logs.sort(key=lambda x: x.created_at, reverse=True)
        
        if limit:
            user_logs = user_logs[:limit]
        
        return [log.to_dict() for log in user_logs]
    
    def get_logs_by_action(self, action: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Aksiyona göre logları getir"""
        action_logs = [log for log in self.logs if log.action == action]
        action_logs.sort(key=lambda x: x.created_at, reverse=True)
        
        if limit:
            action_logs = action_logs[:limit]
        
        return [log.to_dict() for log in action_logs]
    
    def get_logs_by_target(self, target_id: int, target_type: str, 
                          limit: int = 50) -> List[Dict[str, Any]]:
        """Hedef nesneye göre logları getir"""
        target_logs = [
            log for log in self.logs 
            if log.target_id == target_id and log.target_type == target_type
        ]
        target_logs.sort(key=lambda x: x.created_at, reverse=True)
        
        if limit:
            target_logs = target_logs[:limit]
        
        return [log.to_dict() for log in target_logs]
    
    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Son logları getir"""
        recent_logs = sorted(self.logs, key=lambda x: x.created_at, reverse=True)
        
        if limit:
            recent_logs = recent_logs[:limit]
        
        return [log.to_dict() for log in recent_logs]
    
    def get_logs_in_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Tarih aralığına göre logları getir"""
        filtered_logs = [
            log for log in self.logs 
            if start_date <= log.created_at <= end_date
        ]
        filtered_logs.sort(key=lambda x: x.created_at, reverse=True)
        
        return [log.to_dict() for log in filtered_logs]
    
    def search_logs(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Loglarda ara (açıklama ve aksiyon)"""
        query = query.lower().strip()
        results = []
        
        for log in self.logs:
            if (query in log.action.lower() or 
                (log.description and query in log.description.lower())):
                results.append(log.to_dict())
        
        results.sort(key=lambda x: x['created_at'], reverse=True)
        
        if limit:
            results = results[:limit]
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Log istatistikleri"""
        total_logs = len(self.logs)
        
        # Aksiyon dağılımı
        action_distribution = {}
        for log in self.logs:
            action = log.action
            action_distribution[action] = action_distribution.get(action, 0) + 1
        
        # Kullanıcı aktivite dağılımı
        user_activity = {}
        for log in self.logs:
            user_id = log.user_id
            user_activity[user_id] = user_activity.get(user_id, 0) + 1
        
        # Son 24 saat
        last_24h = datetime.now() - timedelta(hours=24)
        recent_logs = [log for log in self.logs if log.created_at >= last_24h]
        
        # Son 7 gün
        last_7d = datetime.now() - timedelta(days=7)
        weekly_logs = [log for log in self.logs if log.created_at >= last_7d]
        
        return {
            'total_logs': total_logs,
            'last_24_hours': len(recent_logs),
            'last_7_days': len(weekly_logs),
            'action_distribution': action_distribution,
            'user_activity': user_activity,
            'most_active_users': sorted(
                user_activity.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        }
    
    def _cleanup_expired_logs(self, expire_days: int = 180):
        """Süresi dolmuş logları temizle"""
        self.logs = [log for log in self.logs if not log.is_expired(expire_days)]
    
    def cleanup_logs_older_than(self, days: int):
        """Belirtilen günden eski logları temizle"""
        cutoff_date = datetime.now() - timedelta(days=days)
        self.logs = [log for log in self.logs if log.created_at >= cutoff_date]
    
    def clear_all_logs(self):
        """Tüm logları temizle"""
        self.logs = []
    
    # Özel log metodları
    def log_login(self, user_id: int, ip: str = '', user_agent: str = ''):
        """Giriş logla"""
        return self.log_activity(
            user_id=user_id,
            action='login',
            description='Kullanıcı sisteme giriş yaptı',
            details={
                'ip': ip,
                'user_agent': user_agent
            }
        )
    
    def log_logout(self, user_id: int):
        """Çıkış logla"""
        return self.log_activity(
            user_id=user_id,
            action='logout',
            description='Kullanıcı sistemden çıkış yaptı'
        )
    
    def log_member_create(self, user_id: int, member_id: int, member_name: str):
        """Üye oluşturma logla"""
        return self.log_activity(
            user_id=user_id,
            action='member_create',
            description=f'Yeni üye oluşturuldu: {member_name}',
            target_id=member_id,
            target_type='Member'
        )
    
    def log_event_create(self, user_id: int, event_id: int, event_title: str):
        """Etkinlik oluşturma logla"""
        return self.log_activity(
            user_id=user_id,
            action='event_create',
            description=f'Yeni etkinlik oluşturuldu: {event_title}',
            target_id=event_id,
            target_type='Event'
        )


# Global aktivite log yöneticisi
activity_log_manager = ActivityLogManager()
