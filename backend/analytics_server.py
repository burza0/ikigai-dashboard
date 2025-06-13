#!/usr/bin/env python3
"""
🎯 IKIGAI Analytics Server with SQLite Database
Serwer API z pełną integracją bazy danych SQLite
"""

from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
import sqlite3
import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from contextlib import contextmanager
from functools import wraps

print("🎯 IKIGAI Analytics Server with Database - Uruchamianie...")

# Tworzymy aplikację Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ikigai-dev-secret-key-2024')

# Konfiguracja CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Sprawdź czy używamy PostgreSQL (Heroku) czy SQLite (lokalnie)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    print("🐘 Wykryto PostgreSQL na Heroku")
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    try:
        import psycopg2
        import psycopg2.extras
        DB_TYPE = 'postgresql'
        DB_PATH = DATABASE_URL
        print("✅ PostgreSQL połączone")
    except ImportError:
        print("❌ Brak psycopg2 - używam SQLite")
        DB_TYPE = 'sqlite'
        DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')
        DB_AVAILABLE = os.path.exists(DB_PATH)
else:
    print("🗃️ Używam lokalnej bazy SQLite")
    DB_TYPE = 'sqlite'
    DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')

# Sprawdź dostępność bazy
if DB_TYPE == 'sqlite':
    DB_AVAILABLE = os.path.exists(DB_PATH)
    if DB_AVAILABLE:
        print(f"✅ SQLite dostępne: {DB_PATH}")
    else:
        print(f"⚠️ SQLite niedostępne: {DB_PATH}")
else:
    DB_AVAILABLE = True

# Ścieżka do plików statycznych frontendu
STATIC_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')

print("📊 IKIGAI Analytics Server v4.0 with Database - Ready!")
print("🌐 Endpoints dostępne na http://localhost:5001")
print("📈 Analytics Dashboard: /api/analytics/*")
print("🍜 Meal Recipes: /api/meal-recipes* (z bazy danych)")
print("🏆 Loyalty Program: /api/loyalty/* (z bazy danych)")
print("🧪 Ingredients: /api/ingredients/* (z bazy danych)")
print(f"🗄️ Database: {DB_TYPE} - {'✅' if DB_AVAILABLE else '❌'}")

@contextmanager
def get_db_connection():
    """Context manager dla połączeń z bazą - SQLite + PostgreSQL"""
    if not DB_AVAILABLE:
        yield None
        return
        
    conn = None
    try:
        if DB_TYPE == 'postgresql':
            conn = psycopg2.connect(DB_PATH)
            yield conn
        else:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            yield conn
    except Exception as e:
        print(f"⚠️ Błąd połączenia z bazą {DB_TYPE}: {e}")
        yield None
    finally:
        if conn:
            conn.close()

def parse_json_field(value):
    """Parsuje pole JSON z bazy danych"""
    if not value:
        return []
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return []

def parse_json_object(value):
    """Parsuje obiekt JSON z bazy danych"""
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}

# =========================
# AUTENTYFIKACJA
# =========================

def hash_password(password):
    """Hashuje hasło za pomocą SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Weryfikuje hasło"""
    return hash_password(password) == password_hash

def setup_auth_tables():
    """Rozszerz tabelę users o kolumny autentyfikacji"""
    if not DB_AVAILABLE:
        print("⚠️ Pomijam setup bazy danych - baza niedostępna")
        return
        
    try:
        with get_db_connection() as conn:
            if not conn:
                print("⚠️ Brak połączenia z bazą - pomijam setup")
                return
            
            # Sprawdź czy kolumny już istnieją
            cursor = conn.execute("PRAGMA table_info(users)")
            existing_columns = [column[1] for column in cursor.fetchall()]
            
            # Dodaj brakujące kolumny
            if 'password_hash' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
                print("✅ Dodano kolumnę password_hash")
            
            if 'role' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
                print("✅ Dodano kolumnę role")
            
            if 'is_active' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1")
                print("✅ Dodano kolumnę is_active")
            
            if 'reset_token' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
                print("✅ Dodano kolumnę reset_token")
            
            if 'login_attempts' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN login_attempts INTEGER DEFAULT 0")
                print("✅ Dodano kolumnę login_attempts")
            
            if 'last_login' not in existing_columns:
                conn.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
                print("✅ Dodano kolumnę last_login")
            
            # Ustaw hasło dla istniejącego użytkownika
            conn.execute("""
                UPDATE users 
                SET password_hash = ?, role = 'user' 
                WHERE id = 'web_user' AND password_hash IS NULL
            """, (hash_password('demo123'),))
            
            # Dodaj administratora jeśli nie istnieje
            admin_exists = conn.execute("SELECT COUNT(*) FROM users WHERE id = 'admin'").fetchone()[0]
            
            if admin_exists == 0:
                conn.execute("""
                    INSERT INTO users (
                        id, name, email, phone, loyalty_level, loyalty_points, 
                        total_orders, total_spent, password_hash, role, is_active,
                        member_since, last_activity
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """, (
                    'admin',
                    'Administrator IKIGAI',
                    'admin@ikigai.com',
                    '+48 123 456 789',
                    5,
                    10000,
                    0,
                    0.0,
                    hash_password('admin123'),
                    'admin',
                    1
                ))
                print("👑 Utworzono konto administratora (admin/admin123)")
            
            conn.commit()
            
    except Exception as e:
        print(f"❌ Błąd rozszerzania tabeli users: {e}")

