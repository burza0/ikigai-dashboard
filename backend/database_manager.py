#!/usr/bin/env python3
"""
🗄️ IKIGAI Database Manager
SQLite database manager dla aplikacji IKIGAI
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import List, Dict, Any, Optional

# Ścieżka do bazy danych
DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')

class IkigaiDatabase:
    """Manager bazy danych IKIGAI"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager dla połączeń z bazą"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Zwraca wyniki jako dict
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Inicjalizuje bazę danych i tworzy tabele"""
        with self.get_connection() as conn:
            # Włącz foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            
            # Tabela kategorii
            conn.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    icon TEXT,
                    color TEXT,
                    type TEXT NOT NULL CHECK (type IN ('recipe', 'ingredient')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela składników
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ingredients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category_id TEXT,
                    price REAL NOT NULL DEFAULT 0.0,
                    unit TEXT DEFAULT 'g',
                    description TEXT,
                    benefits TEXT, -- JSON array
                    nutrition TEXT, -- JSON object
                    allergens TEXT, -- JSON array
                    is_organic BOOLEAN DEFAULT FALSE,
                    is_available BOOLEAN DEFAULT TRUE,
                    stock_level INTEGER DEFAULT 100,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """)
            
            # Tabela przepisów
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category_id TEXT,
                    description TEXT,
                    long_description TEXT,
                    price REAL NOT NULL DEFAULT 0.0,
                    calories INTEGER DEFAULT 0,
                    protein REAL DEFAULT 0.0,
                    carbs REAL DEFAULT 0.0,
                    fat REAL DEFAULT 0.0,
                    fiber REAL DEFAULT 0.0,
                    sugar REAL DEFAULT 0.0,
                    health_score INTEGER DEFAULT 0,
                    prep_time INTEGER DEFAULT 0, -- minutes
                    difficulty TEXT DEFAULT 'easy' CHECK (difficulty IN ('easy', 'medium', 'hard')),
                    tags TEXT, -- JSON array
                    instructions TEXT, -- JSON array
                    tips TEXT, -- JSON array
                    image_url TEXT,
                    is_featured BOOLEAN DEFAULT FALSE,
                    is_available BOOLEAN DEFAULT TRUE,
                    popularity_score INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """)
            
            # Tabela składników w przepisach
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recipe_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipe_id TEXT NOT NULL,
                    ingredient_id TEXT NOT NULL,
                    amount REAL DEFAULT 0.0,
                    unit TEXT DEFAULT 'g',
                    is_required BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id),
                    UNIQUE(recipe_id, ingredient_id)
                )
            """)
            
            # Tabela użytkowników
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    loyalty_level INTEGER DEFAULT 1,
                    loyalty_points INTEGER DEFAULT 0,
                    total_orders INTEGER DEFAULT 0,
                    total_spent REAL DEFAULT 0.0,
                    favorite_recipe_id TEXT,
                    preferences TEXT, -- JSON object
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (favorite_recipe_id) REFERENCES recipes (id)
                )
            """)
            
            # Tabela wyzwań lojalnościowych
            conn.execute("""
                CREATE TABLE IF NOT EXISTS loyalty_challenges (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    type TEXT NOT NULL CHECK (type IN ('daily', 'weekly', 'monthly', 'special')),
                    target INTEGER NOT NULL DEFAULT 1,
                    reward_points INTEGER NOT NULL DEFAULT 0,
                    difficulty TEXT DEFAULT 'easy' CHECK (difficulty IN ('easy', 'medium', 'hard')),
                    icon TEXT,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela postępu użytkowników w wyzwaniach
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_challenge_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    challenge_id TEXT NOT NULL,
                    progress INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'expired')),
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                    FOREIGN KEY (challenge_id) REFERENCES loyalty_challenges (id),
                    UNIQUE(user_id, challenge_id)
                )
            """)
            
            # Tabela nagród lojalnościowych
            conn.execute("""
                CREATE TABLE IF NOT EXISTS loyalty_rewards (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    cost INTEGER NOT NULL DEFAULT 0, -- punkty
                    category TEXT DEFAULT 'general',
                    icon TEXT,
                    image_url TEXT,
                    is_available BOOLEAN DEFAULT TRUE,
                    popularity TEXT DEFAULT 'medium',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela zamówień
            conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    recipe_id TEXT,
                    total_price REAL NOT NULL DEFAULT 0.0,
                    total_calories INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'preparing', 'ready', 'completed', 'cancelled')),
                    qr_code TEXT,
                    custom_ingredients TEXT, -- JSON array
                    special_instructions TEXT,
                    estimated_prep_time INTEGER DEFAULT 5,
                    machine_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (recipe_id) REFERENCES recipes (id)
                )
            """)
            
            # Tabela automatów vendingowych
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vending_machines (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    location TEXT,
                    address TEXT,
                    latitude REAL,
                    longitude REAL,
                    status TEXT DEFAULT 'online' CHECK (status IN ('online', 'offline', 'maintenance')),
                    ingredients_capacity INTEGER DEFAULT 100,
                    daily_orders INTEGER DEFAULT 0,
                    uptime_percentage REAL DEFAULT 100.0,
                    last_maintenance TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Indeksy dla wydajności
            conn.execute("CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes (category_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_ingredients_category ON ingredients (category_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_user ON orders (user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_created ON orders (created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_loyalty ON users (loyalty_level, loyalty_points)")
            
            conn.commit()
            print("✅ Baza danych IKIGAI zainicjalizowana")
    
    # =========================
    # KATEGORIE
    # =========================
    
    def create_category(self, id: str, name: str, type: str, description: str = None, 
                       icon: str = None, color: str = None) -> bool:
        """Tworzy nową kategorię"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO categories (id, name, type, description, icon, color)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id, name, type, description, icon, color))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_categories(self, type: str = None) -> List[Dict]:
        """Pobiera kategorie"""
        with self.get_connection() as conn:
            if type:
                rows = conn.execute("SELECT * FROM categories WHERE type = ? ORDER BY name", (type,))
            else:
                rows = conn.execute("SELECT * FROM categories ORDER BY name")
            return [dict(row) for row in rows.fetchall()]
    
    # =========================
    # SKŁADNIKI
    # =========================
    
    def create_ingredient(self, id: str, name: str, category_id: str = None, 
                         price: float = 0.0, **kwargs) -> bool:
        """Tworzy nowy składnik"""
        try:
            with self.get_connection() as conn:
                # Konwertuj listy/dicts na JSON
                benefits = json.dumps(kwargs.get('benefits', []))
                nutrition = json.dumps(kwargs.get('nutrition', {}))
                allergens = json.dumps(kwargs.get('allergens', []))
                
                conn.execute("""
                    INSERT INTO ingredients (id, name, category_id, price, unit, description, 
                                           benefits, nutrition, allergens, is_organic, is_available)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (id, name, category_id, price, kwargs.get('unit', 'g'), 
                     kwargs.get('description', ''), benefits, nutrition, allergens,
                     kwargs.get('is_organic', False), kwargs.get('is_available', True)))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_ingredients(self, category_id: str = None, available_only: bool = True) -> List[Dict]:
        """Pobiera składniki"""
        with self.get_connection() as conn:
            query = "SELECT * FROM ingredients"
            params = []
            
            conditions = []
            if category_id:
                conditions.append("category_id = ?")
                params.append(category_id)
            if available_only:
                conditions.append("is_available = 1")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY name"
            
            rows = conn.execute(query, params)
            ingredients = []
            for row in rows.fetchall():
                ingredient = dict(row)
                # Parse JSON fields
                try:
                    ingredient['benefits'] = json.loads(ingredient['benefits']) if ingredient['benefits'] else []
                    ingredient['nutrition'] = json.loads(ingredient['nutrition']) if ingredient['nutrition'] else {}
                    ingredient['allergens'] = json.loads(ingredient['allergens']) if ingredient['allergens'] else []
                except json.JSONDecodeError:
                    pass
                ingredients.append(ingredient)
            return ingredients
    
    # =========================
    # PRZEPISY
    # =========================
    
    def create_recipe(self, id: str, name: str, category_id: str = None, 
                     price: float = 0.0, **kwargs) -> bool:
        """Tworzy nowy przepis"""
        try:
            with self.get_connection() as conn:
                # Konwertuj listy na JSON
                tags = json.dumps(kwargs.get('tags', []))
                instructions = json.dumps(kwargs.get('instructions', []))
                tips = json.dumps(kwargs.get('tips', []))
                
                conn.execute("""
                    INSERT INTO recipes (id, name, category_id, description, long_description, price,
                                       calories, protein, carbs, fat, fiber, sugar, health_score,
                                       prep_time, difficulty, tags, instructions, tips, image_url,
                                       is_featured, is_available)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (id, name, category_id, kwargs.get('description', ''), 
                     kwargs.get('long_description', ''), price,
                     kwargs.get('calories', 0), kwargs.get('protein', 0.0), 
                     kwargs.get('carbs', 0.0), kwargs.get('fat', 0.0),
                     kwargs.get('fiber', 0.0), kwargs.get('sugar', 0.0),
                     kwargs.get('health_score', 0), kwargs.get('prep_time', 0),
                     kwargs.get('difficulty', 'easy'), tags, instructions, tips,
                     kwargs.get('image_url', ''), kwargs.get('is_featured', False),
                     kwargs.get('is_available', True)))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_recipes(self, category_id: str = None, available_only: bool = True, 
                   featured_only: bool = False) -> List[Dict]:
        """Pobiera przepisy"""
        with self.get_connection() as conn:
            query = """
                SELECT r.*, c.name as category_name
                FROM recipes r
                LEFT JOIN categories c ON r.category_id = c.id
            """
            params = []
            conditions = []
            
            if category_id:
                conditions.append("r.category_id = ?")
                params.append(category_id)
            if available_only:
                conditions.append("r.is_available = 1")
            if featured_only:
                conditions.append("r.is_featured = 1")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY r.popularity_score DESC, r.name"
            
            rows = conn.execute(query, params)
            recipes = []
            for row in rows.fetchall():
                recipe = dict(row)
                # Parse JSON fields
                try:
                    recipe['tags'] = json.loads(recipe['tags']) if recipe['tags'] else []
                    recipe['instructions'] = json.loads(recipe['instructions']) if recipe['instructions'] else []
                    recipe['tips'] = json.loads(recipe['tips']) if recipe['tips'] else []
                except json.JSONDecodeError:
                    pass
                
                # Pobierz składniki przepisu
                recipe['ingredients'] = self.get_recipe_ingredients(recipe['id'])
                recipes.append(recipe)
            return recipes
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        """Pobiera pojedynczy przepis"""
        recipes = self.get_recipes()
        for recipe in recipes:
            if recipe['id'] == recipe_id:
                return recipe
        return None
    
    def add_ingredient_to_recipe(self, recipe_id: str, ingredient_id: str, 
                                amount: float = 0.0, unit: str = 'g', 
                                is_required: bool = True) -> bool:
        """Dodaje składnik do przepisu"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO recipe_ingredients 
                    (recipe_id, ingredient_id, amount, unit, is_required)
                    VALUES (?, ?, ?, ?, ?)
                """, (recipe_id, ingredient_id, amount, unit, is_required))
                conn.commit()
                return True
        except sqlite3.Error:
            return False
    
    def get_recipe_ingredients(self, recipe_id: str) -> List[Dict]:
        """Pobiera składniki przepisu"""
        with self.get_connection() as conn:
            rows = conn.execute("""
                SELECT ri.*, i.name, i.price, i.unit as ingredient_unit, i.description
                FROM recipe_ingredients ri
                JOIN ingredients i ON ri.ingredient_id = i.id
                WHERE ri.recipe_id = ?
                ORDER BY ri.is_required DESC, i.name
            """, (recipe_id,))
            return [dict(row) for row in rows.fetchall()]
    
    # =========================
    # UŻYTKOWNICY I LOYALTY
    # =========================
    
    def create_user(self, id: str, name: str, email: str = None) -> bool:
        """Tworzy nowego użytkownika"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO users (id, name, email)
                    VALUES (?, ?, ?)
                """, (id, name, email))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Pobiera użytkownika"""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(row) if row else None
    
    def update_user_loyalty(self, user_id: str, points_delta: int = 0, 
                           orders_delta: int = 0, spent_delta: float = 0.0) -> bool:
        """Aktualizuje punkty lojalnościowe użytkownika"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    UPDATE users 
                    SET loyalty_points = loyalty_points + ?,
                        total_orders = total_orders + ?,
                        total_spent = total_spent + ?,
                        last_activity = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (points_delta, orders_delta, spent_delta, user_id))
                conn.commit()
                return True
        except sqlite3.Error:
            return False
    
    # =========================
    # ZAMÓWIENIA
    # =========================
    
    def create_order(self, user_id: str, recipe_id: str = None, 
                    total_price: float = 0.0, **kwargs) -> str:
        """Tworzy nowe zamówienie"""
        import uuid
        order_id = str(uuid.uuid4())[:8]
        
        try:
            with self.get_connection() as conn:
                custom_ingredients = json.dumps(kwargs.get('custom_ingredients', []))
                
                conn.execute("""
                    INSERT INTO orders (id, user_id, recipe_id, total_price, total_calories,
                                      qr_code, custom_ingredients, special_instructions,
                                      estimated_prep_time, machine_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (order_id, user_id, recipe_id, total_price, 
                     kwargs.get('total_calories', 0), kwargs.get('qr_code', order_id),
                     custom_ingredients, kwargs.get('special_instructions', ''),
                     kwargs.get('estimated_prep_time', 5), kwargs.get('machine_id', 'VM001')))
                conn.commit()
                return order_id
        except sqlite3.Error:
            return None
    
    def get_orders(self, user_id: str = None, status: str = None, 
                  limit: int = None) -> List[Dict]:
        """Pobiera zamówienia"""
        with self.get_connection() as conn:
            query = """
                SELECT o.*, u.name as user_name, r.name as recipe_name
                FROM orders o
                LEFT JOIN users u ON o.user_id = u.id
                LEFT JOIN recipes r ON o.recipe_id = r.id
            """
            params = []
            conditions = []
            
            if user_id:
                conditions.append("o.user_id = ?")
                params.append(user_id)
            if status:
                conditions.append("o.status = ?")
                params.append(status)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY o.created_at DESC"
            
            if limit:
                query += f" LIMIT {limit}"
            
            rows = conn.execute(query, params)
            orders = []
            for row in rows.fetchall():
                order = dict(row)
                try:
                    order['custom_ingredients'] = json.loads(order['custom_ingredients']) if order['custom_ingredients'] else []
                except json.JSONDecodeError:
                    order['custom_ingredients'] = []
                orders.append(order)
            return orders

# Singleton instance
db = IkigaiDatabase() 