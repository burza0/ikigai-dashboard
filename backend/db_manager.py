#!/usr/bin/env python3
"""
🗄️ IKIGAI Database Manager
Uniwersalny system obsługi baz danych: SQLite (lokalnie) + PostgreSQL (Heroku)
"""

import os
import sqlite3
import json
from contextlib import contextmanager

# Sprawdź typ bazy danych
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # PostgreSQL na Heroku
    print("🐘 Wykryto PostgreSQL na Heroku")
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    try:
        import psycopg2
        import psycopg2.extras
        DB_TYPE = 'postgresql'
        DB_PATH = DATABASE_URL
        DB_AVAILABLE = True
        print(f"✅ PostgreSQL połączone: {DATABASE_URL.split('@')[1].split('/')[0]}")
    except ImportError:
        print("❌ Brak psycopg2 - nie można połączyć z PostgreSQL")
        DB_TYPE = 'sqlite'
        DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')
        DB_AVAILABLE = os.path.exists(DB_PATH)
else:
    # SQLite lokalnie
    print("🗃️ Używam lokalnej bazy SQLite")
    DB_TYPE = 'sqlite'
    DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')
    DB_AVAILABLE = os.path.exists(DB_PATH)
    if DB_AVAILABLE:
        print(f"✅ SQLite dostępne: {DB_PATH}")
    else:
        print(f"⚠️ SQLite niedostępne: {DB_PATH}")

@contextmanager
def get_db_connection():
    """Universal database connection context manager"""
    if not DB_AVAILABLE:
        yield None
        return
        
    conn = None
    try:
        if DB_TYPE == 'postgresql':
            conn = psycopg2.connect(DATABASE_URL)
            conn.autocommit = False  # Manual transaction control
            yield conn
        else:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            yield conn
    except Exception as e:
        print(f"❌ Błąd połączenia z bazą {DB_TYPE}: {e}")
        if conn:
            conn.rollback()
        yield None
    finally:
        if conn:
            conn.close()

def execute_query(query, params=None, fetch_type='all'):
    """Execute query with universal result handling"""
    with get_db_connection() as conn:
        if not conn:
            return None
            
        try:
            if DB_TYPE == 'postgresql':
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(query, params or ())
                
                if fetch_type == 'one':
                    result = cursor.fetchone()
                elif fetch_type == 'all':
                    result = cursor.fetchall()
                else:
                    result = cursor
                    
                conn.commit()
                return result
            else:
                cursor = conn.execute(query, params or ())
                
                if fetch_type == 'one':
                    return cursor.fetchone()
                elif fetch_type == 'all':
                    return cursor.fetchall()
                else:
                    return cursor
                    
        except Exception as e:
            print(f"❌ Błąd zapytania SQL: {e}")
            conn.rollback()
            return None

