#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://ikigai_user:ikigai_pass@localhost:5432/ikigai_dev')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Testuje dokładnie to samo zapytanie z endpointu
print("🔍 Testowanie zapytania SQL z endpointu...")
cursor.execute("""
    SELECT 
        i.id,
        i.name,
        i.description,
        i.price,
        i.calories_per_100g,
        i.protein_per_100g,
        i.carbs_per_100g,
        i.fat_per_100g,
        i.fiber_per_100g,
        ic.slug as category_slug,
        ic.name as category_name,
        i.origin,
        i.is_organic,
        i.allergens,
        i.benefits
    FROM ingredients i
    JOIN ingredient_categories ic ON i.category_id = ic.id
    WHERE ic.slug = %s AND i.is_available = true
    ORDER BY i.name
    LIMIT 5
""", ('liquids',))

results = cursor.fetchall()
print(f"✅ Zapytanie SQL zwróciło: {len(results)} składników dla 'liquids'")

for r in results:
    print(f"  - {r['name']} ({r['price']}zł) - kategoria: {r['category_slug']}")

# Test dla innych kategorii
for category in ['superfoods', 'proteins', 'fruits']:
    cursor.execute("""
        SELECT COUNT(*) as count, ic.slug, ic.name
        FROM ingredients i
        JOIN ingredient_categories ic ON i.category_id = ic.id
        WHERE ic.slug = %s AND i.is_available = true
        GROUP BY ic.slug, ic.name
    """, (category,))
    
    result = cursor.fetchone()
    if result:
        print(f"✅ {category}: {result['count']} składników")
    else:
        print(f"❌ {category}: brak składników")

conn.close() 