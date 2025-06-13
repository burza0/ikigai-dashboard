#!/usr/bin/env python3
# Ten skrypt zastąpi funkcję get_ingredients_categories w analytics_server.py

import re

# Nowa zawartość funkcji
new_function = '''def get_ingredients_categories():
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
    })'''

# Wczytaj analytics_server.py
with open('analytics_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern do znalezienia starej funkcji
pattern = r'def get_ingredients_categories\(\):.*?(?=\n@app\.route|\nif __name__|$)'

# Zastąp starą funkcję nową
new_content = re.sub(pattern, new_function, content, flags=re.DOTALL)

# Zapisz zaktualizowany plik
with open('analytics_server.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Zaktualizowano funkcję get_ingredients_categories w analytics_server.py")
print("🔄 Restart backendu wymagany dla aktywacji zmian") 