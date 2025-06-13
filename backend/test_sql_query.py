#!/usr/bin/env python3
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://ikigai_user:ikigai_pass@localhost:5432/ikigai_dev')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Test zapytania z endpointu dla różnych kategorii
test_categories = ['liquids', 'superfoods', 'proteins', 'fruits']

for category in test_categories:
    print(f"\n🔍 Testowanie kategorii: {category}")
    cursor.execute('''
        SELECT i.id, i.name, ic.slug 
        FROM ingredients i
        JOIN ingredient_categories ic ON i.category_id = ic.id
        WHERE ic.slug = %s AND i.is_available = true
        ORDER BY i.name
        LIMIT 3
    ''', (category,))
    
    results = cursor.fetchall()
    print(f"  Znalezione składniki: {len(results)}")
    for r in results:
        print(f"    - {r[1]} (kategoria: {r[2]})")

# Sprawdź dostępne kategorie
print(f"\n📋 Dostępne kategorie:")
cursor.execute('SELECT slug, name FROM ingredient_categories ORDER BY slug')
categories = cursor.fetchall()
for cat in categories:
    print(f"  - {cat[0]}: {cat[1]}")

# Sprawdź przykładowe składniki z category_id
print(f"\n🔬 Przykładowe składniki z category_id:")
cursor.execute('SELECT name, category_id FROM ingredients ORDER BY id LIMIT 5')
samples = cursor.fetchall()
for sample in samples:
    print(f"  - {sample[0]} -> category_id: {sample[1]}")

conn.close() 