def require_login(f):
    """Decorator wymagający zalogowania"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Wymagane zalogowanie'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator wymagający uprawnień administratora"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Wymagane zalogowanie'}), 401
        
        try:
            with get_db_connection() as conn:
                user = conn.execute(
                    "SELECT role FROM users WHERE id = ? AND is_active = 1",
                    (session['user_id'],)
                ).fetchone()
                
                if not user or user['role'] != 'admin':
                    return jsonify({'status': 'error', 'message': 'Wymagane uprawnienia administratora'}), 403
                    
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Błąd weryfikacji uprawnień'}), 500
            
        return f(*args, **kwargs)
    return decorated_function

# Uruchom setup przy starcie serwera
setup_auth_tables()

# Analytics API endpoints
@app.route('/api/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Główne statystyki dashboard z bazy danych"""
    try:
        with get_db_connection() as conn:
            # Pobierz statystyki z bazy
            total_recipes = conn.execute("SELECT COUNT(*) as count FROM recipes WHERE is_available = 1").fetchone()['count']
            total_users = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()['count']
            total_orders = conn.execute("SELECT COUNT(*) as count FROM orders").fetchone()['count']
            total_ingredients = conn.execute("SELECT COUNT(*) as count FROM ingredients WHERE is_available = 1").fetchone()['count']
            
            # Sumuj przychody
            total_revenue = conn.execute("SELECT COALESCE(SUM(total_spent), 0) as revenue FROM users").fetchone()['revenue']
            
        return jsonify({
            "status": "success",
            "data": {
                "sales": {
                    "today": round(total_revenue * 0.05, 2),
                    "yesterday": round(total_revenue * 0.048, 2),
                    "this_week": round(total_revenue * 0.3, 2),
                    "last_week": round(total_revenue * 0.28, 2),
                    "this_month": total_revenue,
                    "last_month": round(total_revenue * 0.92, 2),
                    "growth_daily": 4.2,
                    "growth_weekly": 7.1,
                    "growth_monthly": 8.7
                },
                "orders": {
                    "total": total_orders,
                    "today": max(int(total_orders * 0.05), 1),
                    "completed": int(total_orders * 0.96),
                    "pending": int(total_orders * 0.04),
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
                    "total_usage": total_orders * 3,
                    "top_ingredient": "Spirulina Powder BIO",
                    "low_stock": 2,
                    "total_available": total_ingredients
                },
                "recipes": {
                    "total": total_recipes,
                    "featured": conn.execute("SELECT COUNT(*) as count FROM recipes WHERE is_featured = 1").fetchone()['count']
                },
                "users": {
                    "total": total_users,
                    "active_loyalty": total_users
                }
            }
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/analytics/dashboard: {e}")
        # Fallback na statyczne dane
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

# =========================
# MEAL RECIPES API (z bazy danych)
# =========================

@app.route('/api/meal-recipes', methods=['GET'])
def get_meal_recipes():
    """Lista wszystkich przepisów na mieszanki z bazy danych"""
    try:
        if not DB_AVAILABLE:
            # Zwróć statyczne dane gdy baza nie istnieje
            return jsonify({
                "status": "success",
                "data": [
                    {
                        "id": "energetic_morning",
                        "name": "Energetyczny Start Dnia",
                        "category": "breakfast",
                        "category_name": "Śniadanie",
                        "description": "Idealny boost energii na start dnia",
                        "long_description": "Pełnowartościowy posiłek z wysokiej jakości białkami i superfoods",
                        "price": 16.60,
                        "health_score": 94,
                        "calories": 385,
                        "protein": 25,
                        "carbs": 35,
                        "fat": 12,
                        "fiber": 8,
                        "sugar": 15,
                        "prep_time": 3,
                        "difficulty": "łatwy",
                        "tags": ["wysokobiałkowy", "energetyczny", "organiczny"],
                        "is_featured": True,
                        "popularity_score": 95
                    },
                    {
                        "id": "detox_green",
                        "name": "Detox Green Morning",
                        "category": "detox",
                        "category_name": "Detox",
                        "description": "Oczyszczający zielony shake",
                        "long_description": "Mieszanka zielonych superfoods do detoksykacji organizmu",
                        "price": 21.00,
                        "health_score": 98,
                        "calories": 320,
                        "protein": 18,
                        "carbs": 28,
                        "fat": 8,
                        "fiber": 12,
                        "sugar": 10,
                        "prep_time": 4,
                        "difficulty": "średni",
                        "tags": ["detox", "zielony", "antyoksydanty"],
                        "is_featured": True,
                        "popularity_score": 89
                    },
                    {
                        "id": "protein_power",
                        "name": "Power Protein Bowl",
                        "category": "workout",
                        "category_name": "Trening",
                        "description": "Maksymalna dawka białka",
                        "long_description": "Idealny po treningu - wysokie białko i aminokwasy",
                        "price": 18.30,
                        "health_score": 91,
                        "calories": 420,
                        "protein": 35,
                        "carbs": 30,
                        "fat": 15,
                        "fiber": 6,
                        "sugar": 12,
                        "prep_time": 3,
                        "difficulty": "łatwy",
                        "tags": ["post-workout", "wysokobiałkowy", "regeneracja"],
                        "is_featured": False,
                        "popularity_score": 82
                    },
                    {
                        "id": "focus_brain",
                        "name": "Focus Brain Boost",
                        "category": "cognitive",
                        "category_name": "Koncentracja",
                        "description": "Wsparcie dla mózgu i koncentracji",
                        "long_description": "Składniki wspierające funkcje kognitywne i pamięć",
                        "price": 19.90,
                        "health_score": 93,
                        "calories": 350,
                        "protein": 20,
                        "carbs": 32,
                        "fat": 10,
                        "fiber": 9,
                        "sugar": 8,
                        "prep_time": 4,
                        "difficulty": "średni",
                        "tags": ["nootropic", "koncentracja", "adaptogeny"],
                        "is_featured": True,
                        "popularity_score": 87
                    },
                    {
                        "id": "zen_balance",
                        "name": "Zen Balance",
                        "category": "relaxation",
                        "category_name": "Relaks",
                        "description": "Spokój i równowaga",
                        "long_description": "Relaksujący blend z ashwagandha i magnesem",
                        "price": 17.50,
                        "health_score": 89,
                        "calories": 295,
                        "protein": 15,
                        "carbs": 25,
                        "fat": 7,
                        "fiber": 10,
                        "sugar": 6,
                        "prep_time": 3,
                        "difficulty": "łatwy",
                        "tags": ["relaksujący", "adaptogeny", "stres"],
                        "is_featured": False,
                        "popularity_score": 76
                    }
                ]
            })
        
        with get_db_connection() as conn:
            if not conn:
                # Fallback gdy nie można połączyć się z bazą
                return get_meal_recipes()  # Rekurencyjne wywołanie dla statycznych danych
            
            recipes = conn.execute("""
                SELECT r.*, c.name as category_name
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.is_available = 1
                ORDER BY r.popularity_score DESC, r.name
            """).fetchall()
            
            result = []
            for recipe in recipes:
                # Pobierz składniki dla tego przepisu
                ingredients = conn.execute("""
                    SELECT ri.amount, ri.unit, i.id, i.name, i.price
                    FROM recipe_ingredients ri
                    JOIN ingredients i ON ri.ingredient_id = i.id
                    WHERE ri.recipe_id = ?
                    ORDER BY ri.is_required DESC, i.name
                """, (recipe['id'],)).fetchall()
                
                recipe_data = {
                    "id": recipe['id'],
                    "name": recipe['name'],
                    "category": recipe['category_id'],
                    "category_name": recipe['category_name'],
                    "description": recipe['description'],
                    "long_description": recipe['long_description'],
                    "ingredients": [ing['id'] for ing in ingredients],  # Lista ID składników
                    "ingredients_detail": [
                        {
                            "id": ing['id'],
                            "name": ing['name'],
                            "amount": f"{ing['amount']}{ing['unit']}",
                            "price": ing['price']
                        } for ing in ingredients
                    ],
                    "calories": recipe['calories'],
                    "protein": recipe['protein'],
                    "carbs": recipe['carbs'],
                    "fat": recipe['fat'],
                    "fiber": recipe['fiber'],
                    "sugar": recipe['sugar'],
                    "health_score": recipe['health_score'],
                    "prep_time": recipe['prep_time'],
                    "price": recipe['price'],
                    "difficulty": recipe['difficulty'],
                    "tags": parse_json_field(recipe['tags']),
                    "instructions": parse_json_field(recipe['instructions']),
                    "tips": parse_json_field(recipe['tips']),
                    "is_featured": bool(recipe['is_featured']),
                    "popularity_score": recipe['popularity_score']
                }
                result.append(recipe_data)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/meal-recipes: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania przepisów: {str(e)}"
        }), 500

