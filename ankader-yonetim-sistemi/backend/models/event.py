#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Event Model - Etkinlik Modeli
"""

from datetime import datetime, date
import re
from typing import Dict, Any, Optional, List

class Event:
    """Etkinlik modeli"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title', '').strip()
        self.description = kwargs.get('description', '').strip()
        self.date = kwargs.get('date')
        self.start_time = kwargs.get('start_time', '').strip()
        self.end_time = kwargs.get('end_time', '').strip()
        self.location = kwargs.get('location', '').strip()
        self.type = kwargs.get('type', 'other')
        self.status = kwargs.get('status', 'planning')
        self.max_participants = kwargs.get('max_participants')
        self.participants = kwargs.get('participants', [])
        self.budget = kwargs.get('budget', {
            'estimated_cost': 0,
            'actual_cost': 0,
            'income': 0
        })
        self.organizer = kwargs.get('organizer')
        self.assistants = kwargs.get('assistants', [])
        self.attachments = kwargs.get('attachments', [])
        self.feedback = kwargs.get('feedback', [])
        self.created_by = kwargs.get('created_by')
        self.updated_by = kwargs.get('updated_by')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def validate(self) -> Dict[str, Any]:
        """Etkinlik verilerini doğrula"""
        errors = []
        
        # Başlık kontrolü
        if not self.title or len(self.title.strip()) == 0:
            errors.append('Etkinlik başlığı zorunludur')
        elif len(self.title) > 200:
            errors.append('Başlık maksimum 200 karakter olabilir')
        
        # Açıklama kontrolü
        if not self.description or len(self.description.strip()) == 0:
            errors.append('Etkinlik açıklaması zorunludur')
        elif len(self.description) > 2000:
            errors.append('Açıklama maksimum 2000 karakter olabilir')
        
        # Tarih kontrolü
        if not self.date:
            errors.append('Etkinlik tarihi zorunludur')
        elif not isinstance(self.date, (datetime, date)):
            errors.append('Geçersiz tarih formatı')
        
        # Başlangıç saati kontrolü
        if not self.start_time:
            errors.append('Başlangıç saati zorunludur')
        elif not self._validate_time(self.start_time):
            errors.append('Geçerli bir başlangıç saati formatı girin (HH:MM)')
        
        # Bitiş saati kontrolü
        if self.end_time and not self._validate_time(self.end_time):
            errors.append('Geçerli bir bitiş saati formatı girin (HH:MM)')
        
        # Yer kontrolü
        if not self.location or len(self.location.strip()) == 0:
            errors.append('Etkinlik yeri zorunludur')
        elif len(self.location) > 300:
            errors.append('Yer bilgisi maksimum 300 karakter olabilir')
        
        # Tip kontrolü
        valid_types = ['meeting', 'social', 'educational', 'fundraising', 'other']
        if self.type not in valid_types:
            errors.append(f'Geçersiz etkinlik tipi. Geçerli tipler: {", ".join(valid_types)}')
        
        # Durum kontrolü
        valid_statuses = ['planning', 'confirmed', 'ongoing', 'completed', 'cancelled']
        if self.status not in valid_statuses:
            errors.append(f'Geçersiz durum. Geçerli durumlar: {", ".join(valid_statuses)}')
        
        # Maksimum katılımcı kontrolü
        if self.max_participants is not None and self.max_participants < 1:
            errors.append('Maksimum katılımcı sayısı en az 1 olmalıdır')
        
        # Bütçe kontrolü
        if isinstance(self.budget, dict):
            for key in ['estimated_cost', 'actual_cost', 'income']:
                value = self.budget.get(key, 0)
                if value < 0:
                    errors.append(f'{key} negatif olamaz')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def _validate_time(self, time_str: str) -> bool:
        """Saat formatını kontrol et (HH:MM)"""
        pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
        return bool(re.match(pattern, time_str))
    
    @property
    def participant_count(self) -> int:
        """Katılımcı sayısı"""
        return len(self.participants) if self.participants else 0
    
    @property
    def attended_count(self) -> int:
        """Katılan katılımcı sayısı"""
        if not self.participants:
            return 0
        return len([p for p in self.participants if p.get('attendance_status') == 'attended'])
    
    @property
    def is_upcoming(self) -> bool:
        """Gelecek etkinlik mi?"""
        if not self.date:
            return False
        
        if isinstance(self.date, date) and not isinstance(self.date, datetime):
            event_date = datetime.combine(self.date, datetime.min.time())
        else:
            event_date = self.date
        
        return event_date > datetime.now()
    
    @property
    def is_past(self) -> bool:
        """Geçmiş etkinlik mi?"""
        return not self.is_upcoming
    
    @property
    def average_rating(self) -> float:
        """Ortalama değerlendirme"""
        if not self.feedback:
            return 0.0
        
        ratings = [f.get('rating', 0) for f in self.feedback if f.get('rating')]
        if not ratings:
            return 0.0
        
        return round(sum(ratings) / len(ratings), 1)
    
    def add_participant(self, member_id: int, notes: str = '') -> bool:
        """Katılımcı ekle"""
        if not self.participants:
            self.participants = []
        
        # Zaten katılımcı mı kontrol et
        for participant in self.participants:
            if participant.get('member_id') == member_id:
                return False
        
        # Maksimum katılımcı kontrolü
        if (self.max_participants and 
            len(self.participants) >= self.max_participants):
            return False
        
        self.participants.append({
            'member_id': member_id,
            'registration_date': datetime.now(),
            'attendance_status': 'registered',
            'notes': notes
        })
        
        self.updated_at = datetime.now()
        return True
    
    def update_participant_status(self, member_id: int, status: str) -> bool:
        """Katılımcı durumunu güncelle"""
        if not self.participants:
            return False
        
        valid_statuses = ['registered', 'attended', 'absent', 'cancelled']
        if status not in valid_statuses:
            return False
        
        for participant in self.participants:
            if participant.get('member_id') == member_id:
                participant['attendance_status'] = status
                self.updated_at = datetime.now()
                return True
        
        return False
    
    def remove_participant(self, member_id: int) -> bool:
        """Katılımcı kaldır"""
        if not self.participants:
            return False
        
        original_length = len(self.participants)
        self.participants = [p for p in self.participants if p.get('member_id') != member_id]
        
        if len(self.participants) < original_length:
            self.updated_at = datetime.now()
            return True
        
        return False
    
    def add_feedback(self, member_id: int, rating: int, comment: str = '') -> bool:
        """Geri bildirim ekle"""
        if rating < 1 or rating > 5:
            return False
        
        if len(comment) > 1000:
            return False
        
        if not self.feedback:
            self.feedback = []
        
        # Aynı üyeden geri bildirim var mı kontrol et
        for fb in self.feedback:
            if fb.get('member_id') == member_id:
                # Güncelle
                fb['rating'] = rating
                fb['comment'] = comment
                fb['date'] = datetime.now()
                self.updated_at = datetime.now()
                return True
        
        # Yeni geri bildirim ekle
        self.feedback.append({
            'member_id': member_id,
            'rating': rating,
            'comment': comment,
            'date': datetime.now()
        })
        
        self.updated_at = datetime.now()
        return True
    
    def add_attachment(self, filename: str, original_name: str, mimetype: str, size: int) -> bool:
        """Ek dosya ekle"""
        if not self.attachments:
            self.attachments = []
        
        self.attachments.append({
            'filename': filename,
            'original_name': original_name,
            'mimetype': mimetype,
            'size': size,
            'upload_date': datetime.now()
        })
        
        self.updated_at = datetime.now()
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Etkinliği dictionary'ye çevir"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location,
            'type': self.type,
            'status': self.status,
            'max_participants': self.max_participants,
            'participants': self.participants,
            'participant_count': self.participant_count,
            'attended_count': self.attended_count,
            'budget': self.budget,
            'organizer': self.organizer,
            'assistants': self.assistants,
            'attachments': self.attachments,
            'feedback': self.feedback,
            'average_rating': self.average_rating,
            'is_upcoming': self.is_upcoming,
            'is_past': self.is_past,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __str__(self):
        return f"Event(id={self.id}, title='{self.title}', status='{self.status}')"
    
    def __repr__(self):
        return self.__str__()


