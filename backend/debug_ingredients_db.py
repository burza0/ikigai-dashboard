#!/usr/bin/env python3
import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://ikigai_user:ikigai_pass@localhost:5432/ikigai_dev')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Sprawdź łączną liczbę składników
    cursor.execute('SELECT COUNT(*) FROM ingredients WHERE is_available = true')
    total = cursor.fetchone()[0]
    print(f'✅ Łączna liczba składników w bazie: {total}')
    
    # Sprawdź składniki według kategorii
    cursor.execute('''
        SELECT ic.slug, ic.name, COUNT(i.id) 
        FROM ingredient_categories ic 
        LEFT JOIN ingredients i ON ic.id = i.category_id AND i.is_available = true 
        GROUP BY ic.slug, ic.name 
        ORDER BY ic.slug
    ''')
    results = cursor.fetchall()
    
    print('\n📊 Składniki według kategorii:')
    for row in results:
        print(f'  {row[0]}: {row[1]} -> {row[2]} składników')
    
    # Sprawdź przykładowy składnik
    cursor.execute('SELECT * FROM ingredients WHERE is_available = true LIMIT 1')
    sample = cursor.fetchone()
    if sample:
        print(f'\n🔬 Przykładowy składnik: {sample}')
    else:
        print('\n❌ Brak składników w tabeli!')
    
    # Sprawdź strukturę tabeli ingredients
    cursor.execute('''
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'ingredients' 
        ORDER BY ordinal_position
    ''')
    columns = cursor.fetchall()
    print('\n🗂️ Struktura tabeli ingredients:')
    for col in columns:
        print(f'  {col[0]}: {col[1]} (nullable: {col[2]})')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Błąd: {e}') 