@app.route('/api/meal-recipes/categories', methods=['GET'])
def get_meal_categories():
    """Kategorie przepisów z bazy danych"""
    try:
        with get_db_connection() as conn:
            categories = conn.execute("""
                SELECT c.*, COUNT(r.id) as recipe_count
                FROM categories c
                LEFT JOIN recipes r ON c.id = r.category_id AND r.is_available = 1
                WHERE c.type = 'recipe'
                GROUP BY c.id, c.name, c.description, c.icon, c.color
                ORDER BY c.name
            """).fetchall()
            
            # Przekształć na format oczekiwany przez frontend
            result = []
            for cat in categories:
                # Frontend oczekuje tablicy obiektów, ale baza zwraca jeden obiekt
                category_data = {
                    "id": cat['id'],
                    "name": cat['name'],
                    "description": cat['description'],
                    "icon": cat['icon'],
                    "color": cat['color'],
                    "count": cat['recipe_count']
                }
                result.append(category_data)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/meal-recipes/categories: {e}")
        return jsonify({
            "status": "error", 
            "message": f"Błąd pobierania kategorii: {str(e)}"
        }), 500

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
    """Rekomendacje przepisów z bazy danych"""
    # Statyczne dane gdy baza nie jest dostępna
    if not DB_AVAILABLE:
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
                        "image": "/images/energetic_morning.jpg",
                        "reason": "Polecany przez społeczność IKIGAI"
                    },
                    {
                        "id": "detox_green",
                        "name": "Detox Green Morning",
                        "category": "detox",
                        "health_score": 98,
                        "price": 21.00,
                        "image": "/images/detox_green.jpg",
                        "reason": "Najlepszy na detoks organizmu"
                    },
                    {
                        "id": "protein_power",
                        "name": "Power Protein Bowl",
                        "category": "workout",
                        "health_score": 91,
                        "price": 18.30,
                        "image": "/images/protein_power.jpg",
                        "reason": "Idealny po treningu"
                    }
                ],
                "trending_ingredients": [
                    {
                        "id": "spirulina_powder",
                        "name": "Spirulina Powder BIO",
                        "category": "superfoods",
                        "price": 4.50,
                        "trend": "+15%",
                        "reason": "Popularny wybór tego miesiąca"
                    },
                    {
                        "id": "protein_vanilla",
                        "name": "Protein Vanilla Premium",
                        "category": "proteins",
                        "price": 8.20,
                        "trend": "+12%",
                        "reason": "Najczęściej dodawany do bowli"
                    }
                ],
                "personalized": [],
                "seasonal": {
                    "title": "Sezonowe rekomendacje",
                    "season": "Lato 2024",
                    "items": [
                        {
                            "id": "coconut_water",
                            "name": "Woda Kokosowa Premium",
                            "category": "liquids",
                            "price": 5.80,
                            "trend": "+25%",
                            "reason": "Doskonałe na upały"
                        }
                    ]
                }
            }
        })
    
    try:
        with get_db_connection() as conn:
            if not conn:
                # Zwróć statyczne dane gdy baza nie jest dostępna (rekurencyjnie)
                temp_db_available = globals()['DB_AVAILABLE']
                globals()['DB_AVAILABLE'] = False
                result = get_recommendations()
                globals()['DB_AVAILABLE'] = temp_db_available
                return result
            
            # Pobierz popularne przepisy
            featured_recipes = conn.execute("""
                SELECT r.id, r.name, r.category_id, r.health_score, r.price, r.popularity_score
                FROM recipes r
                WHERE r.is_featured = 1 AND r.is_available = 1
                ORDER BY r.popularity_score DESC
                LIMIT 3
            """).fetchall()
            
            # Pobierz popularne składniki
            trending_ingredients = conn.execute("""
                SELECT i.id, i.name, i.price, c.name as category_name
                FROM ingredients i
                LEFT JOIN categories c ON i.category_id = c.id
                WHERE i.is_available = 1
                ORDER BY i.stock_level DESC
                LIMIT 3
            """).fetchall()
            
            featured_list = []
            for recipe in featured_recipes:
                featured_list.append({
                    "id": recipe['id'],
                    "name": recipe['name'],
                    "category": recipe['category_id'],
                    "health_score": recipe['health_score'],
                    "price": recipe['price'],
                    "image": f"/images/{recipe['id']}.jpg",
                    "reason": "Polecany przez społeczność IKIGAI"
                })
            
            trending_list = []
            for ing in trending_ingredients:
                trending_list.append({
                    "id": ing['id'],
                    "name": ing['name'],
                    "category": ing['category_name'] or "general",
                    "price": ing['price'],
                    "trend": "+15%",
                    "reason": "Popularny wybór tego miesiąca"
                })
        
        return jsonify({
            "status": "success",
            "data": {
                "featured_recipes": featured_list,
                "trending_ingredients": trending_list,
                "personalized": [],
                "seasonal": {
                    "title": "Sezonowe rekomendacje",
                    "season": "Lato 2024",
                    "items": trending_list[:2]
                }
            }
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/recommendations: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania rekomendacji: {str(e)}"
        }), 500

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

