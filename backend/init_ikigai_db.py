#!/usr/bin/env python3
"""
🗄️ IKIGAI Database Initializer
Inicjalizuje bazę danych SQLite dla aplikacji IKIGAI
"""

import sqlite3
import json
import os
from datetime import datetime

# Ścieżka do bazy danych
DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')

def init_database():
    """Inicjalizuje bazę danych i tworzy tabele"""
    print("🗄️ Inicjalizuję bazę danych IKIGAI...")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
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
            badges TEXT, -- JSON array
            member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    
    # Indeksy dla wydajności
    conn.execute("CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes (category_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ingredients_category ON ingredients (category_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_user ON orders (user_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_created ON orders (created_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_loyalty ON users (loyalty_level, loyalty_points)")
    
    conn.commit()
    conn.close()
    
    print("✅ Baza danych utworzona")
    return True

def populate_sample_data():
    """Wypełnia bazę przykładowymi danymi z aplikacji"""
    print("📊 Wypełniam bazę przykładowymi danymi...")
    
    conn = sqlite3.connect(DB_PATH)
    
    # Kategorie przepisów
    recipe_categories = [
        ("breakfast", "Śniadanie", "Energetyczne poranki", "🌅", "#ff6b35", "recipe"),
        ("detox", "Detox", "Oczyszczanie organizmu", "🌿", "#4ecdc4", "recipe"),
        ("fitness", "Fitness", "Sport i siła", "💪", "#ff6b6b", "recipe"),
        ("cognitive", "Koncentracja", "Wsparcie mózgu", "🧠", "#4ecdc4", "recipe"),
        ("recovery", "Regeneracja", "Odpoczynek i odnowa", "🧘‍♀️", "#a8e6cf", "recipe"),
    ]
    
    for cat in recipe_categories:
        conn.execute("""
            INSERT OR REPLACE INTO categories (id, name, description, icon, color, type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, cat)
    
    # Kategorie składników
    ingredient_categories = [
        ("superfoods", "Superfoods", "Najlepsze składniki natury", "⭐", "#ff6b35", "ingredient"),
        ("proteins", "Białka", "Budowa mięśni", "💪", "#ff6b6b", "ingredient"),
        ("fruits", "Owoce", "Naturalne witaminy", "🍓", "#4ecdc4", "ingredient"),
        ("seeds", "Nasiona", "Omega-3 i błonnik", "🌱", "#a8e6cf", "ingredient"),
    ]
    
    for cat in ingredient_categories:
        conn.execute("""
            INSERT OR REPLACE INTO categories (id, name, description, icon, color, type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, cat)
    
    # Składniki
    ingredients = [
        ("spirulina_powder", "Spirulina Powder BIO", "superfoods", 4.50, "g", "Najlepsze źródło B12", 
         json.dumps(["Witamina B12", "Żelazo", "Białko kompletne"]), json.dumps({"protein": 60, "iron": 28})),
        ("protein_vanilla", "Protein Vanilla Premium", "proteins", 5.20, "g", "Wysokiej jakości białko", 
         json.dumps(["Budowa mięśni", "Długotrwała sytość"]), json.dumps({"protein": 80, "carbs": 5})),
        ("coconut_water", "Woda Kokosowa Premium", "fruits", 3.80, "ml", "Naturalne elektrolity", 
         json.dumps(["Elektrolity", "Nawodnienie", "Potas"]), json.dumps({"potassium": 600, "sodium": 105})),
        ("chia_seeds", "Chia Seeds Premium", "seeds", 3.20, "g", "Bogate w omega-3", 
         json.dumps(["Omega-3", "Błonnik", "Magnez"]), json.dumps({"omega3": 17, "fiber": 34})),
        ("matcha_premium", "Matcha Premium Grade A", "superfoods", 6.20, "g", "Najwyższej jakości matcha", 
         json.dumps(["L-teanina", "Antyoksydanty", "Kofeina"]), json.dumps({"caffeine": 70, "antioxidants": 1300})),
        ("goji_berries", "Goji Berries Organic", "fruits", 4.80, "g", "Superfruit z Tybetu", 
         json.dumps(["Antyoksydanty", "Witamina C", "Żelazo"]), json.dumps({"vitamin_c": 48, "iron": 6.8})),
    ]
    
    for ing in ingredients:
        conn.execute("""
            INSERT OR REPLACE INTO ingredients 
            (id, name, category_id, price, unit, description, benefits, nutrition)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ing)
    
    # Przepisy
    recipes = [
        ("energetic_morning", "Energetyczny Start Dnia", "breakfast", "Idealna mieszanka na poranną energię", 
         16.60, 320, 25, 18, 12, 8, 6, 94, 3, "easy", 
         json.dumps(["high-protein", "energizing", "superfood"]), True),
        ("detox_green", "Detox Green Morning", "detox", "Oczyszczająca zielona mieszanka", 
         21.00, 180, 12, 24, 6, 5, 8, 98, 3, "easy", 
         json.dumps(["detox", "antioxidants", "green"]), True),
        ("protein_power", "Power Protein Bowl", "fitness", "Maksymalna dawka białka", 
         18.30, 410, 35, 12, 18, 3, 4, 91, 3, "medium", 
         json.dumps(["high-protein", "muscle-building", "post-workout"]), True),
        ("brain_boost", "Brain Boost Focus", "cognitive", "Mieszanka na koncentrację", 
         19.40, 250, 8, 32, 9, 6, 12, 89, 3, "easy", 
         json.dumps(["focus", "brain-health", "antioxidants"]), False),
        ("recovery_zen", "Recovery & Zen", "recovery", "Regeneracja po treningu", 
         17.80, 290, 22, 20, 10, 4, 8, 92, 3, "easy", 
         json.dumps(["recovery", "anti-inflammatory", "calming"]), False),
    ]
    
    for recipe in recipes:
        conn.execute("""
            INSERT OR REPLACE INTO recipes 
            (id, name, category_id, description, price, calories, protein, carbs, fat, 
             fiber, sugar, health_score, prep_time, difficulty, tags, is_featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, recipe)
    
    # Składniki w przepisach
    recipe_ingredients = [
        ("energetic_morning", "spirulina_powder", 5.0, "g"),
        ("energetic_morning", "protein_vanilla", 25.0, "g"),
        ("energetic_morning", "coconut_water", 250.0, "ml"),
        ("energetic_morning", "chia_seeds", 15.0, "g"),
        
        ("detox_green", "spirulina_powder", 3.0, "g"),
        ("detox_green", "matcha_premium", 2.0, "g"),
        ("detox_green", "coconut_water", 200.0, "ml"),
        ("detox_green", "goji_berries", 10.0, "g"),
        
        ("protein_power", "protein_vanilla", 30.0, "g"),
        ("protein_power", "chia_seeds", 20.0, "g"),
        ("protein_power", "coconut_water", 300.0, "ml"),
        
        ("brain_boost", "matcha_premium", 3.0, "g"),
        ("brain_boost", "goji_berries", 15.0, "g"),
        ("brain_boost", "chia_seeds", 10.0, "g"),
        ("brain_boost", "coconut_water", 250.0, "ml"),
        
        ("recovery_zen", "protein_vanilla", 20.0, "g"),
        ("recovery_zen", "spirulina_powder", 3.0, "g"),
        ("recovery_zen", "goji_berries", 12.0, "g"),
        ("recovery_zen", "coconut_water", 250.0, "ml"),
    ]
    
    for ri in recipe_ingredients:
        conn.execute("""
            INSERT OR REPLACE INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit)
            VALUES (?, ?, ?, ?)
        """, ri)
    
    # Przykładowy użytkownik
    conn.execute("""
        INSERT OR REPLACE INTO users 
        (id, name, email, loyalty_level, loyalty_points, total_orders, total_spent, badges, member_since)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("web_user", "IKIGAI Enthusiast", "user@example.com", 3, 2847, 47, 892.40, 
          json.dumps([
              {"id": "first_order", "name": "Pierwszy Krok", "description": "Pierwsze zamówienie w IKIGAI", "earned_date": "2024-03-15", "rarity": "common"},
              {"id": "week_streak", "name": "Tygodniowy Streak", "description": "7 dni z rzędu zdrowych wyborów", "earned_date": "2024-05-22", "rarity": "rare"},
              {"id": "eco_warrior", "name": "Eco Warrior", "description": "25 ekologicznych składników", "earned_date": "2024-06-01", "rarity": "epic"}
          ]), "2024-03-15"))
    
    # Wyzwania lojalnościowe
    challenges = [
        ("daily_protein", "Protein Power", "Zamów mieszankę z dodatkiem białka", "daily", 1, 50, "easy", "💪", "2024-06-13 23:59:59"),
        ("weekly_variety", "Różnorodność Smaków", "Spróbuj 5 różnych składników w tym tygodniu", "weekly", 5, 200, "medium", "🌈", "2024-06-16 23:59:59"),
        ("monthly_eco", "Eco Champion", "20 zamówień z lokalnymi składnikami", "monthly", 20, 500, "hard", "🌱", "2024-06-30 23:59:59"),
    ]
    
    for challenge in challenges:
        conn.execute("""
            INSERT OR REPLACE INTO loyalty_challenges 
            (id, name, description, type, target, reward_points, difficulty, icon, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, challenge)
    
    # Postęp użytkownika w wyzwaniach
    user_progress = [
        ("web_user", "daily_protein", 1, "completed", "2024-06-12 08:30:00"),
        ("web_user", "weekly_variety", 3, "active", None),
        ("web_user", "monthly_eco", 14, "active", None),
    ]
    
    for progress in user_progress:
        conn.execute("""
            INSERT OR REPLACE INTO user_challenge_progress 
            (user_id, challenge_id, progress, status, completed_at)
            VALUES (?, ?, ?, ?, ?)
        """, progress)
    
    # Nagrody lojalnościowe
    rewards = [
        ("free_small", "Darmowa Mała Mieszanka", "Wybierz dowolną mieszankę do 20zł", 500, "freebies", "🎁"),
        ("free_premium", "Darmowa Premium Mieszanka", "Dowolna mieszanka bez limitu ceny", 1000, "freebies", "💎"),
        ("discount_20", "20% Zniżka", "20% zniżki na następne 3 zamówienia", 750, "discounts", "💸"),
        ("ikigai_bottle", "IKIGAI Eco Bottle", "Bambusowa butelka z logo IKIGAI", 2000, "merchandise", "🍶"),
        ("nutrition_guide", "Personal Nutrition Guide", "Konsultacja z dietetykiem (30 min)", 3000, "services", "👨‍⚕️"),
    ]
    
    for reward in rewards:
        conn.execute("""
            INSERT OR REPLACE INTO loyalty_rewards (id, name, description, cost, category, icon)
            VALUES (?, ?, ?, ?, ?, ?)
        """, reward)
    
    conn.commit()
    conn.close()
    
    print("✅ Przykładowe dane dodane")
    return True

if __name__ == "__main__":
    print("🗄️ IKIGAI Database Setup")
    print("=" * 40)
    
    # Usuń starą bazę jeśli istnieje
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Stara baza usunięta")
    
    # Utwórz nową bazę
    init_database()
    populate_sample_data()
    
    print(f"\n✅ Baza danych IKIGAI gotowa!")
    print(f"📁 Plik: {DB_PATH}")
    if os.path.exists(DB_PATH):
        print(f"📏 Rozmiar: {os.path.getsize(DB_PATH)} bytes")
    print("\n🚀 Możesz teraz uruchomić serwer z bazą danych!") 