#!/usr/bin/env python3
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import sqlite3
import hashlib
import os
import json
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
import uuid
import qrcode
import io
import base64
from datetime import datetime

print("🎯 IKIGAI Analytics Server - Uruchamianie...")

# Tworzymy aplikację Flask
app = Flask(__name__)
app.secret_key = 'ikigai-dev-secret-key-2024'

# Konfiguracja CORS z credentials support
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Database setup - try PostgreSQL first, fallback to SQLite
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    print("🐘 Wykryto PostgreSQL - używam bazy danych")
    DB_TYPE = 'postgresql'
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    DB_PATH = DATABASE_URL
    DB_AVAILABLE = True
else:
    print("🗃️ Używam lokalnej bazy SQLite")
    DB_TYPE = 'sqlite'
    DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')
    DB_AVAILABLE = os.path.exists(DB_PATH)

print("📊 IKIGAI Analytics Server v3.0 - Ready!")
print("🌐 Endpoints dostępne na http://localhost:5001")
print("📈 Analytics Dashboard: /api/analytics/*")
print("🎨 UX Enhancements: /api/suggestions/*, /api/favorites/*")
print("🍜 Meal Recipes: /api/meal-recipes*, /api/recommendations")
print("🗺️ Vending Machines: /api/vending-machines")
print("🧪 Ingredients: /api/ingredients/*") 
print("🏆 Loyalty Program: /api/loyalty/*")
print(f"🗄️ Database: {DB_TYPE} - {'✅' if DB_AVAILABLE else '❌'}")

@contextmanager
def get_db_connection():
    """Database connection context manager for both PostgreSQL and SQLite"""
    if not DB_AVAILABLE:
        yield None
        return
    
    conn = None
    try:
        if DB_TYPE == 'postgresql':
            conn = psycopg2.connect(DB_PATH)
            conn.cursor_factory = psycopg2.extras.RealDictCursor
            yield conn
        else:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            yield conn
    finally:
        if conn:
            conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400
    
    try:
        with get_db_connection() as conn:
            if not conn:
                return jsonify({'status': 'error', 'message': 'Database not available'}), 500
            
            user = conn.execute(
                'SELECT * FROM users WHERE (username = ? OR email = ?) AND is_active = 1',
                (username, username)
            ).fetchone()
            
            if user and user['password_hash'] == hash_password(password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                
                return jsonify({
                    'status': 'success',
                    'message': 'Logged in successfully',
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'name': user['name'],
                        'role': user['role'],
                        'loyalty_points': user['loyalty_points']
                    }
                })
            else:
                return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
                
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Login failed'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Get current user profile"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
    
    try:
        with get_db_connection() as conn:
            if not conn:
                return jsonify({'status': 'error', 'message': 'Database not available'}), 500
            
            user = conn.execute(
                'SELECT * FROM users WHERE id = ? AND is_active = 1',
                (session['user_id'],)
            ).fetchone()
            
            if user:
                return jsonify({
                    'status': 'success',
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'name': user['name'],
                        'role': user['role'],
                        'loyalty_points': user['loyalty_points'],
                        'total_orders': user['total_orders'],
                        'total_spent': user['total_spent']
                    }
                })
            else:
                session.clear()
                return jsonify({'status': 'error', 'message': 'User not found'}), 404
                
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Failed to get profile'}), 500

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