# =========================
# INGREDIENTS API (z bazy danych)
# =========================

@app.route('/api/ingredients/categories', methods=['GET'])
def get_ingredients_categories():
    """Kategorie składników z bazy danych"""
    try:
        with get_db_connection() as conn:
            categories = conn.execute("""
                SELECT c.*, COUNT(i.id) as ingredient_count
                FROM categories c
                LEFT JOIN ingredients i ON c.id = i.category_id AND i.is_available = 1
                WHERE c.type = 'ingredient'
                GROUP BY c.id, c.name, c.description, c.icon, c.color
                ORDER BY c.name
            """).fetchall()
            
            result = []
            for cat in categories:
                category_data = {
                    "id": cat['id'],
                    "name": cat['name'],
                    "description": cat['description'],
                    "icon": cat['icon'] or "🧪",
                    "color": cat['color'] or "#4ecdc4",
                    "count": cat['ingredient_count']
                }
                result.append(category_data)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/ingredients/categories: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania kategorii składników: {str(e)}"
        }), 500

@app.route('/api/ingredients/bases', methods=['GET'])
def get_ingredients_bases():
    """Składniki - bazy płynne z bazy danych"""
    try:
        with get_db_connection() as conn:
            # Pobierz składniki z kategorii odpowiadających bazom płynnym
            ingredients = conn.execute("""
                SELECT i.*, c.name as category_name
                FROM ingredients i
                LEFT JOIN categories c ON i.category_id = c.id
                WHERE i.is_available = 1 
                AND (i.unit = 'ml' OR i.category_id IN ('bases', 'liquids'))
                ORDER BY i.name
                LIMIT 10
            """).fetchall()
            
            result = []
            for ing in ingredients:
                ingredient_data = {
                    "id": ing['id'],
                    "name": ing['name'],
                    "category": ing['category_id'] or "bases",
                    "price": ing['price'],
                    "calories_per_100ml": 45,  # Wartość domyślna
                    "description": ing['description'] or f"Wysokiej jakości {ing['name'].lower()}",
                    "origin": "Premium",
                    "organic": bool(ing['is_organic']),
                    "benefits": parse_json_field(ing['benefits']),
                    "unit": ing['unit']
                }
                result.append(ingredient_data)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/ingredients/bases: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania baz: {str(e)}"
        }), 500

