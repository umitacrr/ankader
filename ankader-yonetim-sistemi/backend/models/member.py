#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Member Model - Üye Modeli
"""

from datetime import datetime
import re
from typing import Dict, Any, Optional, List

class Member:
    """Üye modeli"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.photo = kwargs.get('photo', '/uploads/default-avatar.png')
        self.name = kwargs.get('name', '').strip()
        self.phone = kwargs.get('phone', '').strip()
        self.email = kwargs.get('email', '').strip().lower()
        self.graduation_year = kwargs.get('graduation_year')
        self.university = kwargs.get('university', '').strip()
        self.department = kwargs.get('department', '').strip()
        self.status = kwargs.get('status', 'active')
        self.join_date = kwargs.get('join_date', datetime.now())
        self.custom_fields = kwargs.get('custom_fields', {})
        self.notes = kwargs.get('notes', '')
        self.events = kwargs.get('events', [])
        self.created_by = kwargs.get('created_by')
        self.updated_by = kwargs.get('updated_by')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def validate(self) -> Dict[str, Any]:
        """Üye verilerini doğrula"""
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
        
        # Email kontrolü
        if not self.email:
            errors.append('Email adresi zorunludur')
        elif not self._validate_email():
            errors.append('Geçerli bir email adresi girin')
        
        # Mezuniyet yılı kontrolü
        if not self.graduation_year:
            errors.append('Mezuniyet yılı zorunludur')
        elif self.graduation_year < 1990:
            errors.append('Mezuniyet yılı 1990\'dan küçük olamaz')
        elif self.graduation_year > datetime.now().year:
            errors.append('Mezuniyet yılı gelecekte olamaz')
        
        # Üniversite kontrolü
        if not self.university or len(self.university.strip()) == 0:
            errors.append('Üniversite adı zorunludur')
        elif len(self.university) > 200:
            errors.append('Üniversite adı maksimum 200 karakter olabilir')
        
        # Bölüm kontrolü
        if not self.department or len(self.department.strip()) == 0:
            errors.append('Bölüm adı zorunludur')
        elif len(self.department) > 200:
            errors.append('Bölüm adı maksimum 200 karakter olabilir')
        
        # Durum kontrolü
        valid_statuses = ['active', 'inactive']
        if self.status not in valid_statuses:
            errors.append(f'Geçersiz durum. Geçerli durumlar: {", ".join(valid_statuses)}')
        
        # Notlar kontrolü
        if self.notes and len(self.notes) > 1000:
            errors.append('Notlar maksimum 1000 karakter olabilir')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def _validate_phone(self) -> bool:
        """Telefon numarası formatını kontrol et"""
        pattern = r'^(\+90|0)?5\d{9}$'
        return bool(re.match(pattern, self.phone))
    
    def _validate_email(self) -> bool:
        """Email formatını kontrol et"""
        pattern = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
        return bool(re.match(pattern, self.email))
    
    @property
    def event_count(self) -> int:
        """Toplam etkinlik sayısı"""
        return len(self.events) if self.events else 0
    
    @property
    def attended_event_count(self) -> int:
        """Katıldığı etkinlik sayısı"""
        if not self.events:
            return 0
        return len([e for e in self.events if e.get('status') == 'attended'])
    
    def add_event(self, event_id: int, status: str = 'registered') -> bool:
        """Üyeye etkinlik ekle"""
        if not self.events:
            self.events = []
        
        # Aynı etkinlik zaten ekli mi kontrol et
        for event in self.events:
            if event.get('event_id') == event_id:
                return False
        
        self.events.append({
            'event_id': event_id,
            'attendance_date': datetime.now(),
            'status': status
        })
        
        self.updated_at = datetime.now()
        return True
    
    def update_event_status(self, event_id: int, status: str) -> bool:
        """Etkinlik durumunu güncelle"""
        if not self.events:
            return False
        
        valid_statuses = ['attended', 'registered', 'cancelled']
        if status not in valid_statuses:
            return False
        
        for event in self.events:
            if event.get('event_id') == event_id:
                event['status'] = status
                event['attendance_date'] = datetime.now()
                self.updated_at = datetime.now()
                return True
        
        return False
    
    def remove_event(self, event_id: int) -> bool:
        """Üyeden etkinlik kaldır"""
        if not self.events:
            return False
        
        original_length = len(self.events)
        self.events = [e for e in self.events if e.get('event_id') != event_id]
        
        if len(self.events) < original_length:
            self.updated_at = datetime.now()
            return True
        
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Üyeyi dictionary'ye çevir"""
        return {
            'id': self.id,
            'photo': self.photo,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'graduation_year': self.graduation_year,
            'university': self.university,
            'department': self.department,
            'status': self.status,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'custom_fields': self.custom_fields,
            'notes': self.notes,
            'events': self.events,
            'event_count': self.event_count,
            'attended_event_count': self.attended_event_count,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __str__(self):
        return f"Member(id={self.id}, name='{self.name}', status='{self.status}')"
    
    def __repr__(self):
        return self.__str__()


class MemberManager:
    """Üye yönetimi için yardımcı sınıf"""
    
    def __init__(self):
        self.members = []
        self._next_id = 1
    
    def create_member(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni üye oluştur"""
        member_data['id'] = self._next_id
        member = Member(**member_data)
        
        validation = member.validate()
        if not validation['is_valid']:
            return {
                'success': False,
                'errors': validation['errors']
            }
        
        # Email benzersizlik kontrolü
        if self.get_member_by_email(member.email):
            return {
                'success': False,
                'errors': ['Bu email adresi zaten kullanılıyor']
            }
        
        # Telefon benzersizlik kontrolü
        if self.get_member_by_phone(member.phone):
            return {
                'success': False,
                'errors': ['Bu telefon numarası zaten kullanılıyor']
            }
        
        self.members.append(member)
        self._next_id += 1
        
        return {
            'success': True,
            'member': member.to_dict()
        }
    
    def get_member_by_id(self, member_id: int) -> Optional[Member]:
        """ID'ye göre üye bul"""
        for member in self.members:
            if member.id == member_id and member.status == 'active':
                return member
        return None
    
    def get_member_by_email(self, email: str) -> Optional[Member]:
        """Email'e göre üye bul"""
        for member in self.members:
            if member.email.lower() == email.lower() and member.status == 'active':
                return member
        return None
    
    def get_member_by_phone(self, phone: str) -> Optional[Member]:
        """Telefon numarasına göre üye bul"""
        for member in self.members:
            if member.phone == phone and member.status == 'active':
                return member
        return None
    
    def get_all_members(self, status: str = 'active') -> List[Dict[str, Any]]:
        """Tüm üyeleri getir"""
        filtered_members = [member for member in self.members if member.status == status]
        return [member.to_dict() for member in filtered_members]
    
    def search_members(self, query: str) -> List[Dict[str, Any]]:
        """Üye ara (ad, email, telefon)"""
        query = query.lower().strip()
        results = []
        
        for member in self.members:
            if member.status != 'active':
                continue
            
            if (query in member.name.lower() or 
                query in member.email.lower() or 
                query in member.phone or
                query in member.university.lower() or
                query in member.department.lower()):
                results.append(member.to_dict())
        
        return results
    
    def update_member(self, member_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Üye bilgilerini güncelle"""
        member = self.get_member_by_id(member_id)
        if not member:
            return {
                'success': False,
                'errors': ['Üye bulunamadı']
            }
        
        # Güncellenebilir alanları güncelle
        updatable_fields = [
            'photo', 'name', 'phone', 'email', 'graduation_year', 
            'university', 'department', 'status', 'custom_fields', 
            'notes', 'updated_by'
        ]
        
        for field in updatable_fields:
            if field in update_data:
                setattr(member, field, update_data[field])
        
        member.updated_at = datetime.now()
        
        validation = member.validate()
        if not validation['is_valid']:
            return {
                'success': False,
                'errors': validation['errors']
            }
        
        return {
            'success': True,
            'member': member.to_dict()
        }
    
    def delete_member(self, member_id: int) -> Dict[str, Any]:
        """Üyeyi sil (soft delete)"""
        member = self.get_member_by_id(member_id)
        if not member:
            return {
                'success': False,
                'errors': ['Üye bulunamadı']
            }
        
        member.status = 'inactive'
        member.updated_at = datetime.now()
        
        return {
            'success': True,
            'message': 'Üye başarıyla silindi'
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Üye istatistikleri"""
        active_members = [m for m in self.members if m.status == 'active']
        
        # Mezuniyet yılı dağılımı
        graduation_years = {}
        for member in active_members:
            year = member.graduation_year
            graduation_years[year] = graduation_years.get(year, 0) + 1
        
        # Üniversite dağılımı
        universities = {}
        for member in active_members:
            uni = member.university
            universities[uni] = universities.get(uni, 0) + 1
        
        return {
            'total_members': len(active_members),
            'inactive_members': len([m for m in self.members if m.status == 'inactive']),
            'graduation_year_distribution': graduation_years,
            'university_distribution': universities,
            'recent_members': [
                m.to_dict() for m in sorted(
                    active_members, 
                    key=lambda x: x.join_date, 
                    reverse=True
                )[:5]
            ]
        }


# Global üye yöneticisi
member_manager = MemberManager()
