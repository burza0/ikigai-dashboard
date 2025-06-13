#!/usr/bin/env python3
"""
Endpoint do pobierania przepisów z bazy PostgreSQL
"""
import os
import json
import psycopg2
import psycopg2.extras

def get_meal_recipes_from_db():
    """Pobierz przepisy z bazy PostgreSQL"""
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            return {"error": "No DATABASE_URL found"}
        
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, category, description, ingredients, 
                   calories, protein, carbs, price, health_score, prep_time
            FROM recipes 
            WHERE is_available = true
            ORDER BY id
        """)
        
        recipes_data = cursor.fetchall()
        conn.close()
        
        # Convert to frontend format
        recipes = []
        for recipe in recipes_data:
            # Parse JSON ingredients if it's a string
            ingredients = recipe['ingredients']
            if isinstance(ingredients, str):
                try:
                    ingredients = json.loads(ingredients)
                except:
                    ingredients = []
            
            recipes.append({
                "id": recipe['id'],
                "name": recipe['name'],
                "category": recipe['category'],
                "description": recipe['description'],
                "ingredients": ingredients,
                "calories": recipe['calories'],
                "protein": recipe['protein'],
                "carbs": recipe['carbs'] if recipe['carbs'] else 0,
                "price": float(recipe['price']) if recipe['price'] else 0,
                "health_score": recipe['health_score'],
                "prep_time": recipe['prep_time'],
                "difficulty": "easy",
                "tags": ["healthy", "fresh"]
            })
        
        print(f"✅ Pobrano {len(recipes)} przepisów z PostgreSQL")
        return {
            "status": "success",
            "data": recipes
        }
        
    except Exception as e:
        print(f"❌ Błąd pobierania przepisów: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    result = get_meal_recipes_from_db()
    print(json.dumps(result, indent=2)) 
"""
Endpoint do pobierania przepisów z bazy PostgreSQL
"""
import os
import json
import psycopg2
import psycopg2.extras

def get_meal_recipes_from_db():
    """Pobierz przepisy z bazy PostgreSQL"""
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            return {"error": "No DATABASE_URL found"}
        
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, category, description, ingredients, 
                   calories, protein, carbs, price, health_score, prep_time
            FROM recipes 
            WHERE is_available = true
            ORDER BY id
        """)
        
        recipes_data = cursor.fetchall()
        conn.close()
        
        # Convert to frontend format
        recipes = []
        for recipe in recipes_data:
            # Parse JSON ingredients if it's a string
            ingredients = recipe['ingredients']
            if isinstance(ingredients, str):
                try:
                    ingredients = json.loads(ingredients)
                except:
                    ingredients = []
            
            recipes.append({
                "id": recipe['id'],
                "name": recipe['name'],
                "category": recipe['category'],
                "description": recipe['description'],
                "ingredients": ingredients,
                "calories": recipe['calories'],
                "protein": recipe['protein'],
                "carbs": recipe['carbs'] if recipe['carbs'] else 0,
                "price": float(recipe['price']) if recipe['price'] else 0,
                "health_score": recipe['health_score'],
                "prep_time": recipe['prep_time'],
                "difficulty": "easy",
                "tags": ["healthy", "fresh"]
            })
        
        print(f"✅ Pobrano {len(recipes)} przepisów z PostgreSQL")
        return {
            "status": "success",
            "data": recipes
        }
        
    except Exception as e:
        print(f"❌ Błąd pobierania przepisów: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    result = get_meal_recipes_from_db()
    print(json.dumps(result, indent=2)) 