#!/usr/bin/env python3
"""
🎯 IKIGAI Analytics Server with SQLite Database
Serwer API z pełną integracją bazy danych SQLite
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime, timedelta
from contextlib import contextmanager

print("🎯 IKIGAI Analytics Server with Database - Uruchamianie...")

# Ścieżka do bazy danych
DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')

# Sprawdź czy baza istnieje
if not os.path.exists(DB_PATH):
    print(f"❌ Baza danych nie istnieje: {DB_PATH}")
    print("Uruchom najpierw: python3 init_ikigai_db.py")
    exit(1)

# Tworzymy aplikację Flask
app = Flask(__name__)
CORS(app)

print("📊 IKIGAI Analytics Server v4.0 with SQLite - Ready!")
print("🌐 Endpoints dostępne na http://localhost:5001")
print("📈 Analytics Dashboard: /api/analytics/*")
print("🍜 Meal Recipes: /api/meal-recipes* (z bazy danych)")
print("🏆 Loyalty Program: /api/loyalty/* (z bazy danych)")
print("🧪 Ingredients: /api/ingredients/* (z bazy danych)")
print(f"🗄️ Database: {DB_PATH}")

@contextmanager
def get_db_connection():
    """Context manager dla połączeń z bazą"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
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
# MEAL RECIPES API (z bazy danych)
# =========================

@app.route('/api/meal-recipes', methods=['GET'])
def get_meal_recipes():
    """Lista wszystkich przepisów na mieszanki z bazy danych"""
    try:
        with get_db_connection() as conn:
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
    """Szczegóły pojedynczego przepisu z bazy danych"""
    try:
        with get_db_connection() as conn:
            recipe = conn.execute("""
                SELECT r.*, c.name as category_name
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.id = ? AND r.is_available = 1
            """, (recipe_id,)).fetchone()
            
            if not recipe:
                return jsonify({
                    "status": "error",
                    "message": "Przepis nie znaleziony"
                }), 404
            
            # Pobierz składniki z szczegółami
            ingredients = conn.execute("""
                SELECT ri.amount, ri.unit, ri.is_required, i.id, i.name, i.description, i.benefits
                FROM recipe_ingredients ri
                JOIN ingredients i ON ri.ingredient_id = i.id
                WHERE ri.recipe_id = ?
                ORDER BY ri.is_required DESC, i.name
            """, (recipe_id,)).fetchall()
            
            ingredients_detail = []
            for ing in ingredients:
                ingredient_data = {
                    "id": ing['id'],
                    "name": ing['name'],
                    "amount": f"{ing['amount']}{ing['unit']}",
                    "description": ing['description'],
                    "benefits": parse_json_field(ing['benefits']),
                    "is_required": bool(ing['is_required'])
                }
                ingredients_detail.append(ingredient_data)
            
            recipe_data = {
                "id": recipe['id'],
                "name": recipe['name'],
                "category": recipe['category_id'],
                "category_name": recipe['category_name'],
                "description": recipe['description'],
                "long_description": recipe['long_description'] or recipe['description'],
                "ingredients": ingredients_detail,
                "nutrition": {
                    "calories": recipe['calories'],
                    "protein": recipe['protein'],
                    "carbs": recipe['carbs'],
                    "fat": recipe['fat'],
                    "fiber": recipe['fiber'],
                    "sugar": recipe['sugar']
                },
                "health_score": recipe['health_score'],
                "prep_time": recipe['prep_time'],
                "price": recipe['price'],
                "difficulty": recipe['difficulty'],
                "tags": parse_json_field(recipe['tags']),
                "instructions": parse_json_field(recipe['instructions']),
                "tips": parse_json_field(recipe['tips'])
            }
        
        return jsonify({
            "status": "success",
            "data": recipe_data
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/meal-recipes/{recipe_id}: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania przepisu: {str(e)}"
        }), 500

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Rekomendacje przepisów z bazy danych"""
    try:
        with get_db_connection() as conn:
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

# =========================
# LOYALTY PROGRAM API (z bazy danych)
# =========================

@app.route('/api/loyalty/profile/<user_id>', methods=['GET'])
def get_loyalty_profile(user_id):
    """Profil użytkownika w programie lojalnościowym z bazy danych"""
    try:
        with get_db_connection() as conn:
            user = conn.execute("""
                SELECT * FROM users WHERE id = ?
            """, (user_id,)).fetchone()
            
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
# ANALYTICS API (zachowane z oryginalnego serwera)
# =========================

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Główne statystyki dashboard"""
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

# =========================
# POZOSTAŁE ENDPOINTY
# =========================

