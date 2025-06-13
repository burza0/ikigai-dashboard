@app.route('/api/ingredients/category/<category_slug>', methods=['GET'])
def get_ingredients_by_category(category_slug):
    """Składniki dla konkretnej kategorii z PostgreSQL"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                cursor.execute("""
                    SELECT 
                        i.id, i.name, i.description, i.price, i.calories_per_100g,
                        i.protein_per_100g, i.carbs_per_100g, i.fat_per_100g, i.fiber_per_100g,
                        ic.slug as category_slug, ic.name as category_name,
                        i.origin, i.is_organic, i.allergens, i.benefits
                    FROM ingredients i
                    JOIN ingredient_categories ic ON i.category_id = ic.id
                    WHERE ic.slug = %s AND i.is_available = true
                    ORDER BY i.name
                """, (category_slug,))
                
                ingredients = cursor.fetchall()
                ingredients_data = []
                for ing in ingredients:
                    ingredients_data.append({
                        "id": ing['id'],
                        "name": ing['name'],
                        "description": ing['description'] or f"Wysokiej jakości {ing['name']}",
                        "price": float(ing['price']) if ing['price'] else 0,
                        "category": ing['category_slug'],
                        "category_name": ing['category_name'],
                        "calories_per_100g": ing['calories_per_100g'] or 0,
                        "protein": float(ing["protein_per_100g"] or 0),
                        "carbs": float(ing["carbs_per_100g"] or 0),
                        "fat": float(ing["fat_per_100g"] or 0),
                        "fiber": float(ing["fiber_per_100g"] or 0),
                        "origin": ing['origin'] or "Unknown",
                        "organic": bool(ing['is_organic']),
                        "allergens": ing['allergens'].split(',') if ing['allergens'] else [],
                        "benefits": ing['benefits'].split(',') if ing['benefits'] else [],
                        "image": f"/images/ingredients/{ing['name'].lower().replace(' ', '_')}.jpg"
                    })
                
                print(f"✅ Pobrano {len(ingredients_data)} składników dla kategorii '{category_slug}' z PostgreSQL")
                return jsonify({
                    "status": "success",
                    "data": ingredients_data,
                    "category": category_slug,
                    "count": len(ingredients_data)
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania składników dla kategorii '{category_slug}': {e}")
    
    return jsonify({
        "status": "success",
        "data": [],
        "category": category_slug,
        "count": 0
    }) 