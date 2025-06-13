#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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

frontend_categories = []
for cat in categories:
    if cat['slug'] in category_mapping:
        mapping = category_mapping[cat['slug']]
        frontend_categories.append({
            'id': mapping['frontend_id'],
            'db_slug': cat['slug'],
            'name': mapping['frontend_name'],
            'count': int(cat['count']),
            'step': mapping['step'],
            'icon': cat['icon'],
            'color': cat['color']
        })

print('=== MAPOWANIE KATEGORII NA FRONTEND ===')
step1_categories = [cat for cat in frontend_categories if cat['step'] == 1]
step2_categories = [cat for cat in frontend_categories if cat['step'] == 2]

print('\nKrok 1 - Wybierz bazę:')
for cat in step1_categories:
    print(f"  {cat['name']} ({cat['count']}) - {cat['icon']}")

print('\nKrok 2 - Dodaj składniki:')
for cat in step2_categories:
    print(f"  {cat['name']} ({cat['count']}) - {cat['icon']}")

print(f'\nŁącznie: {len(frontend_categories)} kategorii')

conn.close() 