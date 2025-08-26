#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Events Routes - Etkinlik yönetimi route'ları
"""

from flask import Blueprint, request, jsonify, g
from models import event_manager, activity_log_manager
from middleware import auth_required, permission_required, log_activity
from datetime import datetime

events_bp = Blueprint('events', __name__)

@events_bp.route('', methods=['GET'])
@auth_required
@permission_required('events', 'read')
def get_events():
    """Tüm etkinlikleri getir"""
    try:
        status = request.args.get('status')
        event_type = request.args.get('type')
        upcoming = request.args.get('upcoming') == 'true'
        past = request.args.get('past') == 'true'
        search = request.args.get('search', '').strip()
        
        if search:
            events = event_manager.search_events(search)
        elif upcoming:
            events = event_manager.get_upcoming_events()
        elif past:
            events = event_manager.get_past_events()
        else:
            events = event_manager.get_all_events(status)
        
        # Tip filtresi
        if event_type:
            events = [e for e in events if e.get('type') == event_type]
        
        return jsonify({
            'success': True,
            'events': events,
            'total': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>', methods=['GET'])
@auth_required
@permission_required('events', 'read')
def get_event(event_id):
    """Belirli bir etkinliği getir"""
    try:
        event = event_manager.get_event_by_id(event_id)
        
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        return jsonify({
            'success': True,
            'event': event.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('', methods=['POST'])
@auth_required
@permission_required('events', 'write')
@log_activity('event_create', 'Yeni etkinlik oluşturuldu')
def create_event():
    """Yeni etkinlik oluştur"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        # Tarih string'ini datetime'a çevir
        if 'date' in data and isinstance(data['date'], str):
            try:
                data['date'] = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Geçersiz tarih formatı'
                }), 400
        
        # Oluşturan kullanıcı bilgilerini ekle
        data['created_by'] = g.user.id
        data['organizer'] = g.user.id
        
        result = event_manager.create_event(data)
        
        if not result['success']:
            return jsonify(result), 400
        
        # Aktivite logla
        event = result['event']
        activity_log_manager.log_event_create(
            user_id=g.user.id,
            event_id=event['id'],
            event_title=event['title']
        )
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>', methods=['PUT'])
@auth_required
@permission_required('events', 'write')
@log_activity('event_update', 'Etkinlik güncellendi')
def update_event(event_id):
    """Etkinlik bilgilerini güncelle"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        # Tarih string'ini datetime'a çevir
        if 'date' in data and isinstance(data['date'], str):
            try:
                data['date'] = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Geçersiz tarih formatı'
                }), 400
        
        # Güncelleyen kullanıcı bilgisini ekle
        data['updated_by'] = g.user.id
        
        result = event_manager.update_event(event_id, data)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>', methods=['DELETE'])
@auth_required
@permission_required('events', 'delete')
@log_activity('event_delete', 'Etkinlik silindi')
def delete_event(event_id):
    """Etkinliği sil"""
    try:
        event = event_manager.get_event_by_id(event_id)
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        result = event_manager.delete_event(event_id)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/statistics', methods=['GET'])
@auth_required
@permission_required('events', 'read')
def get_event_statistics():
    """Etkinlik istatistikleri"""
    try:
        stats = event_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/upcoming', methods=['GET'])
@auth_required
@permission_required('events', 'read')
def get_upcoming_events():
    """Gelecek etkinlikleri getir"""
    try:
        events = event_manager.get_upcoming_events()
        
        return jsonify({
            'success': True,
            'events': events,
            'total': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/past', methods=['GET'])
@auth_required
@permission_required('events', 'read')
def get_past_events():
    """Geçmiş etkinlikleri getir"""
    try:
        events = event_manager.get_past_events()
        
        return jsonify({
            'success': True,
            'events': events,
            'total': len(events)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/participants', methods=['GET'])
@auth_required
@permission_required('events', 'read')
def get_event_participants(event_id):
    """Etkinlik katılımcılarını getir"""
    try:
        event = event_manager.get_event_by_id(event_id)
        
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        return jsonify({
            'success': True,
            'event_id': event_id,
            'participants': event.participants,
            'participant_count': event.participant_count,
            'attended_count': event.attended_count
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/participants/<int:member_id>', methods=['POST'])
@auth_required
@permission_required('events', 'write')
def add_participant_to_event(event_id, member_id):
    """Etkinliğe katılımcı ekle"""
    try:
        event = event_manager.get_event_by_id(event_id)
        
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        data = request.get_json() or {}
        notes = data.get('notes', '')
        
        success = event.add_participant(member_id, notes)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Katılımcı eklenemedi (zaten kayıtlı veya kontenjan dolu)'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Katılımcı başarıyla eklendi'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/participants/<int:member_id>', methods=['PUT'])
@auth_required
@permission_required('events', 'write')
def update_participant_status(event_id, member_id):
    """Katılımcı durumunu güncelle"""
    try:
        event = event_manager.get_event_by_id(event_id)
        
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'message': 'Durum bilgisi gerekli'
            }), 400
        
        status = data['status']
        success = event.update_participant_status(member_id, status)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Katılımcı durumu güncellenemedi'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Katılımcı durumu güncellendi'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/participants/<int:member_id>', methods=['DELETE'])
@auth_required
@permission_required('events', 'delete')
def remove_participant_from_event(event_id, member_id):
    """Katılımcıyı etkinlikten kaldır"""
    try:
        event = event_manager.get_event_by_id(event_id)
        
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        success = event.remove_participant(member_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Katılımcı bu etkinliğe kayıtlı değil'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Katılımcı etkinlikten kaldırıldı'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/feedback', methods=['POST'])
@auth_required
@permission_required('events', 'write')
def add_event_feedback(event_id):
    """Etkinlik geri bildirimi ekle"""
    try:
        event = event_manager.get_event_by_id(event_id)
        
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        member_id = data.get('member_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not member_id or not rating:
            return jsonify({
                'success': False,
                'message': 'Üye ID ve puanlama gerekli'
            }), 400
        
        success = event.add_feedback(member_id, rating, comment)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Geri bildirim eklenemedi'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Geri bildirim başarıyla eklendi'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@events_bp.route('/<int:event_id>/feedback', methods=['GET'])
@auth_required
@permission_required('events', 'read')
def get_event_feedback(event_id):
    """Etkinlik geri bildirimlerini getir"""
    try:
        event = event_manager.get_event_by_id(event_id)
        
        if not event:
            return jsonify({
                'success': False,
                'message': 'Etkinlik bulunamadı'
            }), 404
        
        return jsonify({
            'success': True,
            'event_id': event_id,
            'feedback': event.feedback,
            'average_rating': event.average_rating,
            'feedback_count': len(event.feedback)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500