# MEAL RECIPES API endpoints - POBIERA Z BAZY DANYCH!
@app.route('/api/meal-recipes', methods=['GET'])
def get_meal_recipes():
    """Lista wszystkich przepisów na mieszanki z bazy danych"""
    try:
        # Try PostgreSQL first
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if DATABASE_URL:
            if DATABASE_URL.startswith('postgres://'):
                DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
            
            import psycopg2
            import psycopg2.extras
            
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("""
                SELECT id, name, category_id as category, description, 
                       calories, protein, carbs, price, health_score, prep_time
                FROM recipes 
                WHERE is_available = true
                ORDER BY id
            """)
            
            recipes_data = cursor.fetchall()
            conn.close()
            
            # Convert to frontend format
            recipes = []
            for recipe in recipes_data:
                # Parse JSON ingredients if it's a string
                ingredients = []  # PostgreSQL nie ma tej kolumny
                if isinstance(ingredients, str):
                    try:
                        ingredients = json.loads(ingredients)
                    except:
                        ingredients = []
                
                recipes.append({
                    "id": recipe['id'],
                    "name": recipe['name'],
                    "category": recipe['category'],
                    "description": recipe['description'],
                    "ingredients": ingredients,
                    "calories": recipe['calories'],
                    "protein": recipe['protein'],
                    "carbs": recipe['carbs'],
                    "price": float(recipe['price']) if recipe['price'] else 0,
                    "health_score": recipe['health_score'],
                    "prep_time": recipe['prep_time'],
                    "difficulty": "easy",
                    "tags": ["healthy", "fresh"]
                })
            
            print(f"✅ Pobrano {len(recipes)} przepisów z PostgreSQL"); print("Przepisy:", [r["name"] for r in recipes])
            return jsonify({
                "status": "success",
                "data": recipes
            })
        
        # Fallback to SQLite if no PostgreSQL
        else:
            with get_db_connection() as conn:
                if not conn:
                    return jsonify({"status": "error", "message": "Database not available"}), 500
                
                cursor = conn.execute("""
                    SELECT * FROM recipes WHERE is_available = 1 ORDER BY id
                """)
                recipes_data = cursor.fetchall()
                
                recipes = []
                for recipe in recipes_data:
                    # Parse JSON ingredients
                    ingredients = []  # PostgreSQL nie ma tej kolumny 
                    if isinstance(ingredients, str):
                        try:
                            ingredients = json.loads(ingredients)
                        except:
                            ingredients = []
                    
                    recipes.append({
                        "id": recipe['name'].lower().replace(' ', '_'),
                        "name": recipe['name'],
                        "category": recipe['category'],
                        "description": recipe['description'],
                        "ingredients": ingredients,
                        "calories": recipe['calories'],
                        "protein": recipe['protein'],
                        "carbs": 0,
                        "price": float(recipe['price']) if recipe['price'] else 0,
                        "health_score": recipe['health_score'],
                        "prep_time": recipe['prep_time'],
                        "difficulty": "easy",
                        "tags": ["healthy", "fresh"]
                    })
                
                print(f"✅ Pobrano {len(recipes)} przepisów z SQLite")
                return jsonify({
                    "status": "success",
                    "data": recipes
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania przepisów: {e}")
        # Fallback to static data if database fails
        return jsonify({
            "status": "success",
            "data": [
                {
                    "id": "energetic_morning",
                    "name": "Energetyczny Start Dnia",
                    "category": "breakfast",
                    "description": "Idealna mieszanka na poranną energię",
                    "ingredients": ["spirulina_powder", "protein_vanilla", "coconut_water", "chia_seeds"],
                    "calories": 320,
                    "protein": 25,
                    "carbs": 18,
                    "price": 16.60,
                    "health_score": 94,
                    "prep_time": 3,
                    "difficulty": "easy",
                    "tags": ["high-protein", "energizing", "superfood"]
                }
            ]
        })

@app.route('/api/meal-recipes/categories', methods=['GET'])
def get_meal_categories():
    """Kategorie przepisów"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": "breakfast",
                "name": "Śniadanie",
                "description": "Energetyczne poranki",
                "icon": "🌅",
                "color": "#ff6b35",
                "count": 1
            },
            {
                "id": "detox",
                "name": "Detox",
                "description": "Oczyszczanie organizmu",
                "icon": "🌿",
                "color": "#4ecdc4",
                "count": 1
            },
            {
                "id": "fitness",
                "name": "Fitness",
                "description": "Sport i siła",
                "icon": "💪",
                "color": "#ff6b6b",
                "count": 1
            },
            {
                "id": "cognitive",
                "name": "Koncentracja",
                "description": "Wsparcie mózgu",
                "icon": "🧠",
                "color": "#4ecdc4",
                "count": 1
            },
            {
                "id": "recovery",
                "name": "Regeneracja",
                "description": "Odpoczynek i odnowa",
                "icon": "🧘‍♀️",
                "color": "#a8e6cf",
                "count": 1
            }
        ]
    })

@app.route('/api/meal-recipes/<recipe_id>', methods=['GET'])
def get_meal_recipe_by_id(recipe_id):
    """Szczegóły pojedynczego przepisu"""
    recipes = {
        "energetic_morning": {
            "id": "energetic_morning",
            "name": "Energetyczny Start Dnia",
            "category": "breakfast",
            "description": "Idealna mieszanka na poranną energię z superpozywkami",
            "long_description": "Ta wyjątkowa mieszanka łączy moc spiruliny z wysokiej jakości białkiem i naturalnymi elektrolitami z wody kokosowej. Nasiona chia dodają omega-3 i błonnik.",
            "ingredients": [
                {
                    "id": "spirulina_powder",
                    "name": "Spirulina Powder BIO",
                    "amount": "5g",
                    "benefits": ["Witamina B12", "Żelazo", "Białko kompletne"]
                },
                {
                    "id": "protein_vanilla",
                    "name": "Protein Vanilla Premium",
                    "amount": "25g",
                    "benefits": ["Budowa mięśni", "Długotrwała sytość", "Aminokwasy"]
                },
                {
                    "id": "coconut_water",
                    "name": "Woda Kokosowa Premium",
                    "amount": "250ml",
                    "benefits": ["Elektrolity", "Nawodnienie", "Potas"]
                },
                {
                    "id": "chia_seeds",
                    "name": "Chia Seeds Premium",
                    "amount": "15g",
                    "benefits": ["Omega-3", "Błonnik", "Magnez"]
                }
            ],
            "nutrition": {
                "calories": 320,
                "protein": 25,
                "carbs": 18,
                "fat": 12,
                "fiber": 8,
                "sugar": 6
            },
            "health_score": 94,
            "prep_time": 3,
            "price": 16.60,
            "difficulty": "easy",
            "tags": ["high-protein", "energizing", "superfood"],
            "instructions": [
                "Dodaj spirulinę do shakera",
                "Wlej wodę kokosową",
                "Dodaj protein waniliowy",
                "Wsyp nasiona chia na koniec",
                "Potrząsaj przez 30 sekund"
            ],
            "tips": [
                "Najlepiej spożyć w ciągu 30 minut od przygotowania",
                "Możesz dodać kostki lodu dla lepszego smaku",
                "Idealne na śniadanie lub przekąskę przedtreningową"
            ]
        }
    }
    
    recipe = recipes.get(recipe_id)
    if not recipe:
        return jsonify({"status": "error", "message": "Przepis nie znaleziony"}), 404
    
    return jsonify({
        "status": "success",
        "data": recipe
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Rekomendacje przepisów i składników"""
    return jsonify({
        "status": "success",
        "data": {
            "featured_recipes": [
                {
                    "id": "energetic_morning",
                    "name": "Energetyczny Start Dnia",
                    "category": "breakfast",
                    "health_score": 94,
                    "price": 16.60,
                    "image": "/images/energetic-morning.jpg",
                    "reason": "Najpopularniejszy wybór o tej porze"
                },
                {
                    "id": "detox_green",
                    "name": "Detox Green Morning",
                    "category": "detox",
                    "health_score": 98,
                    "price": 21.00,
                    "image": "/images/detox-green.jpg",
                    "reason": "Idealny na oczyszczenie organizmu"
                }
            ],
            "trending_ingredients": [
                {
                    "id": "spirulina_powder",
                    "name": "Spirulina Powder BIO",
                    "category": "superfoods",
                    "price": 4.50,
                    "trend": "+22%",
                    "reason": "Bogata w B12 i żelazo"
                },
                {
                    "id": "matcha_premium",
                    "name": "Matcha Premium Grade A",
                    "category": "traditional",
                    "price": 6.20,
                    "trend": "+18%",
                    "reason": "Naturalna kofeina + L-teanina"
                },
                {
                    "id": "chia_seeds",
                    "name": "Chia Seeds Premium",
                    "category": "seeds",
                    "price": 3.20,
                    "trend": "+15%",
                    "reason": "Omega-3 i błonnik"
                }
            ],
            "personalized": [
                {
                    "type": "recipe",
                    "title": "Na podstawie Twoich preferencji",
                    "items": [
                        {
                            "id": "protein_power",
                            "name": "Power Protein Bowl",
                            "match": 92,
                            "reason": "Lubisz wysokobiałkowe mieszanki"
                        }
                    ]
                }
            ],
            "seasonal": {
                "title": "Sezonowe rekomendacje",
                "season": "Lato 2024",
                "items": [
                    {
                        "id": "coconut_water",
                        "name": "Woda Kokosowa Premium",
                        "reason": "Idealne nawodnienie w upalne dni"
                    }
                ]
            }
                 }
     })

# VENDING MACHINES API endpoints - NOWE!
@app.route('/api/vending-machines', methods=['GET'])
def get_vending_machines():
    """Lista automatów vendingowych z lokalizacjami"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": 1,
                "name": "IKIGAI Campus AGH",
                "location": "AGH University of Science and Technology",
                "address": "al. Mickiewicza 30, 30-059 Kraków",
                "lat": 50.0647,
                "lng": 19.9237,
                "status": "online",
                "uptime": 98.5,
                "daily_orders": 47,
                "popular_items": ["Energetyczny Start Dnia", "Protein Power Bowl"],
                "opening_hours": "06:00-22:00",
                "last_maintenance": "2024-06-10",
                "stock_level": 85
            },
            {
                "id": 2,
                "name": "IKIGAI Fitness Zone",
                "location": "City Fitness Center",
                "address": "ul. Karmelicka 45, 31-128 Kraków",
                "lat": 50.0613,
                "lng": 19.9370,
                "status": "online",
                "uptime": 97.2,
                "daily_orders": 63,
                "popular_items": ["Recovery & Zen", "Brain Boost Focus"],
                "opening_hours": "05:30-23:00",
                "last_maintenance": "2024-06-08",
                "stock_level": 92
            },
            {
                "id": 3,
                "name": "IKIGAI Tech Hub",
                "location": "Krakow Technology Park",
                "address": "ul. Podole 60, 30-394 Kraków",
                "lat": 50.0295,
                "lng": 19.9062,
                "status": "online",
                "uptime": 99.1,
                "daily_orders": 89,
                "popular_items": ["Detox Green Morning", "Brain Boost Focus"],
                "opening_hours": "07:00-20:00",
                "last_maintenance": "2024-06-11",
                "stock_level": 78
            },
            {
                "id": 4,
                "name": "IKIGAI Medical District",
                "location": "Jagiellonian University Medical College",
                "address": "ul. Św. Anny 12, 31-008 Kraków",
                "lat": 50.0614,
                "lng": 19.9365,
                "status": "maintenance",
                "uptime": 95.8,
                "daily_orders": 32,
                "popular_items": ["Energetyczny Start Dnia", "Recovery & Zen"],
                "opening_hours": "06:00-21:00",
                "last_maintenance": "2024-06-12",
                "stock_level": 45
            },
            {
                "id": 5,
                "name": "IKIGAI Old Town",
                "location": "Main Market Square Area",
                "address": "ul. Floriańska 23, 31-019 Kraków",
                "lat": 50.0619,
                "lng": 19.9368,
                "status": "online",
                "uptime": 96.7,
                "daily_orders": 71,
                "popular_items": ["Detox Green Morning", "Protein Power Bowl"],
                "opening_hours": "08:00-22:00",
                "last_maintenance": "2024-06-09",
                "stock_level": 88
            }
        ]
    })

# INGREDIENTS API endpoints - NOWE!
@app.route('/api/ingredients/categories', methods=['GET'])
def get_ingredients_categories():
    """Kategorie składników z PostgreSQL"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                # Pobierz kategorie z liczbą składników
                cursor.execute("""
                    SELECT ic.*, COUNT(i.id) as count
                    FROM ingredient_categories ic
                    LEFT JOIN ingredients i ON ic.id = i.category_id AND i.is_available = true
                    GROUP BY ic.id, ic.name, ic.description, ic.icon, ic.color, ic.slug
                    ORDER BY ic.id
                """)
                categories = cursor.fetchall()
                
                # Mapowanie kategorii na frontend
                category_mapping = {
                    'liquids': {'step': 1, 'frontend_name': 'Bazy', 'frontend_id': 'bases'},
                    'superfoods': {'step': 2, 'frontend_name': 'Superfoods', 'frontend_id': 'superfoods'},
                    'fruits': {'step': 2, 'frontend_name': 'Owoce', 'frontend_id': 'fruits'},
                    'nuts_seeds': {'step': 2, 'frontend_name': 'Nasiona', 'frontend_id': 'seeds'},
                    'sweeteners': {'step': 2, 'frontend_name': 'Produkty pszczele', 'frontend_id': 'honey'},
                    'adaptogens': {'step': 2, 'frontend_name': 'Detoks', 'frontend_id': 'detox'},
                    'vitamins': {'step': 2, 'frontend_name': 'Witaminy', 'frontend_id': 'vitamins'},
                    'proteins': {'step': 2, 'frontend_name': 'Białka', 'frontend_id': 'proteins'}
                }
                
                # Tworzenie odpowiedzi dla frontendu
                frontend_categories = []
                for cat in categories:
                    if cat['slug'] in category_mapping:
                        mapping = category_mapping[cat['slug']]
                        frontend_categories.append({
                            "id": mapping['frontend_id'],
                            "db_slug": cat['slug'],
                            "name": mapping['frontend_name'],
                            "description": cat['description'] or f"Składniki kategorii {mapping['frontend_name']}",
                            "icon": cat['icon'] or "🔸",
                            "color": cat['color'] or "#666666",
                            "count": int(cat['count']),
                            "step": mapping['step']
                        })
                
                print(f"✅ Pobrano {len(frontend_categories)} kategorii składników z PostgreSQL")
                return jsonify({
                    "status": "success",
                    "data": frontend_categories
                })
            else:
                print("❌ Brak połączenia z bazą danych - używam statycznych kategorii")
                
    except Exception as e:
        print(f"❌ Błąd pobierania kategorii składników: {e}")
    
    # Fallback - statyczne kategorie
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": "bases",
                "name": "Bazy",
                "description": "Płyny i bazy do mieszanek",
                "icon": "💧",
                "color": "#45b7d1",
                "count": 0,
                "step": 1
            },
            {
                "id": "superfoods",
                "name": "Superfoods",
                "description": "Składniki o wysokiej wartości odżywczej",
                "icon": "⚡",
                "color": "#4ecdc4",
                "count": 0,
                "step": 2
            }
        ]
    })