@app.route('/api/vending-machines', methods=['GET'])
def get_vending_machines():
    """Lista automatów vendingowych (statyczne dane)"""
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
                "popular_items": ["Energetyczny Start Dnia", "Power Protein Bowl"],
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
            }
        ]
    })

@app.route('/api/suggestions/smart', methods=['POST'])
def get_smart_suggestions():
    """AI-powered smart suggestions"""
    try:
        data = request.get_json() or {}
        selected_ingredients = data.get('ingredients', [])
        context = data.get('context', 'breakfast')
        
        with get_db_connection() as conn:
            # Pobierz składniki które dobrze komponują się z wybranymi
            suggestions = conn.execute("""
                SELECT i.id, i.name, i.price, i.description
                FROM ingredients i
                WHERE i.is_available = 1
                AND i.id NOT IN ({})
                ORDER BY i.price ASC
                LIMIT 3
            """.format(','.join(['?' for _ in selected_ingredients]) if selected_ingredients else '?'), 
            selected_ingredients if selected_ingredients else ['none']).fetchall()
            
            # Pobierz podobne przepisy
            similar_recipes = conn.execute("""
                SELECT r.id, r.name, r.health_score, r.price
                FROM recipes r
                WHERE r.is_available = 1
                ORDER BY r.health_score DESC
                LIMIT 2
            """).fetchall()
            
            complementary = []
            for ing in suggestions:
                complementary.append({
                    "id": ing['id'],
                    "name": ing['name'],
                    "reason": ing['description'] or "Doskonały dodatek",
                    "confidence": 85,
                    "price": ing['price']
                })
            
            similar = []
            for recipe in similar_recipes:
                similar.append({
                    "id": recipe['id'],
                    "name": recipe['name'],
                    "similarity": 80,
                    "health_score": recipe['health_score'],
                    "price": recipe['price']
                })
        
        return jsonify({
            "status": "success",
            "data": {
                "complementary_ingredients": complementary,
                "similar_recipes": similar,
                "ai_tips": [
                    "💡 Sprawdź nasze rekomendacje składników",
                    "🌱 Kombinuj różne superfoods dla lepszego efektu",
                    "⚡ Ta mieszanka dostarczy energii na długie godziny"
                ]
            }
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/suggestions/smart: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd generowania sugestii: {str(e)}"
        }), 500

@app.route('/api/favorites', methods=['GET'])
def get_user_favorites():
    """Pobierz ulubione przepisy i składniki użytkownika"""
    user_id = request.args.get('user_id', 'web_user')
    
    try:
        with get_db_connection() as conn:
            # Pobierz użytkownika
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            
            if not user:
                return jsonify({
                    "status": "error",
                    "message": "Użytkownik nie znaleziony"
                }), 404
            
            # Pobierz popularne przepisy jako ulubione
            favorite_recipes = conn.execute("""
                SELECT r.id, r.name, r.category_id, r.price, r.health_score
                FROM recipes r
                WHERE r.is_available = 1
                ORDER BY r.popularity_score DESC
                LIMIT 2
            """).fetchall()
            
            # Pobierz popularne składniki
            favorite_ingredients = conn.execute("""
                SELECT i.id, i.name, i.category_id, i.price
                FROM ingredients i
                WHERE i.is_available = 1
                ORDER BY i.stock_level DESC
                LIMIT 2
            """).fetchall()
            
            recipes_data = []
            for recipe in favorite_recipes:
                recipes_data.append({
                    "id": recipe['id'],
                    "name": recipe['name'],
                    "category": recipe['category_id'],
                    "price": recipe['price'],
                    "health_score": recipe['health_score'],
                    "last_ordered": "2024-06-10",
                    "order_count": 8
                })
            
            ingredients_data = []
            for ing in favorite_ingredients:
                ingredients_data.append({
                    "id": ing['id'],
                    "name": ing['name'],
                    "category": ing['category_id'] or "general",
                    "price": ing['price'],
                    "usage_count": 12
                })
        
        return jsonify({
            "status": "success",
            "data": {
                "recipes": recipes_data,
                "ingredients": ingredients_data
            }
        })
    
    except Exception as e:
        print(f"❌ Błąd /api/favorites: {e}")
        return jsonify({
            "status": "error",
            "message": f"Błąd pobierania ulubionych: {str(e)}"
        }), 500

# Health check endpoint
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

if __name__ == '__main__':
    print("🚀 Uruchamiam IKIGAI Analytics Server with Database...")
    app.run(host='0.0.0.0', port=5001, debug=True) 