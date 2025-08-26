#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin Routes - Yönetici route'ları
"""

from flask import Blueprint, request, jsonify, g
from models import user_manager, member_manager, event_manager, activity_log_manager
from middleware import auth_required, admin_required, acar_required, log_activity
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@auth_required
@admin_required
def get_dashboard():
    """Admin dashboard verilerini getir"""
    try:
        # Genel istatistikler
        member_stats = member_manager.get_statistics()
        event_stats = event_manager.get_statistics()
        activity_stats = activity_log_manager.get_statistics()
        
        # Son aktiviteler
        recent_activities = activity_log_manager.get_recent_logs(limit=20)
        
        dashboard_data = {
            'overview': {
                'total_members': member_stats['total_members'],
                'total_events': event_stats['total_events'],
                'upcoming_events': event_stats['upcoming_events'],
                'total_activities': activity_stats['total_logs']
            },
            'member_statistics': member_stats,
            'event_statistics': event_stats,
            'activity_statistics': activity_stats,
            'recent_activities': recent_activities
        }
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/users', methods=['GET'])
@auth_required
@acar_required
def get_users():
    """Tüm kullanıcıları getir (sadece ACAR)"""
    try:
        users = user_manager.get_all_users()
        
        return jsonify({
            'success': True,
            'users': users,
            'total': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/users', methods=['POST'])
@auth_required
@acar_required
@log_activity('admin_user_create', 'Yeni kullanıcı oluşturuldu')
def create_user():
    """Yeni kullanıcı oluştur (sadece ACAR)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        # Oluşturan kullanıcı bilgisini ekle
        data['created_by'] = g.user.id
        
        result = user_manager.create_user(data)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@auth_required
