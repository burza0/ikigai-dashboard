# -*- coding: utf-8 -*-
"""
IKIGAI Dashboard - API Module Init
Wersja: 2.0.0
Inicjalizacja modułowej architektury z blueprintami
"""

import sys
import os

# Dodaj ścieżkę do głównego backend
sys.path.append(os.path.dirname(__file__))

# Import blueprintów z poprawkami ścieżek
from .zawodnicy import zawodnicy_bp
from .qr_generation import qr_generation_bp
from .centrum_startu import centrum_startu_bp
# 🆕 IKIGAI: Nowe blueprinty
from .orders import orders_bp
from .products import products_bp

def init_app(app):
    """
    Rejestruje wszystkie blueprinty w aplikacji Flask
    """
    print("🔗 Rejestruję blueprinty IKIGAI...")
    
    # Rejestruj blueprinty
    app.register_blueprint(zawodnicy_bp)
    app.register_blueprint(qr_generation_bp)
    app.register_blueprint(centrum_startu_bp)
    # 🆕 NOWE: IKIGAI blueprinty
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)
    
    # Endpoint główny wersji
    @app.route('/api/version', methods=['GET'])
    def get_version():
        """Informacje o wersji i architekturze"""
        return {
            "success": True,
            "data": {
                "name": "IKIGAI Dashboard Backend",
                "version": "2.0.0",
                "architecture": "Modular IKIGAI Architecture",
                "description": "QR Order System for healthy vending machines",
                "modules": [
                    "zawodnicy_bp - User Management (to be transformed)", 
                    "qr_generation_bp - QR Generation (to be transformed)",
                    "centrum_startu_bp - Vending Machine Management (to be transformed)",
                    "🆕 orders_bp - IKIGAI Order System with QR Codes",
                    "🆕 products_bp - IKIGAI Product Catalog & Vending Machines"
                ],
                "features": [
                    "📱 Order Composition in Mobile App",
                    "🎯 QR Code Generation for Orders", 
                    "📱 QR Scanning in Vending Machines",
                    "🚀 Automatic Order Preparation",
                    "📊 Real-time Order Status Tracking",
                    "🛍️ Product Catalog with Nutrition Info",
                    "🏪 Vending Machine Locations & Status",
                    "🌱 Dietary Labels & Filtering"
                ],
                "data_source": "In-Memory Demo + Order Database",
                "build_date": "2025-06-10",
                "transformation": "SKATECROSS → IKIGAI"
            }
        }
    
    print("✅ Blueprinty IKIGAI zarejestrowane:")
    print("   👤 zawodnicy_bp - /api/zawodnicy/* (→ users)")
    print("   🔲 qr_generation_bp - /api/qr/* (legacy)") 
    print("   🏁 centrum_startu_bp - /api/grupy-startowe, /api/scan-qr (legacy)")
    print("   🛒 orders_bp - /api/orders/* (IKIGAI QR Orders)")
    print("   🛍️ products_bp - /api/products/*, /api/vending-machines/* (IKIGAI Catalog)")
    print("   ℹ️ version endpoint - /api/version")
    
    return app

print("📦 IKIGAI Dashboard - API Module Init loaded") 