@app.route('/api/ingredients/bases', methods=['GET'])
def get_ingredients_bases():
    """Składniki - bazy płynne"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": "coconut_water",
                "name": "Woda Kokosowa Premium",
                "category": "bases",
                "price": 5.80,
                "calories_per_100ml": 45,
                "description": "Naturalne elektrolity i minerały",
                "origin": "Sri Lanka",
                "organic": True,
                "benefits": ["Nawodnienie", "Elektrolity", "Potas"]
            },
            {
                "id": "almond_milk",
                "name": "Mleko Migdałowe BIO",
                "category": "bases",
                "price": 4.20,
                "calories_per_100ml": 24,
                "description": "Delikatny smak, niska kaloryczność",
                "origin": "California",
                "organic": True,
                "benefits": ["Witamina E", "Niska kaloryczność", "Bez laktozy"]
            },
            {
                "id": "oat_milk",
                "name": "Mleko Owsiane Barista",
                "category": "bases",
                "price": 3.90,
                "calories_per_100ml": 59,
                "description": "Kremowa tekstura, idealne do mieszania",
                "origin": "Scandinavia",
                "organic": True,
                "benefits": ["Beta-glukan", "Kremowa tekstura", "Sustainable"]
            }
        ]
    })

@app.route('/api/ingredients/toppings', methods=['GET'])
def get_ingredients_toppings():
    """Składniki - dodatki i toppings"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": "chia_seeds",
                "name": "Chia Seeds Premium",
                "category": "seeds",
                "price": 3.20,
                "calories_per_10g": 49,
                "description": "Nasiona chia bogate w omega-3",
                "origin": "Mexico",
                "organic": True,
                "benefits": ["Omega-3", "Błonnik", "Magnez"]
            },
            {
                "id": "goji_berries",
                "name": "Goji Berries Organic",
                "category": "superfoods",
                "price": 7.80,
                "calories_per_10g": 34,
                "description": "Suszone jagody goji z Himalajów",
                "origin": "Tibet",
                "organic": True,
                "benefits": ["Antyoksydanty", "Witamina C", "Zeaksantyna"]
            },
            {
                "id": "hemp_seeds",
                "name": "Hemp Seeds Raw",
                "category": "seeds",
                "price": 4.50,
                "calories_per_10g": 55,
                "description": "Surowe nasiona konopi, kompletne aminokwasy",
                "origin": "Canada",
                "organic": True,
                "benefits": ["Kompletne białko", "GLA", "Magnez"]
            }
        ]
    })

