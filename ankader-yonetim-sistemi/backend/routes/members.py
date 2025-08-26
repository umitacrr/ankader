#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Members Routes - Üye yönetimi route'ları
"""

from flask import Blueprint, request, jsonify, g
from models import member_manager, activity_log_manager
from middleware import auth_required, permission_required, log_activity

members_bp = Blueprint('members', __name__)

@members_bp.route('', methods=['GET'])
@auth_required
@permission_required('members', 'read')
def get_members():
    """Tüm üyeleri getir"""
    try:
        status = request.args.get('status', 'active')
        search = request.args.get('search', '').strip()
        
        if search:
            members = member_manager.search_members(search)
        else:
            members = member_manager.get_all_members(status)
        
        return jsonify({
            'success': True,
            'members': members,
            'total': len(members)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/<int:member_id>', methods=['GET'])
@auth_required
@permission_required('members', 'read')
def get_member(member_id):
    """Belirli bir üyeyi getir"""
    try:
        member = member_manager.get_member_by_id(member_id)
        
        if not member:
            return jsonify({
                'success': False,
                'message': 'Üye bulunamadı'
            }), 404
        
        return jsonify({
            'success': True,
            'member': member.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('', methods=['POST'])
@auth_required
@permission_required('members', 'write')
@log_activity('member_create', 'Yeni üye oluşturuldu')
def create_member():
    """Yeni üye oluştur"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        # Oluşturan kullanıcı bilgisini ekle
        data['created_by'] = g.user.id
        
        result = member_manager.create_member(data)
        
        if not result['success']:
            return jsonify(result), 400
        
        # Aktivite logla
        member = result['member']
        activity_log_manager.log_member_create(
            user_id=g.user.id,
            member_id=member['id'],
            member_name=member['name']
        )
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/<int:member_id>', methods=['PUT'])
@auth_required
@permission_required('members', 'write')
@log_activity('member_update', 'Üye bilgileri güncellendi')
def update_member(member_id):
    """Üye bilgilerini güncelle"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        # Güncelleyen kullanıcı bilgisini ekle
        data['updated_by'] = g.user.id
        
        result = member_manager.update_member(member_id, data)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/<int:member_id>', methods=['DELETE'])
@auth_required
@permission_required('members', 'delete')
@log_activity('member_delete', 'Üye silindi')
def delete_member(member_id):
    """Üyeyi sil"""
    try:
        member = member_manager.get_member_by_id(member_id)
        if not member:
            return jsonify({
                'success': False,
                'message': 'Üye bulunamadı'
            }), 404
        
        result = member_manager.delete_member(member_id)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/statistics', methods=['GET'])
@auth_required
@permission_required('members', 'read')
def get_member_statistics():
    """Üye istatistikleri"""
    try:
        stats = member_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/search', methods=['GET'])
@auth_required
@permission_required('members', 'read')
def search_members():
    """Üye ara"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Arama terimi gerekli'
            }), 400
        
        results = member_manager.search_members(query)
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/<int:member_id>/events', methods=['GET'])
@auth_required
@permission_required('members', 'read')
def get_member_events(member_id):
    """Üyenin etkinliklerini getir"""
    try:
        member = member_manager.get_member_by_id(member_id)
        
        if not member:
            return jsonify({
                'success': False,
                'message': 'Üye bulunamadı'
            }), 404
        
        return jsonify({
            'success': True,
            'member_id': member_id,
            'events': member.events,
            'event_count': member.event_count,
            'attended_count': member.attended_event_count
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/<int:member_id>/events/<int:event_id>', methods=['POST'])
@auth_required
@permission_required('members', 'write')
def add_member_to_event(member_id, event_id):
    """Üyeyi etkinliğe ekle"""
    try:
        member = member_manager.get_member_by_id(member_id)
        
        if not member:
            return jsonify({
                'success': False,
                'message': 'Üye bulunamadı'
            }), 404
        
        data = request.get_json() or {}
        status = data.get('status', 'registered')
        
        success = member.add_event(event_id, status)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Üye zaten bu etkinliğe kayıtlı'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Üye etkinliğe başarıyla eklendi'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/<int:member_id>/events/<int:event_id>', methods=['PUT'])
@auth_required
@permission_required('members', 'write')
def update_member_event_status(member_id, event_id):
    """Üyenin etkinlik durumunu güncelle"""
    try:
        member = member_manager.get_member_by_id(member_id)
        
        if not member:
            return jsonify({
                'success': False,
                'message': 'Üye bulunamadı'
            }), 404
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'message': 'Durum bilgisi gerekli'
            }), 400
        
        status = data['status']
        success = member.update_event_status(event_id, status)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Etkinlik durumu güncellenemedi'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Etkinlik durumu güncellendi'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@members_bp.route('/<int:member_id>/events/<int:event_id>', methods=['DELETE'])
@auth_required
@permission_required('members', 'delete')
def remove_member_from_event(member_id, event_id):
    """Üyeyi etkinlikten kaldır"""
    try:
        member = member_manager.get_member_by_id(member_id)
        
        if not member:
            return jsonify({
                'success': False,
                'message': 'Üye bulunamadı'
            }), 404
        
        success = member.remove_event(event_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': 'Üye bu etkinliğe kayıtlı değil'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Üye etkinlikten kaldırıldı'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500