@acar_required
@log_activity('admin_user_update', 'Kullanıcı güncellendi')
def update_user(user_id):
    """Kullanıcı güncelle (sadece ACAR)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz JSON'
            }), 400
        
        result = user_manager.update_user(user_id, data)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@auth_required
@acar_required
@log_activity('admin_user_delete', 'Kullanıcı silindi')
def delete_user(user_id):
    """Kullanıcı sil (sadece ACAR)"""
    try:
        result = user_manager.delete_user(user_id)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/activity-logs', methods=['GET'])
@auth_required
@admin_required
def get_activity_logs():
    """Aktivite loglarını getir"""
    try:
        limit = int(request.args.get('limit', 50))
        user_id = request.args.get('user_id')
        action = request.args.get('action')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if user_id:
            logs = activity_log_manager.get_logs_by_user(int(user_id), limit)
        elif action:
            logs = activity_log_manager.get_logs_by_action(action, limit)
        elif start_date and end_date:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            logs = activity_log_manager.get_logs_in_date_range(start_dt, end_dt)
        else:
            logs = activity_log_manager.get_recent_logs(limit)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'total': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/activity-logs/search', methods=['GET'])
@auth_required
@admin_required
def search_activity_logs():
    """Aktivite loglarında ara"""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 50))
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Arama terimi gerekli'
            }), 400
        
        logs = activity_log_manager.search_logs(query, limit)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'total': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/activity-logs/cleanup', methods=['POST'])
@auth_required
@acar_required
@log_activity('admin_logs_cleanup', 'Aktivite logları temizlendi')
def cleanup_activity_logs():
    """Eski aktivite loglarını temizle (sadece ACAR)"""
    try:
        data = request.get_json() or {}
        days = data.get('days', 180)  # Varsayılan 6 ay
        
        if days < 30:
            return jsonify({
                'success': False,
                'message': 'En az 30 günlük log tutulmalıdır'
            }), 400
        
        old_count = len(activity_log_manager.logs)
        activity_log_manager.cleanup_logs_older_than(days)
        new_count = len(activity_log_manager.logs)
        
        deleted_count = old_count - new_count
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} eski log temizlendi',
            'deleted_count': deleted_count,
            'remaining_count': new_count
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/system-info', methods=['GET'])
@auth_required
@admin_required
def get_system_info():
    """Sistem bilgileri"""
    try:
        import sys
        import platform
        from datetime import datetime
        
        system_info = {
            'python_version': sys.version,
            'platform': platform.platform(),
            'system': platform.system(),
            'architecture': platform.architecture(),
            'server_time': datetime.now().isoformat(),
            'uptime': 'N/A',  # Basit backend için
            'memory_usage': 'N/A',  # Basit backend için
            'database': 'In-Memory (Bellekte)',
            'framework': 'Python Flask',
            'version': '1.0.0'
        }
        
        # Uygulama istatistikleri
        app_stats = {
            'total_users': len(user_manager.users),
            'active_users': len([u for u in user_manager.users if u.is_active]),
            'total_members': len(member_manager.members),
            'active_members': len([m for m in member_manager.members if m.status == 'active']),
            'total_events': len(event_manager.events),
            'total_logs': len(activity_log_manager.logs)
        }
        
        return jsonify({
            'success': True,
            'system_info': system_info,
            'app_statistics': app_stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/backup', methods=['POST'])
@auth_required
@acar_required
@log_activity('admin_backup', 'Sistem yedeği oluşturuldu')
def create_backup():
    """Sistem yedeği oluştur (sadece ACAR)"""
    try:
        import json
        from datetime import datetime
        
        # Tüm veriyi topla
        backup_data = {
            'backup_date': datetime.now().isoformat(),
            'version': '1.0.0',
            'users': [user.to_dict(include_password=True) for user in user_manager.users],
            'members': [member.to_dict() for member in member_manager.members],
            'events': [event.to_dict() for event in event_manager.events],
            'activity_logs': [log.to_dict() for log in activity_log_manager.logs]
        }
        
        # JSON formatında döndür (gerçek uygulamada dosyaya kaydedilir)
        return jsonify({
            'success': True,
            'message': 'Yedek başarıyla oluşturuldu',
            'backup_data': backup_data,
            'total_users': len(backup_data['users']),
            'total_members': len(backup_data['members']),
            'total_events': len(backup_data['events']),
            'total_logs': len(backup_data['activity_logs'])
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/restore', methods=['POST'])
@auth_required
@acar_required
@log_activity('admin_restore', 'Sistem geri yüklendi')
def restore_backup():
    """Sistem yedeğini geri yükle (sadece ACAR)"""
    try:
        data = request.get_json()
        
        if not data or 'backup_data' not in data:
            return jsonify({
                'success': False,
                'message': 'Geçersiz yedek verisi'
            }), 400
        
        backup_data = data['backup_data']
        
        # Mevcut verileri temizle
        user_manager.users = []
        member_manager.members = []
        event_manager.events = []
        activity_log_manager.logs = []
        
        # Kullanıcıları geri yükle
        if 'users' in backup_data:
            for user_data in backup_data['users']:
                user = user_manager.User(**user_data)
                user_manager.users.append(user)
            user_manager._next_id = max([u.id for u in user_manager.users], default=0) + 1
        
        # Üyeleri geri yükle
        if 'members' in backup_data:
            for member_data in backup_data['members']:
                member = member_manager.Member(**member_data)
                member_manager.members.append(member)
            member_manager._next_id = max([m.id for m in member_manager.members], default=0) + 1
        
        # Etkinlikleri geri yükle
        if 'events' in backup_data:
            for event_data in backup_data['events']:
                event = event_manager.Event(**event_data)
                event_manager.events.append(event)
            event_manager._next_id = max([e.id for e in event_manager.events], default=0) + 1
        
        # Logları geri yükle
        if 'activity_logs' in backup_data:
            for log_data in backup_data['activity_logs']:
                log = activity_log_manager.ActivityLog(**log_data)
                activity_log_manager.logs.append(log)
            activity_log_manager._next_id = max([l.id for l in activity_log_manager.logs], default=0) + 1
        
        return jsonify({
            'success': True,
            'message': 'Sistem başarıyla geri yüklendi',
            'restored_users': len(user_manager.users),
            'restored_members': len(member_manager.members),
            'restored_events': len(event_manager.events),
            'restored_logs': len(activity_log_manager.logs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500

@admin_bp.route('/reports/monthly', methods=['GET'])
@auth_required
@admin_required
def get_monthly_report():
    """Aylık rapor"""
    try:
        from collections import defaultdict
        
        # Son 12 ayın verisini al
        now = datetime.now()
        monthly_data = defaultdict(lambda: {
            'new_members': 0,
            'new_events': 0,
            'login_count': 0
        })
        
        # Üye istatistikleri
        for member in member_manager.members:
            if member.join_date:
                month_key = member.join_date.strftime('%Y-%m')
                monthly_data[month_key]['new_members'] += 1
        
        # Etkinlik istatistikleri
        for event in event_manager.events:
            if event.created_at:
                month_key = event.created_at.strftime('%Y-%m')
                monthly_data[month_key]['new_events'] += 1
        
        # Giriş istatistikleri
        for log in activity_log_manager.logs:
            if log.action == 'login' and log.created_at:
                month_key = log.created_at.strftime('%Y-%m')
                monthly_data[month_key]['login_count'] += 1
        
        # Son 12 ayı formatla
        months = []
        for i in range(12):
            date = now.replace(day=1) - timedelta(days=32*i)
            month_key = date.strftime('%Y-%m')
            months.append({
                'month': month_key,
                'month_name': date.strftime('%B %Y'),
                **monthly_data[month_key]
            })
        
        months.reverse()
        
        return jsonify({
            'success': True,
            'monthly_report': months
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Sunucu hatası: {str(e)}'
        }), 500
