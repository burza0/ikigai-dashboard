import psycopg2
import psycopg2.extras
from flask import jsonify
from contextlib import contextmanager
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

@contextmanager
def get_db_connection():
    conn = None
    try:
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL)
            yield conn
        else:
            yield None
    except Exception as e:
        print(f"Error connecting to database: {e}")
        yield None
    finally:
        if conn:
            conn.close()

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
                
                print(f"✅ Pobrano {len(frontend_categories)} kategorii składników")
                return {
                    "status": "success",
                    "data": frontend_categories
                }
            else:
                print("❌ Brak połączenia z bazą danych")
                
    except Exception as e:
        print(f"❌ Błąd pobierania kategorii składników: {e}")
    
    # Fallback - statyczne kategorie
    return {
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
            }
        ]
    }

if __name__ == '__main__':
    result = get_ingredients_categories()
    print("Wynik:", result) 