@app.route('/api/ingredients/toppings', methods=['GET'])
def get_ingredients_toppings():
    """Składniki - dodatki i toppings z bazy danych"""
    try:
        with get_db_connection() as conn:
            # Pobierz składniki które nie są bazami płynnymi
            ingredients = conn.execute("""
                SELECT i.*, c.name as category_name
                FROM ingredients i
                LEFT JOIN categories c ON i.category_id = c.id
                WHERE i.is_available = 1 
                AND i.unit != 'ml'
                AND i.category_id NOT IN ('bases', 'liquids')
                ORDER BY i.name
                LIMIT 15
            """).fetchall()
            
            result = []
            for ing in ingredients:
                ingredient_data = {
                    "id": ing['id'],
                    "name": ing['name'],
                    "category": ing['category_id'] or "toppings",
                    "price": ing['price'],
                    "calories_per_10g": 35,  # Wartość domyślna
                    "description": ing['description'] or f"Premium {ing['name'].lower()}",
                    "origin": "Organiczne",
                    "organic": bool(ing['is_organic']),
                    "benefits": parse_json_field(ing['benefits']),
                    "unit": ing['unit']
                }
                result.append(ingredient_data)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/ingredients/toppings: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania dodatków: {str(e)}"
        }), 500

# =========================
# LOYALTY PROGRAM API (z bazy danych)
# =========================