def create_tables_postgresql():
    """Create PostgreSQL tables from SQLite schema"""
    if DB_TYPE != 'postgresql':
        return False
        
    print("🏗️ Tworzenie tabel PostgreSQL...")
    
    # SQL do tworzenia tabel w PostgreSQL (konwersja z SQLite)
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS categories (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            type VARCHAR(50),
            icon VARCHAR(100),
            color VARCHAR(20)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ingredients (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category_id VARCHAR(50),
            price DECIMAL(10,2),
            unit VARCHAR(20),
            description TEXT,
            benefits JSONB,
            is_organic BOOLEAN DEFAULT FALSE,
            is_available BOOLEAN DEFAULT TRUE,
            stock_level INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category_id VARCHAR(50),
            description TEXT,
            long_description TEXT,
            calories INTEGER,
            protein INTEGER,
            carbs INTEGER,
            fat INTEGER,
            fiber INTEGER,
            sugar INTEGER,
            health_score INTEGER,
            prep_time INTEGER,
            price DECIMAL(10,2),
            difficulty VARCHAR(50),
            tags JSONB,
            instructions JSONB,
            tips JSONB,
            is_featured BOOLEAN DEFAULT FALSE,
            is_available BOOLEAN DEFAULT TRUE,
            popularity_score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(50),
            loyalty_level INTEGER DEFAULT 1,
            loyalty_points INTEGER DEFAULT 0,
            total_orders INTEGER DEFAULT 0,
            total_spent DECIMAL(10,2) DEFAULT 0.00,
            password_hash VARCHAR(255),
            role VARCHAR(50) DEFAULT 'user',
            is_active BOOLEAN DEFAULT TRUE,
            reset_token VARCHAR(255),
            login_attempts INTEGER DEFAULT 0,
            last_login TIMESTAMP,
            member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            badges JSONB,
            favorite_recipe_id VARCHAR(50)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id VARCHAR(50) PRIMARY KEY,
            user_id VARCHAR(50),
            recipe_id VARCHAR(50),
            mixture_name VARCHAR(255),
            total_price DECIMAL(10,2),
            status VARCHAR(50) DEFAULT 'pending',
            vending_machine_id VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        );
        """
    ]
    
    try:
        with get_db_connection() as conn:
            if not conn:
                return False
                
            cursor = conn.cursor()
            for sql in tables_sql:
                cursor.execute(sql)
            conn.commit()
            print("✅ Tabele PostgreSQL utworzone")
            return True
    except Exception as e:
        print(f"❌ Błąd tworzenia tabel PostgreSQL: {e}")
        return False

def insert_sample_data():
    """Insert sample data for PostgreSQL"""
    if DB_TYPE != 'postgresql':
        return False
        
    print("📝 Dodawanie przykładowych danych...")
    
    # Sprawdź czy dane już istnieją
    existing_recipes = execute_query("SELECT COUNT(*) FROM recipes", fetch_type='one')
    if existing_recipes and existing_recipes[0] > 0:
        print("✅ Dane już istnieją w PostgreSQL")
        return True
    
    try:
        # Kategorie
        categories = [
            ('breakfast', 'Śniadanie', 'Energetyczny start dnia', 'recipe', '🌅', '#ff9800'),
            ('detox', 'Detox', 'Oczyszczanie organizmu', 'recipe', '🌿', '#4caf50'),
            ('workout', 'Trening', 'Wsparcie treningu', 'recipe', '💪', '#f44336'),
            ('proteins', 'Białka', 'Białka i aminokwasy', 'ingredient', '🥩', '#9c27b0'),
            ('superfoods', 'Superfoods', 'Składniki o wyjątkowych właściwościach', 'ingredient', '⭐', '#2196f3')
        ]
        
        # Składniki
        ingredients = [
            ('spirulina_powder', 'Spirulina Powder BIO', 'superfoods', 4.50, 'g', 'Alga spirulina bogata w białko', '["witamina B12", "żelazo", "białko"]', True),
            ('protein_vanilla', 'Protein Vanilla Premium', 'proteins', 8.20, 'g', 'Białko waniliowe najwyższej jakości', '["budowa mięśni", "regeneracja"]', False),
            ('coconut_water', 'Woda Kokosowa Premium', 'liquids', 5.80, 'ml', 'Naturalna woda kokosowa', '["elektrolity", "nawodnienie"]', True),
            ('chia_seeds', 'Chia Seeds Premium', 'superfoods', 3.20, 'g', 'Nasiona chia bogate w omega-3', '["omega-3", "błonnik", "magnez"]', True)
        ]
        
        # Przepisy
        recipes = [
            ('energetic_morning', 'Energetyczny Start Dnia', 'breakfast', 'Idealny boost energii', 'Pełnowartościowy posiłek', 385, 25, 35, 12, 8, 15, 94, 3, 16.60, 'łatwy', '["wysokobiałkowy", "energetyczny"]', '["Dodaj spirulinę", "Wlej wodę", "Wymieszaj"]', '["Spożyj w 30 min"]', True, 95),
            ('detox_green', 'Detox Green Morning', 'detox', 'Oczyszczający shake', 'Zielone superfoods', 320, 18, 28, 8, 12, 10, 98, 4, 21.00, 'średni', '["detox", "zielony"]', '["Mix składniki", "Podawaj schłodzone"]', '["Pij rano"]', True, 89)
        ]
        
        # Użytkownicy  
        users = [
            ('web_user', 'Demo User', 'demo@ikigai.com', '+48 123 456 789', 2, 2847, 15, 247.50, None, 'user', True),
            ('admin', 'Administrator', 'admin@ikigai.com', '+48 987 654 321', 5, 10000, 0, 0.00, None, 'admin', True)
        ]
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Dodaj kategorie
            for cat in categories:
                cursor.execute("""
                    INSERT INTO categories (id, name, description, type, icon, color)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, cat)
            
            # Dodaj składniki
            for ing in ingredients:
                cursor.execute("""
                    INSERT INTO ingredients (id, name, category_id, price, unit, description, benefits, is_organic)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, ing)
            
            # Dodaj przepisy
            for recipe in recipes:
                cursor.execute("""
                    INSERT INTO recipes (id, name, category_id, description, long_description, calories, protein, carbs, fat, fiber, sugar, health_score, prep_time, price, difficulty, tags, instructions, tips, is_featured, popularity_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, recipe)
            
            # Dodaj użytkowników
            for user in users:
                cursor.execute("""
                    INSERT INTO users (id, name, email, phone, loyalty_level, loyalty_points, total_orders, total_spent, password_hash, role, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, user)
                
            conn.commit()
            print("✅ Przykładowe dane dodane do PostgreSQL")
            return True
            
    except Exception as e:
        print(f"❌ Błąd dodawania danych: {e}")
        return False

def setup_database():
    """Setup database (create tables and insert data)"""
    if DB_TYPE == 'postgresql':
        print("🚀 Konfiguracja PostgreSQL...")
        if create_tables_postgresql():
            insert_sample_data()
            return True
    else:
        print("✅ SQLite nie wymaga dodatkowej konfiguracji")
        return True
    return False

def setup_postgresql():
    """Setup PostgreSQL tables"""
    if DB_TYPE != 'postgresql':
        return False
        
    print("🏗️ Creating PostgreSQL tables...")
    
    with get_db_connection() as conn:
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(50),
                loyalty_level INTEGER DEFAULT 1,
                loyalty_points INTEGER DEFAULT 0,
                total_orders INTEGER DEFAULT 0,
                total_spent DECIMAL(10,2) DEFAULT 0.00,
                password_hash VARCHAR(255),
                role VARCHAR(50) DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                favorite_recipe_id VARCHAR(50)
            );
        """)
        
        # Insert sample user
        cursor.execute("""
            INSERT INTO users (id, name, email, loyalty_points, total_orders, total_spent, role)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, ('web_user', 'Demo User', 'demo@ikigai.com', 2847, 15, 247.50, 'user'))
        
        conn.commit()
        print("✅ PostgreSQL setup complete")
        return True

if __name__ == "__main__":
    print("🗄️ IKIGAI Database Manager")
    print(f"📊 Typ bazy: {DB_TYPE}")
    print(f"🔗 Dostępność: {'✅' if DB_AVAILABLE else '❌'}")
    
    if DB_TYPE == 'postgresql':
        setup_database()
        setup_postgresql() 