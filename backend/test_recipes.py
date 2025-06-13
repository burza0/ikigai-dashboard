#!/usr/bin/env python3
import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print(f"Connecting to: {DATABASE_URL}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute('SELECT id, name, price FROM recipes WHERE is_available = true')
    recipes = cursor.fetchall()
    
    print(f"Znaleziono {len(recipes)} przepisów w bazie PostgreSQL:")
    for recipe in recipes:
        print(f"  {recipe['id']}: {recipe['name']} - {recipe['price']}zł")
    
    conn.close()
    
except Exception as e:
    print(f"Błąd: {e}") 
import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print(f"Connecting to: {DATABASE_URL}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute('SELECT id, name, price FROM recipes WHERE is_available = true')
    recipes = cursor.fetchall()
    
    print(f"Znaleziono {len(recipes)} przepisów w bazie PostgreSQL:")
    for recipe in recipes:
        print(f"  {recipe['id']}: {recipe['name']} - {recipe['price']}zł")
    
    conn.close()
    
except Exception as e:
    print(f"Błąd: {e}") 