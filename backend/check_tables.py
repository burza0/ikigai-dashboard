#!/usr/bin/env python3
"""
Sprawdź jakie tabele istnieją w PostgreSQL na Heroku
"""
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ DATABASE_URL not found")
    exit(1)

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

try:
    import psycopg2
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Lista wszystkich tabel
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    
    print(f"📊 Tabele w bazie danych ({len(tables)} total):")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count} rows")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}") 