# LOYALTY PROGRAM API endpoints - NOWE!
@app.route('/api/loyalty/profile/<user_id>', methods=['GET'])
def get_loyalty_profile(user_id):
    """Profil użytkownika w programie lojalnościowym"""
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user_id,
            "name": "IKIGAI Enthusiast",
            "email": "user@example.com",
            "level": 3,
            "level_name": "Wellness Warrior",
            "points": 2847,
            "points_to_next_level": 653,
            "total_orders": 47,
            "total_spent": 892.40,
            "member_since": "2024-03-15",
            "favorite_recipe": "Energetyczny Start Dnia",
            "badges": [
                {
                    "id": "first_order",
                    "name": "Pierwszy Krok",
                    "description": "Pierwsze zamówienie w IKIGAI",
                    "earned_date": "2024-03-15",
                    "rarity": "common"
                },
                {
                    "id": "week_streak",
                    "name": "Tygodniowy Streak",
                    "description": "7 dni z rzędu zdrowych wyborów",
                    "earned_date": "2024-05-22",
                    "rarity": "rare"
                },
                {
                    "id": "eco_warrior",
                    "name": "Eco Warrior",
                    "description": "25 ekologicznych składników",
                    "earned_date": "2024-06-01",
                    "rarity": "epic"
                }
            ],
            "next_reward": {
                "points_needed": 153,
                "reward": "Darmowa mieszanka premium"
            }
        }
    })

