#!/usr/bin/env python3

# Odczytaj zawartość pliku
with open('analytics_server.py', 'r') as f:
    content = f.read()

# Znajdź miejsce gdzie dodać nowy endpoint (przed if __name__)
insertion_point = content.rfind('if __name__ == \'__main__\'')

# Nowy endpoint
new_endpoint = '''
@app.route('/api/ingredients/category/<category_slug>', methods=['GET'])
def get_ingredients_by_category(category_slug):
    """Składniki dla konkretnej kategorii z PostgreSQL"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                # Pobierz składniki dla danej kategorii
                cursor.execute("""
                    SELECT 
                        i.id,
                        i.name,
                        i.description,
                        i.price,
                        i.calories_per_100g,
                        i.protein,
                        i.carbs,
                        i.fat,
                        i.fiber,
                        ic.slug as category_slug,
                        ic.name as category_name,
                        i.origin,
                        i.is_organic,
                        i.allergens,
                        i.benefits,
                        i.image_url
                    FROM ingredients i
                    JOIN ingredient_categories ic ON i.category_id = ic.id
                    WHERE ic.slug = %s AND i.is_available = true
                    ORDER BY i.name
                """, (category_slug,))
                
                ingredients = cursor.fetchall()
                
                # Konwersja na format JSON-friendly
                ingredients_data = []
                for ing in ingredients:
                    ingredients_data.append({
                        "id": ing['id'],
                        "name": ing['name'],
                        "description": ing['description'],
                        "price": float(ing['price']),
                        "category": ing['category_slug'],
                        "category_name": ing['category_name'],
                        "calories_per_100g": ing['calories_per_100g'],
                        "protein": float(ing['protein'] or 0),
                        "carbs": float(ing['carbs'] or 0),
                        "fat": float(ing['fat'] or 0),
                        "fiber": float(ing['fiber'] or 0),
                        "origin": ing['origin'],
                        "organic": ing['is_organic'],
                        "allergens": ing['allergens'].split(',') if ing['allergens'] else [],
                        "benefits": ing['benefits'].split(',') if ing['benefits'] else [],
                        "image": ing['image_url'] or f"/images/ingredients/{ing['id']}.jpg"
                    })
                
                print(f"✅ Pobrano {len(ingredients_data)} składników dla kategorii '{category_slug}' z PostgreSQL")
                return jsonify({
                    "status": "success",
                    "data": ingredients_data,
                    "category": category_slug,
                    "count": len(ingredients_data)
                })
            else:
                print("❌ Brak połączenia z bazą danych")
                
    except Exception as e:
        print(f"❌ Błąd pobierania składników dla kategorii '{category_slug}': {e}")
    
    # Fallback - puste dane
    return jsonify({
        "status": "success",
        "data": [],
        "category": category_slug,
        "count": 0
    })

'''

# Wstaw nowy endpoint
if insertion_point != -1:
    new_content = content[:insertion_point] + new_endpoint + content[insertion_point:]
    
    # Zapisz do pliku
    with open('analytics_server.py', 'w') as f:
        f.write(new_content)
    print('✅ Nowy endpoint dodany do analytics_server.py')
else:
    print('❌ Nie znaleziono miejsca do wstawienia endpointu') 