class EventManager:
    """Etkinlik yönetimi için yardımcı sınıf"""
    
    def __init__(self):
        self.events = []
        self._next_id = 1
    
    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni etkinlik oluştur"""
        event_data['id'] = self._next_id
        event = Event(**event_data)
        
        validation = event.validate()
        if not validation['is_valid']:
            return {
                'success': False,
                'errors': validation['errors']
            }
        
        self.events.append(event)
        self._next_id += 1
        
        return {
            'success': True,
            'event': event.to_dict()
        }
    
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """ID'ye göre etkinlik bul"""
        for event in self.events:
            if event.id == event_id:
                return event
        return None
    
    def get_all_events(self, status: str = None) -> List[Dict[str, Any]]:
        """Tüm etkinlikleri getir"""
        filtered_events = self.events
        
        if status:
            filtered_events = [event for event in self.events if event.status == status]
        
        return [event.to_dict() for event in filtered_events]
    
    def get_upcoming_events(self) -> List[Dict[str, Any]]:
        """Gelecek etkinlikleri getir"""
        upcoming = [event for event in self.events if event.is_upcoming]
        upcoming.sort(key=lambda x: x.date)
        return [event.to_dict() for event in upcoming]
    
    def get_past_events(self) -> List[Dict[str, Any]]:
        """Geçmiş etkinlikleri getir"""
        past = [event for event in self.events if event.is_past]
        past.sort(key=lambda x: x.date, reverse=True)
        return [event.to_dict() for event in past]
    
    def search_events(self, query: str) -> List[Dict[str, Any]]:
        """Etkinlik ara (başlık, açıklama)"""
        query = query.lower().strip()
        results = []
        
        for event in self.events:
            if (query in event.title.lower() or 
                query in event.description.lower() or
                query in event.location.lower()):
                results.append(event.to_dict())
        
        return results
    
    def update_event(self, event_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Etkinlik bilgilerini güncelle"""
        event = self.get_event_by_id(event_id)
        if not event:
            return {
                'success': False,
                'errors': ['Etkinlik bulunamadı']
            }
        
        # Güncellenebilir alanları güncelle
        updatable_fields = [
            'title', 'description', 'date', 'start_time', 'end_time', 
            'location', 'type', 'status', 'max_participants', 'budget',
            'organizer', 'assistants', 'updated_by'
        ]
        
        for field in updatable_fields:
            if field in update_data:
                setattr(event, field, update_data[field])
        
        event.updated_at = datetime.now()
        
        validation = event.validate()
        if not validation['is_valid']:
            return {
                'success': False,
                'errors': validation['errors']
            }
        
        return {
            'success': True,
            'event': event.to_dict()
        }
    
    def delete_event(self, event_id: int) -> Dict[str, Any]:
        """Etkinliği sil"""
        event = self.get_event_by_id(event_id)
        if not event:
            return {
                'success': False,
                'errors': ['Etkinlik bulunamadı']
            }
        
        self.events = [e for e in self.events if e.id != event_id]
        
        return {
            'success': True,
            'message': 'Etkinlik başarıyla silindi'
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Etkinlik istatistikleri"""
        total_events = len(self.events)
        upcoming_events = len([e for e in self.events if e.is_upcoming])
        past_events = len([e for e in self.events if e.is_past])
        
        # Durum dağılımı
        status_distribution = {}
        for event in self.events:
            status = event.status
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        # Tip dağılımı
        type_distribution = {}
        for event in self.events:
            event_type = event.type
            type_distribution[event_type] = type_distribution.get(event_type, 0) + 1
        
        return {
            'total_events': total_events,
            'upcoming_events': upcoming_events,
            'past_events': past_events,
            'status_distribution': status_distribution,
            'type_distribution': type_distribution,
            'recent_events': [
                e.to_dict() for e in sorted(
                    self.events, 
                    key=lambda x: x.created_at, 
                    reverse=True
                )[:5]
            ]
        }


# Global etkinlik yöneticisi
event_manager = EventManager()