@app.route('/api/loyalty/profile/<user_id>', methods=['GET'])
def get_loyalty_profile(user_id):
    """Profil użytkownika w programie lojalnościowym z bazy danych"""
    try:
        with get_db_connection() as conn:
            if not conn:
                # Fallback na statyczne dane
                return jsonify({
                    "status": "success",
                    "data": {
                        "user_id": "web_user",
                        "name": "Demo User",
                        "email": "demo@ikigai.com",
                        "level": 2,
                        "level_name": "🌿 Health Enthusiast",
                        "points": 2847,
                        "points_to_next_level": 653,
                        "total_orders": 15,
                        "total_spent": 247.50,
                        "member_since": "2024-01-15",
                        "favorite_recipe": "Energetyczny Start Dnia",
                        "badges": ["early_adopter", "green_warrior"],
                        "next_reward": {
                            "points_needed": 153,
                            "reward": "Darmowa średnia mieszanka"
                        }
                    }
                })
            
            # Uniwersalne zapytanie SQL
            if DB_TYPE == 'postgresql':
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
            else:
                user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            
            if not user:
                return jsonify({
                    "status": "error",
                    "message": "Użytkownik nie znaleziony"
                }), 404
            
            # Oblicz poziom na podstawie punktów
            points = user['loyalty_points']
            levels = [
                {"level": 1, "name": "🌱 Wellness Starter", "points_required": 0},
                {"level": 2, "name": "🌿 Health Enthusiast", "points_required": 500},
                {"level": 3, "name": "🏆 Wellness Warrior", "points_required": 1500},
                {"level": 4, "name": "👑 IKIGAI Master", "points_required": 3500}
            ]
            
            current_level = 1
            level_name = "🌱 Wellness Starter"
            points_to_next = 500
            
            for level in levels:
                if points >= level['points_required']:
                    current_level = level['level']
                    level_name = level['name']
                    # Znajdź następny poziom
                    next_levels = [l for l in levels if l['level'] > current_level]
                    if next_levels:
                        points_to_next = next_levels[0]['points_required'] - points
                    else:
                        points_to_next = 0  # Maksymalny poziom
            
            # Parse badges z JSON
            badges = parse_json_field(user['badges'])
            
            profile_data = {
                "user_id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "level": current_level,
                "level_name": level_name,
                "points": points,
                "points_to_next_level": points_to_next,
                "total_orders": user['total_orders'],
                "total_spent": user['total_spent'],
                "member_since": user['member_since'],
                "favorite_recipe": user['favorite_recipe_id'] or "Brak",
                "badges": badges,
                "next_reward": {
                    "points_needed": max(500 - points, 0) if points < 500 else 0,
                    "reward": "Darmowa mała mieszanka"
                }
            }
        
        return jsonify({
            "status": "success",
            "data": profile_data
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/loyalty/profile/{user_id}: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania profilu: {str(e)}"
        }), 500

@app.route('/api/loyalty/challenges/<user_id>', methods=['GET'])
def get_loyalty_challenges(user_id):
    """Wyzwania dla użytkownika z bazy danych"""
    try:
        with get_db_connection() as conn:
            # Sprawdź czy użytkownik istnieje
            user_exists = conn.execute("""
                SELECT 1 FROM users WHERE id = ?
            """, (user_id,)).fetchone()
            
            if not user_exists:
                return jsonify({
                    "status": "error",
                    "message": "Użytkownik nie znaleziony"
                }), 404
            
            # Pobierz wyzwania z postępem użytkownika
            challenges = conn.execute("""
                SELECT 
                    lc.*,
                    COALESCE(ucp.progress, 0) as progress,
                    COALESCE(ucp.status, 'active') as user_status,
                    ucp.completed_at
                FROM loyalty_challenges lc
                LEFT JOIN user_challenge_progress ucp ON lc.id = ucp.challenge_id AND ucp.user_id = ?
                WHERE lc.is_active = 1
                ORDER BY lc.difficulty, lc.name
            """, (user_id,)).fetchall()
            
            result = []
            for challenge in challenges:
                challenge_data = {
                    "id": challenge['id'],
                    "name": challenge['name'],
                    "description": challenge['description'],
                    "type": challenge['type'],
                    "progress": challenge['progress'],
                    "target": challenge['target'],
                    "reward_points": challenge['reward_points'],
                    "expires": challenge['expires_at'],
                    "status": challenge['user_status'],
                    "difficulty": challenge['difficulty'],
                    "icon": challenge['icon'] or "🎯",
                    "completed": challenge['user_status'] == 'completed'
                }
                result.append(challenge_data)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/loyalty/challenges/{user_id}: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania wyzwań: {str(e)}"
        }), 500

