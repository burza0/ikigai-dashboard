#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print("=== KATEGORIE SKŁADNIKÓW ===")
cursor.execute("SELECT * FROM ingredient_categories ORDER BY id")
ingredient_categories = cursor.fetchall()
for cat in ingredient_categories:
    print(f"  {cat['id']}: {cat['name']} ({cat['slug']})")

print("\n=== SKŁADNIKI WEDŁUG KATEGORII ===")
for cat in ingredient_categories:
    cursor.execute("""
        SELECT i.name, i.price 
        FROM ingredients i 
        WHERE i.category_id = %s AND i.is_available = true 
        ORDER BY i.name
    """, (cat['id'],))
    ingredients = cursor.fetchall()
    count = len(ingredients)
    print(f"\n{cat['name']} ({cat['slug']}) - {count} składników:")
    for ing in ingredients:
        print(f"  - {ing['name']} - {ing['price']}zł")

print("\n=== MAPOWANIE NA FRONTEND ===")
print("Na froncie potrzebujemy:")
print("BAZY (krok 1): Tradycyjne, Kubeczki, Proszki")
print("SKŁADNIKI (krok 2): Superfoods, Owoce, Nasiona, Przyprawy, Produkty pszczele, Detoks")

print("\nW bazie mamy kategorie:")
for cat in ingredient_categories:
    print(f"  {cat['slug']}: {cat['name']}")

conn.close() 