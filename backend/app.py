from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# Import modułów 
import orders
import products  
import zawodnicy
import qr_generation
import centrum_startu

print("🎯 Ładuję IKIGAI Modules...")
print("🛒 orders.py - QR Orders Workflow")
print("🛍️ products.py - Product Catalog & Vending Machines")
print("👤 zawodnicy.py - Users (legacy)")
print("🔲 qr_generation.py - QR Legacy")
print("🏁 centrum_startu.py - Legacy")

# Tworzymy aplikację Flask
app = Flask(__name__)
CORS(app)

# Import blueprintów
from orders import orders_bp
from products import products_bp, ingredients_bp
from loyalty import loyalty_bp

# Logging dla debugowania
import logging
logging.basicConfig(level=logging.DEBUG)

# Pozostałe blueprinty legacy
from zawodnicy import zawodnicy_bp
from qr_generation import qr_generation_bp
from centrum_startu import centrum_startu_bp

print("📦 IKIGAI Dashboard - API Module Init loaded")
print("✅ orders_bp imported")
print("✅ products_bp imported") 
print("✅ ingredients_bp imported")
print("✅ loyalty_bp imported")

print("🎯 IKIGAI Dashboard - Healthy Vending Machines")
print("🔗 Rejestruję blueprinty...")

# Rejestracja blueprintów
app.register_blueprint(orders_bp)
app.register_blueprint(products_bp)
app.register_blueprint(ingredients_bp)
app.register_blueprint(loyalty_bp)

# Legacy blueprinty  
app.register_blueprint(zawodnicy_bp)
app.register_blueprint(qr_generation_bp)
app.register_blueprint(centrum_startu_bp)

print("✅ orders_bp registered")
print("✅ products_bp registered")
print("✅ ingredients_bp registered") 
print("✅ loyalty_bp registered")

print("🚀 Uruchamiam IKIGAI Backend v2.0.0")
print("🛒 orders_bp - /api/orders/* (QR Order Workflow)")
print("🛍️ products_bp - /api/products/*, /api/vending-machines/*")
print("👤 zawodnicy_bp - /api/zawodnicy/* (legacy)")
print("🔲 qr_generation_bp - /api/qr/* (legacy)")
print("🏁 centrum_startu_bp - /api/grupy-startowe/* (legacy)")
print("📊 Demo: 6 produktów + 3 automaty + kompletny QR workflow")
print("🌐 Serwer dostępny na http://localhost:5001")
print("🎯 WORKFLOW: Kompozycja → QR → Skanowanie → Przygotowanie")
print("🌱 Filozofia IKIGAI: Zdrowe wybory łatwo dostępne")
print("=" * 72)

