#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Routes Package
"""

from .auth import auth_bp
from .members import members_bp
from .events import events_bp
from .admin import admin_bp

__all__ = ['auth_bp', 'members_bp', 'events_bp', 'admin_bp']
