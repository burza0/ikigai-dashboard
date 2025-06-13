#!/usr/bin/env python3
"""
Inicjalizacja bazy danych IKIGAI Dashboard
Tworzy tablice i dodaje dane demo
"""

import sqlite3
import hashlib
import os

def hash_password(password):
    """Hashuje hasło za pomocą SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Inicjalizuje bazę danych IKIGAI"""
    db_path = os.path.join(os.path.dirname(__file__), 'ikigai.db')
    
    # Usuń starą bazę jeśli istnieje
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Usunięto starą bazę danych")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🏗️ Tworzenie tabel...")
    
    # Tabela użytkowników z autentykacją
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_active INTEGER DEFAULT 1,
            loyalty_points INTEGER DEFAULT 0,
            total_orders INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela przepisów
    cursor.execute('''
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            ingredients TEXT,
            price REAL,
            calories INTEGER,
            protein INTEGER,
            health_score INTEGER,
            prep_time INTEGER,
            is_available INTEGER DEFAULT 1,
            is_featured INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela składników
    cursor.execute('''
        CREATE TABLE ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            type TEXT,
            price REAL,
            nutrition TEXT,
            is_available INTEGER DEFAULT 1,
            is_organic INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela zamówień
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            recipe_name TEXT,
            total_price REAL,
            status TEXT DEFAULT 'pending',
            qr_code TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    print("👤 Dodawanie użytkowników demo...")
    
    # Użytkownicy demo
    users_data = [
        ('admin', 'admin@ikigai.com', 'Administrator IKIGAI', hash_password('admin123'), 'admin', 1, 10000, 50, 1250.0),
        ('web_user', 'user@ikigai.com', 'Demo User IKIGAI', hash_password('demo123'), 'user', 1, 2847, 15, 247.50)
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, email, name, password_hash, role, is_active, loyalty_points, total_orders, total_spent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)
    
    print("🍜 Dodawanie przepisów demo...")
    
    # Przepisy demo
    recipes_data = [
        ('Energetyczny Start Dnia', 'breakfast', 'Idealna mieszanka na poranną energię', 
         '["spirulina_powder", "protein_vanilla", "coconut_water", "chia_seeds"]', 16.60, 320, 25, 94, 3, 1, 1),
        ('Detox Green Morning', 'detox', 'Oczyszczająca zielona mieszanka',
         '["spirulina_powder", "matcha_premium", "coconut_water", "goji_berries"]', 21.00, 180, 12, 98, 3, 1, 1),
        ('Power Protein Bowl', 'fitness', 'Maksymalna dawka białka',
         '["protein_vanilla", "protein_chocolate", "chia_seeds", "coconut_water"]', 18.30, 410, 35, 91, 3, 1, 0),
        ('Brain Boost Focus', 'cognitive', 'Mieszanka na koncentrację',
         '["matcha_premium", "goji_berries", "chia_seeds", "coconut_water"]', 19.40, 250, 8, 89, 3, 1, 0),
        ('Recovery & Zen', 'recovery', 'Regeneracja po treningu',
         '["protein_vanilla", "spirulina_powder", "goji_berries", "coconut_water"]', 17.80, 290, 22, 92, 3, 1, 0)
    ]
    
    cursor.executemany('''
        INSERT INTO recipes (name, category, description, ingredients, price, calories, protein, health_score, prep_time, is_available, is_featured)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', recipes_data)
    
    print("🧪 Dodawanie składników demo...")
    
    # Składniki demo
    ingredients_data = [
        ('Spirulina Powder BIO', 'superfoods', 'powder', 4.50, '{"protein": 5, "b12": "high", "iron": "high"}', 1, 1),
        ('Protein Vanilla Premium', 'proteins', 'powder', 8.20, '{"protein": 25, "bcaa": "high"}', 1, 0),
        ('Woda Kokosowa Premium', 'liquids', 'liquid', 5.80, '{"electrolytes": "high", "potassium": "high"}', 1, 1),
        ('Chia Seeds Premium', 'seeds', 'seeds', 3.20, '{"omega3": "high", "fiber": "high"}', 1, 1),
        ('Matcha Premium Grade A', 'traditional', 'powder', 6.20, '{"antioxidants": "very_high", "caffeine": "medium"}', 1, 1),
        ('Goji Berries Organic', 'superfoods', 'dried_fruit', 7.40, '{"vitamin_c": "very_high", "antioxidants": "high"}', 1, 1),
        ('Protein Chocolate Premium', 'proteins', 'powder', 8.50, '{"protein": 24, "magnesium": "high"}', 1, 0)
    ]
    
    cursor.executemany('''
        INSERT INTO ingredients (name, category, type, price, nutrition, is_available, is_organic)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ingredients_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Baza danych została utworzona pomyślnie!")
    print(f"📍 Lokalizacja: {db_path}")
    print("\n👥 Konta demo:")
    print("🔑 Admin: admin / admin123")
    print("👤 User: web_user / demo123")

if __name__ == '__main__':
    init_database() 
"""
Inicjalizacja bazy danych IKIGAI Dashboard
Tworzy tablice i dodaje dane demo
"""

import sqlite3
import hashlib
import os

def hash_password(password):
    """Hashuje hasło za pomocą SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Inicjalizuje bazę danych IKIGAI"""
    db_path = os.path.join(os.path.dirname(__file__), 'ikigai.db')
    
    # Usuń starą bazę jeśli istnieje
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Usunięto starą bazę danych")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🏗️ Tworzenie tabel...")
    
    # Tabela użytkowników z autentykacją
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_active INTEGER DEFAULT 1,
            loyalty_points INTEGER DEFAULT 0,
            total_orders INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela przepisów
    cursor.execute('''
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            ingredients TEXT,
            price REAL,
            calories INTEGER,
            protein INTEGER,
            health_score INTEGER,
            prep_time INTEGER,
            is_available INTEGER DEFAULT 1,
            is_featured INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela składników
    cursor.execute('''
        CREATE TABLE ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            type TEXT,
            price REAL,
            nutrition TEXT,
            is_available INTEGER DEFAULT 1,
            is_organic INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela zamówień
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            recipe_name TEXT,
            total_price REAL,
            status TEXT DEFAULT 'pending',
            qr_code TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    print("👤 Dodawanie użytkowników demo...")
    
    # Użytkownicy demo
    users_data = [
        ('admin', 'admin@ikigai.com', 'Administrator IKIGAI', hash_password('admin123'), 'admin', 1, 10000, 50, 1250.0),
        ('web_user', 'user@ikigai.com', 'Demo User IKIGAI', hash_password('demo123'), 'user', 1, 2847, 15, 247.50)
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, email, name, password_hash, role, is_active, loyalty_points, total_orders, total_spent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)
    
    print("🍜 Dodawanie przepisów demo...")
    
    # Przepisy demo
    recipes_data = [
        ('Energetyczny Start Dnia', 'breakfast', 'Idealna mieszanka na poranną energię', 
         '["spirulina_powder", "protein_vanilla", "coconut_water", "chia_seeds"]', 16.60, 320, 25, 94, 3, 1, 1),
        ('Detox Green Morning', 'detox', 'Oczyszczająca zielona mieszanka',
         '["spirulina_powder", "matcha_premium", "coconut_water", "goji_berries"]', 21.00, 180, 12, 98, 3, 1, 1),
        ('Power Protein Bowl', 'fitness', 'Maksymalna dawka białka',
         '["protein_vanilla", "protein_chocolate", "chia_seeds", "coconut_water"]', 18.30, 410, 35, 91, 3, 1, 0),
        ('Brain Boost Focus', 'cognitive', 'Mieszanka na koncentrację',
         '["matcha_premium", "goji_berries", "chia_seeds", "coconut_water"]', 19.40, 250, 8, 89, 3, 1, 0),
        ('Recovery & Zen', 'recovery', 'Regeneracja po treningu',
         '["protein_vanilla", "spirulina_powder", "goji_berries", "coconut_water"]', 17.80, 290, 22, 92, 3, 1, 0)
    ]
    
    cursor.executemany('''
        INSERT INTO recipes (name, category, description, ingredients, price, calories, protein, health_score, prep_time, is_available, is_featured)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', recipes_data)
    
    print("🧪 Dodawanie składników demo...")
    
    # Składniki demo
    ingredients_data = [
        ('Spirulina Powder BIO', 'superfoods', 'powder', 4.50, '{"protein": 5, "b12": "high", "iron": "high"}', 1, 1),
        ('Protein Vanilla Premium', 'proteins', 'powder', 8.20, '{"protein": 25, "bcaa": "high"}', 1, 0),
        ('Woda Kokosowa Premium', 'liquids', 'liquid', 5.80, '{"electrolytes": "high", "potassium": "high"}', 1, 1),
        ('Chia Seeds Premium', 'seeds', 'seeds', 3.20, '{"omega3": "high", "fiber": "high"}', 1, 1),
        ('Matcha Premium Grade A', 'traditional', 'powder', 6.20, '{"antioxidants": "very_high", "caffeine": "medium"}', 1, 1),
        ('Goji Berries Organic', 'superfoods', 'dried_fruit', 7.40, '{"vitamin_c": "very_high", "antioxidants": "high"}', 1, 1),
        ('Protein Chocolate Premium', 'proteins', 'powder', 8.50, '{"protein": 24, "magnesium": "high"}', 1, 0)
    ]
    
    cursor.executemany('''
        INSERT INTO ingredients (name, category, type, price, nutrition, is_available, is_organic)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ingredients_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Baza danych została utworzona pomyślnie!")
    print(f"📍 Lokalizacja: {db_path}")
    print("\n👥 Konta demo:")
    print("🔑 Admin: admin / admin123")
    print("👤 User: web_user / demo123")

if __name__ == '__main__':
    init_database() 