@app.route('/api/loyalty/challenges/<user_id>', methods=['GET'])
def get_loyalty_challenges(user_id):
    """Wyzwania dla użytkownika"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": "daily_protein",
                "name": "Protein Power",
                "description": "Zamów mieszankę z dodatkiem białka",
                "type": "daily",
                "progress": 1,
                "target": 1,
                "reward_points": 50,
                "expires": "2024-06-13T23:59:59Z",
                "status": "completed",
                "difficulty": "easy"
            },
            {
                "id": "weekly_variety",
                "name": "Różnorodność Smaków",
                "description": "Spróbuj 5 różnych składników w tym tygodniu",
                "type": "weekly",
                "progress": 3,
                "target": 5,
                "reward_points": 200,
                "expires": "2024-06-16T23:59:59Z",
                "status": "active",
                "difficulty": "medium"
            },
            {
                "id": "monthly_eco",
                "name": "Eco Champion",
                "description": "20 zamówień z lokalnymi składnikami",
                "type": "monthly",
                "progress": 14,
                "target": 20,
                "reward_points": 500,
                "expires": "2024-06-30T23:59:59Z",
                "status": "active",
                "difficulty": "hard"
            }
        ]
    })

@app.route('/api/loyalty/rewards', methods=['GET'])
def get_loyalty_rewards():
    """Dostępne nagrody w sklepie punktów"""
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": "free_small",
                "name": "Darmowa Mała Mieszanka",
                "description": "Wybierz dowolną mieszankę do 20zł",
                "cost": 500,
                "category": "freebies",
                "available": True,
                "image": "/images/rewards/free-small.jpg",
                "popularity": "high"
            },
            {
                "id": "free_premium",
                "name": "Darmowa Premium Mieszanka",
                "description": "Dowolna mieszanka bez limitu ceny",
                "cost": 1000,
                "category": "freebies",
                "available": True,
                "image": "/images/rewards/free-premium.jpg",
                "popularity": "medium"
            },
            {
                "id": "discount_20",
                "name": "20% Zniżka",
                "description": "20% zniżki na następne 3 zamówienia",
                "cost": 750,
                "category": "discounts",
                "available": True,
                "image": "/images/rewards/discount.jpg",
                "popularity": "high"
            },
            {
                "id": "ikigai_bottle",
                "name": "IKIGAI Eco Bottle",
                "description": "Bambusowa butelka z logo IKIGAI",
                "cost": 2000,
                "category": "merchandise",
                "available": True,
                "image": "/images/rewards/bottle.jpg",
                "popularity": "medium"
            },
            {
                "id": "nutrition_guide",
                "name": "Personal Nutrition Guide",
                "description": "Konsultacja z dietetykiem (30 min)",
                "cost": 3000,
                "category": "services",
                "available": True,
                "image": "/images/rewards/consultation.jpg",
                "popularity": "low"
            }
        ]
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
            "ingredients_usage": "/api/analytics/ingredients/usage",
            "funnel": "/api/analytics/funnel",
            "realtime": "/api/analytics/realtime",
            "suggestions": "/api/suggestions/smart",
            "favorites": "/api/favorites",
            "meal_recipes": "/api/meal-recipes",
            "recipe_categories": "/api/meal-recipes/categories",
            "recommendations": "/api/recommendations",
            "vending_machines": "/api/vending-machines",
            "ingredients_categories": "/api/ingredients/categories",
            "ingredients_bases": "/api/ingredients/bases",
            "ingredients_toppings": "/api/ingredients/toppings",
            "loyalty_profile": "/api/loyalty/profile/<user_id>",
            "loyalty_challenges": "/api/loyalty/challenges/<user_id>",
            "loyalty_rewards": "/api/loyalty/rewards"
        }
    })


@app.route("/api/ingredients/category/<category_slug>", methods=["GET"])
def get_ingredients_by_category(category_slug):
    """Składniki dla konkretnej kategorii z PostgreSQL"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT i.id, i.name, i.description, i.price FROM ingredients i JOIN ingredient_categories ic ON i.category_id = ic.id WHERE ic.slug = %s AND i.is_available = true ORDER BY i.name", (category_slug,))
                ingredients = cursor.fetchall()
                data = [{"id": ing["id"], "name": ing["name"], "description": ing["description"] or "Składnik", "price": float(ing["price"] or 0)} for ing in ingredients]
                print(f"✅ {len(data)} składników dla {category_slug}")
                return jsonify({"status": "success", "data": data, "count": len(data)})
    except Exception as e:
        print(f"ERROR: {e}")
    return jsonify({"status": "error", "data": [], "count": 0})