# Analytics API endpoints
@app.route('/api/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Główne statystyki dashboard"""
    return jsonify({
        "status": "success",
        "data": {
            "sales": {
                "today": 2847.50,
                "yesterday": 2156.30,
                "this_week": 18542.80,
                "last_week": 16234.20,
                "this_month": 78549.60,
                "last_month": 72348.90,
                "growth_daily": 32.1,
                "growth_weekly": 14.2,
                "growth_monthly": 8.6
            },
            "orders": {
                "total": 1247,
                "today": 89,
                "completed": 1198,
                "pending": 49,
                "completion_rate": 96.1,
                "avg_preparation_time": 4.2
            },
            "machines": {
                "total": 5,
                "online": 5,
                "offline": 0,
                "uptime": 98.7,
                "maintenance_due": 1
            },
            "ingredients": {
                "total_usage": 2847,
                "top_ingredient": "Spirulina Powder BIO",
                "low_stock": 3
            }
        }
    })

@app.route('/api/analytics/charts/sales', methods=['GET'])
def get_sales_charts():
    """Dane dla wykresów sprzedaży"""
    return jsonify({
        "status": "success",
        "data": {
            "daily_sales": [
                {"date": "2024-06-05", "sales": 2156.30},
                {"date": "2024-06-06", "sales": 2398.70},
                {"date": "2024-06-07", "sales": 2687.90},
                {"date": "2024-06-08", "sales": 2234.50},
                {"date": "2024-06-09", "sales": 2756.80},
                {"date": "2024-06-10", "sales": 2445.60},
                {"date": "2024-06-11", "sales": 2847.50}
            ],
            "hourly_today": [
                {"hour": "06:00", "orders": 12},
                {"hour": "07:00", "orders": 18},
                {"hour": "08:00", "orders": 24},
                {"hour": "09:00", "orders": 15},
                {"hour": "10:00", "orders": 8},
                {"hour": "11:00", "orders": 6},
                {"hour": "12:00", "orders": 22},
                {"hour": "13:00", "orders": 19},
                {"hour": "14:00", "orders": 11}
            ]
        }
    })

@app.route('/api/analytics/ingredients/usage', methods=['GET'])
def get_ingredients_usage():
    """Usage tracking składników"""
    return jsonify({
        "status": "success", 
        "data": {
            "top_ingredients": [
                {"name": "Spirulina Powder BIO", "usage_count": 287, "trend": "+15%"},
                {"name": "Protein Vanilla Premium", "usage_count": 234, "trend": "+8%"},
                {"name": "Woda Kokosowa Premium", "usage_count": 198, "trend": "+22%"},
                {"name": "Matcha Premium Grade A", "usage_count": 176, "trend": "+5%"},
                {"name": "Goji Berries Organic", "usage_count": 145, "trend": "+12%"},
                {"name": "Chia Seeds Premium", "usage_count": 132, "trend": "+3%"}
            ]
        }
    })

@app.route('/api/analytics/funnel', methods=['GET'])
def get_sales_funnel():
    """Sales funnel analytics"""
    return jsonify({
        "status": "success",
        "data": {
            "funnel_steps": [
                {"step": "Wejście na stronę", "visitors": 12547, "conversion": 100.0},
                {"step": "Otworzenie kreatora", "visitors": 8234, "conversion": 65.6},
                {"step": "Wybór przepisu", "visitors": 6789, "conversion": 54.1},
                {"step": "Dodanie składników", "visitors": 4532, "conversion": 36.1},
                {"step": "Generowanie QR", "visitors": 2847, "conversion": 22.7},
                {"step": "Finalizacja zamówienia", "visitors": 2156, "conversion": 17.2}
            ]
        }
    })

@app.route('/api/analytics/realtime', methods=['GET'])
def get_realtime_analytics():
    """Real-time dane z auto-refresh"""
    return jsonify({
        "status": "success",
        "data": {
            "current_users": 47,
            "orders_last_hour": 12,
            "active_machines": 5,
            "avg_response_time": 0.8
        }
    })

# UX Enhancements API endpoints
@app.route('/api/suggestions/smart', methods=['POST'])
def get_smart_suggestions():
    """AI-powered smart suggestions na podstawie wybranych składników"""
    data = request.get_json()
    selected_ingredients = data.get('ingredients', [])
    context = data.get('context', 'breakfast')  # breakfast, lunch, dinner, snack
    
    # Smart suggestions logic
    suggestions = {
        "complementary_ingredients": [
            {
                "id": "spirulina_powder",
                "name": "Spirulina Powder BIO",
                "reason": "Doskonale komponuje się z proteinami",
                "confidence": 92,
                "price": 4.50
            },
            {
                "id": "chia_seeds",
                "name": "Chia Seeds Premium", 
                "reason": "Dodaje teksturę i omega-3",
                "confidence": 87,
                "price": 3.20
            },
            {
                "id": "coconut_water",
                "name": "Woda Kokosowa Premium",
                "reason": "Naturalne nawodnienie i elektrolity", 
                "confidence": 95,
                "price": 5.80
            }
        ],
        "similar_recipes": [
            {
                "id": "energetic_morning",
                "name": "Energetyczny Start Dnia",
                "similarity": 89,
                "health_score": 94,
                "price": 16.60
            },
            {
                "id": "protein_power",
                "name": "Power Protein Bowl",
                "similarity": 76,
                "health_score": 91,
                "price": 18.30
            }
        ],
        "ai_tips": [
            "💡 Dodaj spirulinę dla dodatkowych witamin B12",
            "🌱 Chia seeds zwiększą zawartość błonnika", 
            "⚡ Ta kombinacja zapewni energię na 4-5 godzin"
        ]
    }
    
    return jsonify({
        "status": "success",
        "data": suggestions
    })

@app.route('/api/favorites', methods=['GET'])
def get_user_favorites():
    """Pobierz ulubione przepisy i składniki użytkownika"""
    user_id = request.args.get('user_id', 'web_user')
    
    favorites = {
        "recipes": [
            {
                "id": "energetic_morning",
                "name": "Energetyczny Start Dnia",
                "category": "breakfast",
                "price": 16.60,
                "health_score": 94,
                "last_ordered": "2024-06-10",
                "order_count": 12
            },
            {
                "id": "detox_green", 
                "name": "Detox Green Morning",
                "category": "breakfast",
                "price": 21.00,
                "health_score": 98,
                "last_ordered": "2024-06-09",
                "order_count": 8
            },
            {
                "id": "power_protein",
                "name": "Power Protein Bowl",
                "category": "lunch", 
                "price": 18.30,
                "health_score": 91,
                "last_ordered": "2024-06-08",
                "order_count": 5
            }
        ],
        "ingredients": [
            {
                "id": "spirulina_powder",
                "name": "Spirulina Powder BIO",
                "category": "superfoods",
                "price": 4.50,
                "usage_count": 18
            },
            {
                "id": "matcha_premium",
                "name": "Matcha Premium Grade A", 
                "category": "traditional",
                "price": 6.20,
                "usage_count": 14
            },
            {
                "id": "coconut_water",
                "name": "Woda Kokosowa Premium",
                "category": "liquid_cup",
                "price": 5.80,
                "usage_count": 22
            }
        ],
        "categories": [
            {"name": "breakfast", "count": 2},
            {"name": "lunch", "count": 1},
            {"name": "superfoods", "count": 1},
            {"name": "traditional", "count": 1},
            {"name": "liquid_cup", "count": 1}
        ]
    }
    
    return jsonify({
        "status": "success",
        "data": favorites
    })

@app.route('/api/favorites', methods=['POST'])
def add_to_favorites():
    """Dodaj przepis lub składnik do ulubionych"""
    data = request.get_json()
    user_id = data.get('user_id', 'web_user')
    item_type = data.get('type')  # 'recipe' or 'ingredient'
    item_id = data.get('item_id')
    
    return jsonify({
        "status": "success",
        "message": f"{item_type.capitalize()} added to favorites",
        "data": {
            "user_id": user_id,
            "item_type": item_type,
            "item_id": item_id,
            "added_at": "2024-06-11T22:15:00Z"
        }
    })

@app.route('/api/favorites/<item_id>', methods=['DELETE'])
def remove_from_favorites(item_id):
    """Usuń z ulubionych"""
    user_id = request.args.get('user_id', 'web_user')
    
    return jsonify({
        "status": "success", 
        "message": "Item removed from favorites",
        "data": {
            "user_id": user_id,
            "item_id": item_id,
            "removed_at": "2024-06-11T22:15:00Z"
        }
    })

@app.route('/api/preferences', methods=['GET'])
def get_user_preferences():
    """Pobierz preferencje użytkownika"""
    user_id = request.args.get('user_id', 'web_user')
    
    preferences = {
        "dietary": {
            "vegan": True,
            "gluten_free": False,
            "high_protein": True,
            "low_carb": False,
            "organic_only": True
        },
        "allergies": [
            "nuts",
            "dairy"
        ],
        "goals": [
            "weight_loss",
            "energy_boost",
            "muscle_building"
        ],
        "price_range": {
            "min": 10.00,
            "max": 25.00
        },
        "favorite_time": "morning",
        "notification_preferences": {
            "new_recipes": True,
            "price_alerts": True,
            "health_tips": True
        }
    }
    
    return jsonify({
        "status": "success",
        "data": preferences
    })

@app.route('/api/preferences', methods=['POST'])
def update_user_preferences():
    """Aktualizuj preferencje użytkownika"""
    data = request.get_json()
    user_id = data.get('user_id', 'web_user')
    preferences = data.get('preferences', {})
    
    return jsonify({
        "status": "success",
        "message": "Preferences updated successfully",
        "data": {
            "user_id": user_id,
            "updated_at": "2024-06-11T22:15:00Z",
            "preferences": preferences
        }
    })

@app.route('/api/search/smart', methods=['POST'])
def smart_search():
    """Inteligentne wyszukiwanie z AI"""
    data = request.get_json()
    query = data.get('query', '')
    filters = data.get('filters', {})
    context = data.get('context', 'all')
    
    # Smart search results
    results = {
        "recipes": [
            {
                "id": "energetic_morning",
                "name": "Energetyczny Start Dnia",
                "category": "breakfast",
                "price": 16.60,
                "health_score": 94,
                "match_score": 95,
                "match_reasons": ["zawiera spirulinę", "idealny na śniadanie"]
            }
        ],
        "ingredients": [
            {
                "id": "spirulina_powder", 
                "name": "Spirulina Powder BIO",
                "category": "superfoods",
                "price": 4.50,
                "match_score": 98,
                "match_reasons": ["dokładne dopasowanie nazwy"]
            }
        ],
        "suggestions": [
            "Czy chodziło Ci o 'spirulina'?",
            "Sprawdź także: chlorella, matcha",
            "Popularne w kategorii: superfoods"
        ],
        "total_results": 12
    }
    
    return jsonify({
        "status": "success",
        "data": results,
        "query": query,
        "filters_applied": filters
    })

@app.route('/api/quick-actions', methods=['GET'])
def get_quick_actions():
    """Quick actions dla użytkownika"""
    user_id = request.args.get('user_id', 'web_user')
    
    actions = {
        "frequent_orders": [
            {
                "name": "Ulubione śniadanie",
                "recipe_id": "energetic_morning", 
                "icon": "☀️",
                "last_ordered": "2 dni temu"
            },
            {
                "name": "Detox wieczorny",
                "recipe_id": "detox_green",
                "icon": "🌱", 
                "last_ordered": "wczoraj"
            }
        ],
        "recommended_actions": [
            {
                "title": "Wypróbuj nowy przepis",
                "description": "Mamy 3 nowe przepisy w Twojej kategorii",
                "action": "view_new_recipes",
                "icon": "✨"
            },
            {
                "title": "Uzupełnij profil",
                "description": "Dodaj preferencje żywieniowe",
                "action": "edit_preferences", 
                "icon": "👤"
            }
        ],
        "shortcuts": [
            {"name": "Ostatnie zamówienie", "action": "repeat_last", "icon": "🔄"},
            {"name": "Random przepis", "action": "random_recipe", "icon": "🎲"},
            {"name": "Sprawdź ulubione", "action": "view_favorites", "icon": "⭐"}
        ]
    }
    
    return jsonify({
        "status": "success",
        "data": actions
    })

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "IKIGAI Backend działa poprawnie"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 