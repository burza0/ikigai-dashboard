#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS

print("🎯 IKIGAI Analytics Server - Uruchamianie...")

# Tworzymy aplikację Flask
app = Flask(__name__)
CORS(app)

print("📊 IKIGAI Analytics Server v2.0 - Ready!")
print("🌐 Endpoints dostępne na http://localhost:5001")
print("📈 Analytics Dashboard: /api/analytics/*")
print("🎨 UX Enhancements: /api/suggestions/*, /api/favorites/*")

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
    context = data.get('context', 'breakfast')
    
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
            }
        ]
    }
    
    return jsonify({
        "status": "success",
        "data": favorites
    })

# Health check endpoint
@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "IKIGAI Analytics Server działa poprawnie",
        "endpoints": {
            "analytics": "/api/analytics/dashboard",
            "charts": "/api/analytics/charts/sales",
            "ingredients": "/api/analytics/ingredients/usage",
            "funnel": "/api/analytics/funnel",
            "realtime": "/api/analytics/realtime",
            "suggestions": "/api/suggestions/smart",
            "favorites": "/api/favorites"
        }
    })

if __name__ == '__main__':
    print("🚀 Uruchamiam IKIGAI Analytics Server...")
    app.run(host='0.0.0.0', port=5001, debug=True) 