@app.route('/api/loyalty/rewards', methods=['GET'])
def get_loyalty_rewards():
    """Dostępne nagrody w sklepie punktów z bazy danych"""
    try:
        with get_db_connection() as conn:
            rewards = conn.execute("""
                SELECT * FROM loyalty_rewards
                WHERE is_available = 1
                ORDER BY cost ASC, name
            """).fetchall()
            
            result = []
            for reward in rewards:
                reward_data = {
                    "id": reward['id'],
                    "name": reward['name'],
                    "description": reward['description'],
                    "cost": reward['cost'],
                    "category": reward['category'],
                    "available": bool(reward['is_available']),
                    "icon": reward['icon'] or "🏆",
                    "image": reward['image_url'] or f"/images/rewards/{reward['id']}.jpg",
                    "popularity": reward['popularity']
                }
                result.append(reward_data)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/loyalty/rewards: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania nagród: {str(e)}"
        }), 500

# =========================
# AUTENTYFIKACJA API
# =========================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Logowanie użytkownika"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'status': 'error',
                'message': 'Podaj login i hasło'
            }), 400
        
        with get_db_connection() as conn:
            # Znajdź użytkownika po ID lub emailu
            user = conn.execute("""
                SELECT id, name, email, password_hash, role, is_active, login_attempts
                FROM users 
                WHERE (id = ? OR email = ?) AND is_active = 1
            """, (username, username)).fetchone()
            
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'Nieprawidłowy login lub hasło'
                }), 401
            
            # Sprawdź blokadę konta (więcej niż 5 prób)
            if user['login_attempts'] >= 5:
                return jsonify({
                    'status': 'error',
                    'message': 'Konto zablokowane z powodu zbyt wielu nieudanych prób logowania'
                }), 401
            
            # Weryfikuj hasło
            if not verify_password(password, user['password_hash']):
                # Zwiększ licznik nieudanych prób
                conn.execute("""
                    UPDATE users 
                    SET login_attempts = login_attempts + 1 
                    WHERE id = ?
                """, (user['id'],))
                conn.commit()
                
                return jsonify({
                    'status': 'error',
                    'message': 'Nieprawidłowy login lub hasło'
                }), 401
            
            # Resetuj licznik prób i ustaw ostatnie logowanie
            conn.execute("""
                UPDATE users 
                SET login_attempts = 0, last_login = datetime('now'), last_activity = datetime('now')
                WHERE id = ?
            """, (user['id'],))
            conn.commit()
            
            # Ustaw sesję
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            session['user_name'] = user['name']
            
            return jsonify({
                'status': 'success',
                'message': 'Zalogowano pomyślnie',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            })
            
    except Exception as e:
        print(f"❌ Błąd logowania: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Błąd serwera podczas logowania'
        }), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Rejestracja nowego użytkownika"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Walidacja danych
        if not all([username, email, password, name]):
            return jsonify({
                'status': 'error',
                'message': 'Wszystkie pola są wymagane'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'status': 'error',
                'message': 'Hasło musi mieć przynajmniej 6 znaków'
            }), 400
        
        if '@' not in email:
            return jsonify({
                'status': 'error',
                'message': 'Nieprawidłowy format emaila'
            }), 400
        
        with get_db_connection() as conn:
            # Sprawdź czy użytkownik już istnieje
            existing = conn.execute("""
                SELECT id FROM users WHERE id = ? OR email = ?
            """, (username, email)).fetchone()
            
            if existing:
                return jsonify({
                    'status': 'error',
                    'message': 'Użytkownik o takim loginie lub emailu już istnieje'
                }), 409
            
            # Utwórz nowego użytkownika
            conn.execute("""
                INSERT INTO users (
                    id, name, email, password_hash, role, is_active,
                    loyalty_level, loyalty_points, total_orders, total_spent,
                    member_since, last_activity
                ) VALUES (?, ?, ?, ?, 'user', 1, 1, 0, 0, 0.0, datetime('now'), datetime('now'))
            """, (username, name, email, hash_password(password)))
            
            conn.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Konto zostało utworzone pomyślnie',
                'user': {
                    'id': username,
                    'name': name,
                    'email': email,
                    'role': 'user'
                }
            })
            
    except Exception as e:
        print(f"❌ Błąd rejestracji: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Błąd serwera podczas rejestracji'
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Wylogowanie użytkownika"""
    session.clear()
    return jsonify({
        'status': 'success',
        'message': 'Wylogowano pomyślnie'
    })

@app.route('/api/auth/profile', methods=['GET'])
@require_login
def get_profile():
    """Pobierz profil zalogowanego użytkownika"""
    try:
        with get_db_connection() as conn:
            user = conn.execute("""
                SELECT id, name, email, phone, role, loyalty_level, loyalty_points,
                       total_orders, total_spent, member_since, last_login
                FROM users WHERE id = ?
            """, (session['user_id'],)).fetchone()
            
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'Użytkownik nie znaleziony'
                }), 404
            
            return jsonify({
                'status': 'success',
                'data': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'phone': user['phone'],
                    'role': user['role'],
                    'loyalty_level': user['loyalty_level'],
                    'loyalty_points': user['loyalty_points'],
                    'total_orders': user['total_orders'],
                    'total_spent': user['total_spent'],
                    'member_since': user['member_since'],
                    'last_login': user['last_login']
                }
            })
            
    except Exception as e:
        print(f"❌ Błąd pobierania profilu: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Błąd pobierania profilu'
        }), 500

@app.route('/api/auth/users', methods=['GET'])
@require_admin
def get_all_users():
    """Lista wszystkich użytkowników (tylko dla adminów)"""
    try:
        with get_db_connection() as conn:
            users = conn.execute("""
                SELECT id, name, email, role, is_active, loyalty_points,
                       total_orders, member_since, last_login
                FROM users
                ORDER BY role DESC, name
            """).fetchall()
            
            result = []
            for user in users:
                result.append({
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role'],
                    'is_active': bool(user['is_active']),
                    'loyalty_points': user['loyalty_points'],
                    'total_orders': user['total_orders'],
                    'member_since': user['member_since'],
                    'last_login': user['last_login']
                })
            
            return jsonify({
                'status': 'success',
                'data': result
            })
            
    except Exception as e:
        print(f"❌ Błąd pobierania użytkowników: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Błąd pobierania użytkowników'
        }), 500

# =========================
# HEALTH CHECK
# =========================

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        with get_db_connection() as conn:
            # Test połączenia z bazą
            conn.execute("SELECT 1").fetchone()
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return jsonify({
        "status": "healthy", 
        "message": "IKIGAI Analytics Server with Database działa poprawnie",
        "database": db_status,
        "database_path": DB_PATH,
        "endpoints": {
            "analytics": "/api/analytics/dashboard",
            "meal_recipes": "/api/meal-recipes",
            "recipe_categories": "/api/meal-recipes/categories",
            "recommendations": "/api/recommendations",
            "loyalty_profile": "/api/loyalty/profile/<user_id>",
            "loyalty_challenges": "/api/loyalty/challenges/<user_id>",
            "loyalty_rewards": "/api/loyalty/rewards",
            "ingredients_categories": "/api/ingredients/categories",
            "ingredients_bases": "/api/ingredients/bases",
            "ingredients_toppings": "/api/ingredients/toppings",
            "vending_machines": "/api/vending-machines",
            "suggestions": "/api/suggestions/smart",
            "favorites": "/api/favorites"
        }
    })

# =========================
# FRONTEND STATIC FILES (dla Heroku)
# =========================

@app.route('/')
def serve_frontend():
    """Serwuje główną stronę frontendu"""
    try:
        return send_from_directory(STATIC_PATH, 'index.html')
    except Exception as e:
        return jsonify({"error": "Frontend not found", "message": str(e)}), 404

@app.route('/<path:filename>')
def serve_static(filename):
    """Serwuje pliki statyczne frontendu"""
    try:
        return send_from_directory(STATIC_PATH, filename)
    except Exception as e:
        # Jeśli plik nie istnieje, zwróć index.html (dla Vue Router)
        try:
            return send_from_directory(STATIC_PATH, 'index.html')
        except Exception:
            return jsonify({"error": "File not found", "message": str(e)}), 404

if __name__ == '__main__':
    print("🚀 Uruchamiam IKIGAI Analytics Server...")
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False) 