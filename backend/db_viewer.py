#!/usr/bin/env python3
"""
🔍 IKIGAI Database Viewer
Prosty viewer bazy danych SQLite dla aplikacji IKIGAI
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'ikigai.db')

def get_db_connection():
    """Połączenie z bazą danych"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def view_tables():
    """Wyświetla wszystkie tabele w bazie"""
    conn = get_db_connection()
    
    print("📋 Tabele w bazie danych:")
    tables = conn.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """).fetchall()
    
    for table in tables:
        # Policz rekordy w każdej tabeli
        count = conn.execute(f"SELECT COUNT(*) as count FROM {table['name']}").fetchone()['count']
        print(f"   📊 {table['name']}: {count} rekordów")
    
    conn.close()

def view_recipes():
    """Wyświetla przepisy"""
    conn = get_db_connection()
    
    print("\n🍜 PRZEPISY:")
    print("=" * 50)
    
    recipes = conn.execute("""
        SELECT r.*, c.name as category_name
        FROM recipes r
        LEFT JOIN categories c ON r.category_id = c.id
        ORDER BY r.name
    """).fetchall()
    
    for recipe in recipes:
        print(f"\n🍽️ {recipe['name']}")
        print(f"   📂 Kategoria: {recipe['category_name'] or 'Brak'}")
        print(f"   💰 Cena: {recipe['price']}zł")
        print(f"   🔥 Kalorie: {recipe['calories']} kcal")
        print(f"   🏥 Health Score: {recipe['health_score']}/100")
        print(f"   ⏱️ Czas przygotowania: {recipe['prep_time']} min")
        print(f"   📈 Trudność: {recipe['difficulty']}")
        
        # Pokaż składniki
        ingredients = conn.execute("""
            SELECT ri.amount, ri.unit, i.name
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = ?
            ORDER BY i.name
        """, (recipe['id'],)).fetchall()
        
        if ingredients:
            print(f"   🧪 Składniki:")
            for ing in ingredients:
                print(f"      • {ing['name']}: {ing['amount']}{ing['unit']}")
    
    conn.close()

def view_users():
    """Wyświetla użytkowników"""
    conn = get_db_connection()
    
    print("\n👥 UŻYTKOWNICY:")
    print("=" * 50)
    
    users = conn.execute("SELECT * FROM users ORDER BY loyalty_points DESC").fetchall()
    
    for user in users:
        print(f"\n👤 {user['name']}")
        print(f"   📧 Email: {user['email'] or 'Brak'}")
        print(f"   🏆 Poziom lojalnościowy: {user['loyalty_level']}")
        print(f"   ⭐ Punkty: {user['loyalty_points']}")
        print(f"   🛒 Zamówienia: {user['total_orders']}")
        print(f"   💸 Wydane: {user['total_spent']}zł")
        print(f"   📅 Członek od: {user['member_since']}")
        
        # Pokaż odznaki
        if user['badges']:
            try:
                badges = json.loads(user['badges'])
                print(f"   🏅 Odznaki: {len(badges)}")
                for badge in badges[:3]:  # Pokaż maksymalnie 3
                    print(f"      • {badge.get('name', 'Nieznana')}")
            except json.JSONDecodeError:
                pass
    
    conn.close()

def view_challenges():
    """Wyświetla wyzwania"""
    conn = get_db_connection()
    
    print("\n🎯 WYZWANIA LOJALNOŚCIOWE:")
    print("=" * 50)
    
    challenges = conn.execute("""
        SELECT * FROM loyalty_challenges 
        WHERE is_active = 1
        ORDER BY difficulty, name
    """).fetchall()
    
    for challenge in challenges:
        print(f"\n🎯 {challenge['name']}")
        print(f"   📝 Opis: {challenge['description']}")
        print(f"   🗓️ Typ: {challenge['type']}")
        print(f"   🎯 Cel: {challenge['target']}")
        print(f"   🎁 Nagroda: {challenge['reward_points']} punktów")
        print(f"   📈 Trudność: {challenge['difficulty']}")
        print(f"   ⏰ Wygasa: {challenge['expires_at'] or 'Bez terminu'}")
        
        # Pokaż postęp użytkowników
        progress = conn.execute("""
            SELECT u.name, ucp.progress, ucp.status
            FROM user_challenge_progress ucp
            JOIN users u ON ucp.user_id = u.id
            WHERE ucp.challenge_id = ?
        """, (challenge['id'],)).fetchall()
        
        if progress:
            print(f"   👥 Postęp użytkowników:")
            for p in progress:
                status_emoji = "✅" if p['status'] == 'completed' else "🔄"
                print(f"      {status_emoji} {p['name']}: {p['progress']}/{challenge['target']}")
    
    conn.close()

def view_orders():
    """Wyświetla zamówienia"""
    conn = get_db_connection()
    
    print("\n🛒 OSTATNIE ZAMÓWIENIA:")
    print("=" * 50)
    
    orders = conn.execute("""
        SELECT o.*, u.name as user_name, r.name as recipe_name
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        LEFT JOIN recipes r ON o.recipe_id = r.id
        ORDER BY o.created_at DESC
        LIMIT 10
    """).fetchall()
    
    for order in orders:
        print(f"\n🧾 Zamówienie #{order['id']}")
        print(f"   👤 Użytkownik: {order['user_name'] or 'Anonim'}")
        print(f"   🍽️ Przepis: {order['recipe_name'] or 'Własna kompozycja'}")
        print(f"   💰 Cena: {order['total_price']}zł")
        print(f"   🔥 Kalorie: {order['total_calories']} kcal")
        print(f"   📊 Status: {order['status']}")
        print(f"   📅 Utworzono: {order['created_at']}")
        if order['qr_code']:
            print(f"   📱 QR Code: {order['qr_code']}")
    
    conn.close()

def view_analytics():
    """Wyświetla analitykę bazy danych"""
    conn = get_db_connection()
    
    print("\n📊 ANALITYKA BAZY DANYCH:")
    print("=" * 50)
    
    # Podstawowe statystyki
    stats = {
        'recipes': conn.execute("SELECT COUNT(*) as count FROM recipes").fetchone()['count'],
        'ingredients': conn.execute("SELECT COUNT(*) as count FROM ingredients").fetchone()['count'],
        'users': conn.execute("SELECT COUNT(*) as count FROM users").fetchone()['count'],
        'orders': conn.execute("SELECT COUNT(*) as count FROM orders").fetchone()['count'],
        'challenges': conn.execute("SELECT COUNT(*) as count FROM loyalty_challenges WHERE is_active = 1").fetchone()['count'],
    }
    
    print(f"📋 Przepisy: {stats['recipes']}")
    print(f"🧪 Składniki: {stats['ingredients']}")
    print(f"👥 Użytkownicy: {stats['users']}")
    print(f"🛒 Zamówienia: {stats['orders']}")
    print(f"🎯 Aktywne wyzwania: {stats['challenges']}")
    
    # Najpopularniejsze przepisy
    popular_recipes = conn.execute("""
        SELECT r.name, COUNT(o.id) as order_count
        FROM recipes r
        LEFT JOIN orders o ON r.id = o.recipe_id
        GROUP BY r.id, r.name
        ORDER BY order_count DESC
        LIMIT 3
    """).fetchall()
    
    print(f"\n🏆 Najpopularniejsze przepisy:")
    for recipe in popular_recipes:
        print(f"   • {recipe['name']}: {recipe['order_count']} zamówień")
    
    # Użytkownicy z największą liczbą punktów
    top_users = conn.execute("""
        SELECT name, loyalty_points, total_orders
        FROM users
        ORDER BY loyalty_points DESC
        LIMIT 3
    """).fetchall()
    
    print(f"\n⭐ Top użytkownicy (punkty):")
    for user in top_users:
        print(f"   • {user['name']}: {user['loyalty_points']} punktów ({user['total_orders']} zamówień)")
    
    conn.close()

def execute_custom_query():
    """Wykonuje własne zapytanie SQL"""
    print("\n💻 WYKONAJ WŁASNE ZAPYTANIE SQL:")
    print("=" * 50)
    print("Przykłady:")
    print("  SELECT * FROM recipes LIMIT 5;")
    print("  SELECT COUNT(*) FROM users;")
    print("  SELECT name, price FROM recipes ORDER BY price DESC;")
    
    query = input("\nTwoje zapytanie SQL: ").strip()
    
    if not query:
        print("❌ Puste zapytanie")
        return
    
    if not query.upper().startswith('SELECT'):
        print("❌ Tylko zapytania SELECT są dozwolone")
        return
    
    try:
        conn = get_db_connection()
        rows = conn.execute(query).fetchall()
        
        if rows:
            print(f"\n✅ Znaleziono {len(rows)} wyników:")
            print("-" * 50)
            
            # Pokaż nagłówki kolumn
            if rows:
                headers = list(rows[0].keys())
                print(" | ".join(f"{h:15}" for h in headers))
                print("-" * (len(headers) * 18))
                
                # Pokaż dane (maksymalnie 20 wierszy)
                for row in rows[:20]:
                    values = []
                    for value in row:
                        if isinstance(value, str) and len(value) > 15:
                            values.append(value[:12] + "...")
                        else:
                            values.append(str(value) if value is not None else "NULL")
                    print(" | ".join(f"{v:15}" for v in values))
                
                if len(rows) > 20:
                    print(f"... i {len(rows) - 20} więcej wierszy")
        else:
            print("ℹ️ Brak wyników")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Błąd SQL: {e}")

def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ Baza danych nie istnieje: {DB_PATH}")
        print("Uruchom najpierw: python3 init_ikigai_db.py")
        return
    
    print("🔍 IKIGAI Database Viewer")
    print(f"📁 Baza: {DB_PATH}")
    print(f"📏 Rozmiar: {os.path.getsize(DB_PATH)} bytes")
    print("=" * 50)
    
    while True:
        print(f"""
Wybierz opcję:
1. 📋 Pokaż tabele
2. 🍜 Pokaż przepisy
3. 👥 Pokaż użytkowników  
4. 🎯 Pokaż wyzwania
5. 🛒 Pokaż zamówienia
6. 📊 Analityka
7. 💻 Własne zapytanie SQL
0. ❌ Wyjście
""")
        
        try:
            choice = input("Twój wybór (0-7): ").strip()
            
            if choice == "1":
                view_tables()
            elif choice == "2":
                view_recipes()
            elif choice == "3":
                view_users()
            elif choice == "4":
                view_challenges()
            elif choice == "5":
                view_orders()
            elif choice == "6":
                view_analytics()
            elif choice == "7":
                execute_custom_query()
            elif choice == "0":
                print("👋 Do widzenia!")
                break
            else:
                print("❌ Nieprawidłowy wybór")
                
        except KeyboardInterrupt:
            print("\n👋 Do widzenia!")
            break
        except Exception as e:
            print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    main()