# ===== SYSTEM ZAMÓWIEŃ I QR KODÓW =====

def generate_qr_code(order_id, order_data):
    """Generuje kod QR dla zamówienia"""
    try:
        # Dane do QR kodu
        qr_data = {
            "order_id": order_id, "order": {"id": order_id}, "success": True,
            "user_id": order_data.get("user_id"),
            "recipe_id": order_data.get("recipe_id"),
            "machine_id": order_data.get("machine_id"),
            "total_price": order_data.get("total_price"),
            "timestamp": datetime.now().isoformat()
        }
        
        qr_content = json.dumps(qr_data)
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
        
    except Exception as e:
        print(f"❌ Błąd generowania QR kodu: {e}")
        return None


@app.route("/api/orders/test", methods=["POST"])
def test_order():
    try:
        data = request.get_json()
        return jsonify({"status": "success", "received": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Składanie nowego zamówienia"""
    try:
        raw_data = request.get_json(); print(f"📥 Raw data: {raw_data}"); data = {"user_id": raw_data.get("user_id", "web_user"), "machine_id": raw_data.get("machine_id") or raw_data.get("vending_machine_id", "VM001"), "payment_method": raw_data.get("payment_method", "card"), "recipe_id": raw_data.get("recipe_id", "detox_green"), "notes": raw_data.get("notes", "")}; print(f"📝 Normalized: {data}")
        required_fields = ["user_id", "recipe_id", "machine_id", "payment_method"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"status": "error", "message": f"Brak pola: {field}"}), 400
        
        order_id = str(uuid.uuid4())
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT price FROM recipes WHERE id = %s", (data["recipe_id"],))
                recipe = cursor.fetchone()
                
                if not recipe:
                    return jsonify({"status": "error", "message": "Przepis nie znaleziony"}), 404
                
                total_price = float(recipe["price"])
                
                order_data = {
                    "user_id": data["user_id"],
                    "recipe_id": data["recipe_id"],
                    "machine_id": data["machine_id"],
                    "total_price": total_price,
                    "payment_method": data["payment_method"],
                    "notes": data.get("notes", "")
                }
                # qr_code = generate_qr_code(order_id, order_data)
                # qr_code = None  # Tymczasowo wyłączone
                qr_code = generate_qr_code(order_id, order_data)
                
                cursor.execute("""
                    INSERT INTO orders (id, user_id, recipe_id, status, total_price, 
                                      payment_method, machine_id, qr_code, created_at, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    order_id, data["user_id"], data["recipe_id"], "pending", 
                    total_price, data["payment_method"], data["machine_id"], 
                    qr_code, datetime.now(), data.get("notes", "")
                ))
                conn.commit()
                
                print(f"✅ Zamówienie {order_id} utworzone")
                
                return jsonify({
                    "status": "success",
                    "order_id": order_id, "order": {"id": order_id}, "success": True,
                    "qr_code": qr_code,
                    "total_price": total_price,
                    "estimated_time": 5,
                    "message": "Zamówienie zostało złożone. Pokaż kod QR przy automacie."
                })
                
    except Exception as e:
        print(f"❌ Błąd tworzenia zamówienia: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Pobieranie listy zamówień"""
    try:
        user_id = request.args.get("user_id")
        status = request.args.get("status")
        limit = int(request.args.get("limit", 20))
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                query = """
                    SELECT o.*, r.name as recipe_name, r.description as recipe_description
                    FROM orders o
                    LEFT JOIN recipes r ON o.recipe_id = r.id
                    WHERE 1=1
                """
                params = []
                
                if user_id:
                    query += " AND o.user_id = %s"
                    params.append(user_id)
                    
                if status:
                    query += " AND o.status = %s"
                    params.append(status)
                    
                query += " ORDER BY o.created_at DESC LIMIT %s"
                params.append(limit)
                
                cursor.execute(query, params)
                orders = cursor.fetchall()
                
                orders_data = []
                for order in orders:
                    orders_data.append({
                        "id": order["id"],
                        "user_id": order["user_id"],
                        "recipe": {
                            "id": order["recipe_id"],
                            "name": order["recipe_name"],
                            "description": order["recipe_description"]
                        },
                        "status": order["status"],
                        "total_price": float(order["total_price"]),
                        "payment_method": order["payment_method"],
                        "machine_id": order["machine_id"],
                        "created_at": order["created_at"].isoformat() if order["created_at"] else None,
                        "completed_at": order["completed_at"].isoformat() if order["completed_at"] else None,
                        "notes": order["notes"],
                        "qr_code": order["qr_code"] if order["status"] == "pending" else None
                    })
                
                print(f"✅ Pobrano {len(orders_data)} zamówień")
                return jsonify({
                    "status": "success",
                    "data": orders_data,
                    "count": len(orders_data)
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania zamówień: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Pobieranie szczegółów zamówienia"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("""
                    SELECT o.*, r.name as recipe_name, r.description as recipe_description,
                           r.ingredients, r.calories, r.protein
                    FROM orders o
                    LEFT JOIN recipes r ON o.recipe_id = r.id
                    WHERE o.id = %s
                """, (order_id,))
                
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Zamówienie nie znalezione"}), 404
                
                order_data = {
                    "id": order["id"],
                    "user_id": order["user_id"],
                    "recipe": {
                        "id": order["recipe_id"],
                        "name": order["recipe_name"],
                        "description": order["recipe_description"],
                        "ingredients": order["ingredients"],
                        "calories": order["calories"],
                        "protein": order["protein"]
                    },
                    "status": order["status"],
                    "total_price": float(order["total_price"]),
                    "payment_method": order["payment_method"],
                    "machine_id": order["machine_id"],
                    "created_at": order["created_at"].isoformat() if order["created_at"] else None,
                    "completed_at": order["completed_at"].isoformat() if order["completed_at"] else None,
                    "notes": order["notes"],
                    "qr_code": order["qr_code"]
                }
                
                return jsonify({
                    "status": "success",
                    "data": order_data
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania zamówienia {order_id}: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Aktualizacja statusu zamówienia"""
    try:
        data = request.get_json()
        new_status = data.get("status")
        
        if new_status not in ["pending", "preparing", "ready", "completed", "cancelled"]:
            return jsonify({"status": "error", "message": "Nieprawidłowy status"}), 400
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor()
                
                if new_status == "completed":
                    cursor.execute(
                        "UPDATE orders SET status = %s, completed_at = %s WHERE id = %s",
                        (new_status, datetime.now(), order_id)
                    )
                else:
                    cursor.execute(
                        "UPDATE orders SET status = %s WHERE id = %s",
                        (new_status, order_id)
                    )
                
                if cursor.rowcount == 0:
                    return jsonify({"status": "error", "message": "Zamówienie nie znalezione"}), 404
                
                conn.commit()
                
                print(f"✅ Status zamówienia {order_id} zmieniony na {new_status}")
                return jsonify({
                    "status": "success",
                    "message": f"Status zamówienia zmieniony na {new_status}"
                })
                
    except Exception as e:
        print(f"❌ Błąd aktualizacji statusu {order_id}: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders/<order_id>/qr', methods=['GET'])
def get_order_qr(order_id):
    """Pobieranie kodu QR dla zamówienia"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT qr_code, status FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Zamówienie nie znalezione"}), 404
                
                if order["status"] not in ["pending", "preparing"]:
                    return jsonify({"status": "error", "message": "Kod QR nieaktywny dla tego statusu"}), 400
                
                return jsonify({
                    "status": "success",
                    "qr_code": order["qr_code"],
                    "order_status": order["status"]
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania QR dla {order_id}: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

if __name__ == '__main__':
    print("🚀 Uruchamiam IKIGAI Analytics Server...")
    app.run(host='0.0.0.0', port=5001, debug=True) 

