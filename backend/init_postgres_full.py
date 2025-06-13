#!/usr/bin/env python3
"""
🐘 IKIGAI PostgreSQL Database Initializer
Inicjalizuje pełną bazę danych PostgreSQL dla aplikacji IKIGAI na Heroku
"""

import os

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ DATABASE_URL not found. Run this on Heroku or set the variable locally.")
    exit(1)

# Fix postgres:// to postgresql:// for psycopg2
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print("🐘 Initializing full PostgreSQL database for IKIGAI...")

try:
    import psycopg2
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("✅ Connected to PostgreSQL")
    
    # 1. Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            type VARCHAR(20) NOT NULL,
            icon VARCHAR(50),
            color VARCHAR(20)
        );
    """)
    print("✅ Categories table created")
    
    # 2. Users table
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
    print("✅ Users table created")
    
    # 3. Recipes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            long_description TEXT,
            category_id VARCHAR(50),
            calories INTEGER,
            protein INTEGER,
            carbs INTEGER,
            fat INTEGER,
            fiber INTEGER,
            sugar INTEGER,
            health_score INTEGER,
            prep_time INTEGER,
            price DECIMAL(10,2),
            difficulty VARCHAR(20),
            tags TEXT,
            instructions TEXT,
            tips TEXT,
            is_featured BOOLEAN DEFAULT FALSE,
            is_available BOOLEAN DEFAULT TRUE,
            popularity_score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("✅ Recipes table created")
    
    # 4. Ingredients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category_id VARCHAR(50),
            price DECIMAL(10,2),
            unit VARCHAR(20),
            calories_per_100g INTEGER,
            protein_per_100g INTEGER,
            carbs_per_100g INTEGER,
            fat_per_100g INTEGER,
            fiber_per_100g INTEGER,
            description TEXT,
            origin VARCHAR(100),
            is_organic BOOLEAN DEFAULT FALSE,
            is_available BOOLEAN DEFAULT TRUE,
            benefits TEXT,
            allergens TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("✅ Ingredients table created")
    
    # 5. Recipe ingredients (junction table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            id SERIAL PRIMARY KEY,
            recipe_id VARCHAR(50),
            ingredient_id VARCHAR(50),
            amount DECIMAL(10,2),
            unit VARCHAR(20),
            is_required BOOLEAN DEFAULT TRUE,
            preparation_note TEXT
        );
    """)
    print("✅ Recipe ingredients table created")
    
    # 6. Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id VARCHAR(50) PRIMARY KEY,
            user_id VARCHAR(50),
            recipe_id VARCHAR(50),
            status VARCHAR(20) DEFAULT 'pending',
            total_price DECIMAL(10,2),
            payment_method VARCHAR(50),
            machine_id VARCHAR(50),
            qr_code VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            notes TEXT
        );
    """)
    print("✅ Orders table created")
    
    # 7. Loyalty challenges
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loyalty_challenges (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            type VARCHAR(50),
            target INTEGER,
            reward_points INTEGER,
            difficulty VARCHAR(20),
            icon VARCHAR(50),
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("✅ Loyalty challenges table created")
    
    # 8. Loyalty rewards
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loyalty_rewards (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            cost INTEGER NOT NULL,
            category VARCHAR(50),
            icon VARCHAR(50),
            image_url VARCHAR(255),
            popularity INTEGER DEFAULT 0,
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("✅ Loyalty rewards table created")
    
    # 9. User challenge progress
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_challenge_progress (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50),
            challenge_id VARCHAR(50),
            progress INTEGER DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );
    """)
    print("✅ User challenge progress table created")
    
    # Insert sample data
    print("\n📊 Inserting sample data...")
    
    # Categories
    categories_data = [
        ('breakfast', 'Śniadanie', 'Energetyczne posiłki na start dnia', 'recipe', '🌅', '#FF6B35'),
        ('detox', 'Detox', 'Oczyszczające mieszanki', 'recipe', '🌿', '#4ECDC4'),
        ('workout', 'Trening', 'Wsparcie przed i po treningu', 'recipe', '💪', '#45B7D1'),
        ('cognitive', 'Koncentracja', 'Wsparcie funkcji kognitywnych', 'recipe', '🧠', '#96CEB4'),
        ('relaxation', 'Relaks', 'Uspokajające mieszanki', 'recipe', '😌', '#FFEAA7'),
        ('superfoods', 'Superfoods', 'Składniki o wysokiej wartości odżywczej', 'ingredient', '⭐', '#6C5CE7'),
        ('proteins', 'Białka', 'Białka roślinne i zwierzęce', 'ingredient', '🥜', '#A29BFE'),
        ('adaptogens', 'Adaptogeny', 'Naturalne adaptogeny', 'ingredient', '🍄', '#FD79A8'),
        ('vitamins', 'Witaminy', 'Witaminy i minerały', 'ingredient', '💊', '#FDCB6E'),
        ('liquids', 'Płyny bazowe', 'Podstawy płynne do mieszanek', 'ingredient', '🥛', '#74B9FF')
    ]
    
    for cat in categories_data:
        cursor.execute("""
            INSERT INTO categories (id, name, description, type, icon, color)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, cat)
    
    # Sample recipes
    recipes_data = [
        ('energetic_morning', 'Energetyczny Start Dnia', 'Idealny boost energii na start dnia', 
         'Pełnowartościowy posiłek z wysokiej jakości białkami i superfoods', 'breakfast',
         385, 25, 35, 12, 8, 15, 94, 3, 16.60, 'łatwy',
         '["wysokobiałkowy", "energetyczny", "organiczny"]',
         '["Dodaj wszystkie składniki", "Mieszaj 30 sekund", "Podawaj natychmiast"]',
         '["Najlepiej rano na czczo", "Można dodać lód"]', True, True, 95),
        
        ('detox_green', 'Detox Green Morning', 'Oczyszczający zielony shake',
         'Mieszanka zielonych superfoods do detoksykacji organizmu', 'detox',
         320, 18, 28, 8, 12, 10, 98, 4, 21.00, 'średni',
         '["detox", "zielony", "antyoksydanty"]',
         '["Wszystkie składniki do blendera", "Mieszaj intensywnie", "Filtruj opcjonalnie"]',
         '["Pij powoli", "Dodaj cytrynę dla smaku"]', True, True, 89),
        
        ('protein_power', 'Power Protein Bowl', 'Maksymalna dawka białka',
         'Idealny po treningu - wysokie białko i aminokwasy', 'workout',
         420, 35, 30, 15, 6, 12, 91, 3, 18.30, 'łatwy',
         '["post-workout", "wysokobiałkowy", "regeneracja"]',
         '["Protein do shakersa", "Dodaj płyn", "Wstrząsaj energicznie"]',
         '["W ciągu 30 min po treningu", "Można schłodzić"]', False, True, 82)
    ]
    
    for recipe in recipes_data:
        cursor.execute("""
            INSERT INTO recipes (id, name, description, long_description, category_id,
                               calories, protein, carbs, fat, fiber, sugar, health_score,
                               prep_time, price, difficulty, tags, instructions, tips,
                               is_featured, is_available, popularity_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, recipe)
    
    # Sample ingredients
    ingredients_data = [
        ('spirulina_powder', 'Spirulina Powder BIO', 'superfoods', 4.50, 'g', 290, 57, 23, 8, 4,
         'Organiczna spirulina w proszku', 'Hawaje', True, True,
         '["wysokie białko", "witamina B12", "żelazo"]', '[]'),
        
        ('protein_vanilla', 'Protein Vanilla Premium', 'proteins', 6.20, 'g', 380, 80, 5, 3, 2,
         'Premium białko waniliowe', 'Europa', False, True,
         '["regeneracja", "budowa mięśni", "aminokwasy"]', '["soja"]'),
        
        ('coconut_water', 'Woda Kokosowa Premium', 'liquids', 2.80, 'ml', 19, 0.7, 3.7, 0.2, 1.1,
         'Naturalna woda kokosowa', 'Tajlandia', True, True,
         '["elektrolity", "nawodnienie", "potas"]', '[]'),
        
        ('matcha_premium', 'Matcha Premium Grade A', 'superfoods', 8.90, 'g', 324, 30, 39, 5, 38,
         'Najwyższa jakość matcha z Japonii', 'Japonia', True, True,
         '["antyoksydanty", "koncentracja", "L-teanina"]', '[]'),
        
        ('chia_seeds', 'Chia Seeds Premium', 'superfoods', 3.20, 'g', 486, 17, 42, 31, 34,
         'Nasiona chia najwyższej jakości', 'Meksyk', True, True,
         '["omega-3", "błonnik", "białko"]', '[]')
    ]
    
    for ing in ingredients_data:
        cursor.execute("""
            INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g,
                                   protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g,
                                   description, origin, is_organic, is_available, benefits, allergens)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, ing)
    
    # Sample users
    cursor.execute("""
        INSERT INTO users (id, name, email, loyalty_points, total_orders, total_spent, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            loyalty_points = EXCLUDED.loyalty_points,
            total_orders = EXCLUDED.total_orders,
            total_spent = EXCLUDED.total_spent
    """, ('web_user', 'Demo User IKIGAI', 'demo@ikigai.com', 2847, 15, 247.50, 'user'))
    
    cursor.execute("""
        INSERT INTO users (id, name, email, loyalty_points, role)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, ('admin', 'Administrator IKIGAI', 'admin@ikigai.com', 10000, 'admin'))
    
    conn.commit()
    print("✅ Sample data inserted")
    
    # Test the setup
    cursor.execute("SELECT COUNT(*) FROM recipes")
    recipe_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ingredients")
    ingredient_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    print(f"\n📊 Database summary:")
    print(f"  - {recipe_count} recipes")
    print(f"  - {ingredient_count} ingredients") 
    print(f"  - {user_count} users")
    print(f"  - 9 tables total")
    
    conn.close()
    print("\n🎉 Full PostgreSQL database initialization complete!")
    
except ImportError:
    print("❌ psycopg2 not installed. Add 'psycopg2-binary' to requirements.txt")
except Exception as e:
    print(f"❌ Error initializing PostgreSQL: {e}")
    import traceback
    traceback.print_exc() 