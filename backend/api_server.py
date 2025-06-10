from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
import math
import re
from psycopg2 import pool
from cache import app_cache

load_dotenv()
app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("DATABASE_URL")

# Connection pool dla lepszej wydajności
connection_pool = None

def init_db_pool():
    """Inicjalizuje pulę połączeń"""
    global connection_pool
    if connection_pool is None:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,  # min 1, max 20 połączeń
            DB_URL
        )

def get_db_connection():
    """Pobiera połączenie z puli"""
    global connection_pool
    if connection_pool is None:
        init_db_pool()
    return connection_pool.getconn()

def return_db_connection(conn):
    """Zwraca połączenie do puli"""
    global connection_pool
    if connection_pool is not None and conn is not None:
        try:
            connection_pool.putconn(conn)
        except psycopg2.pool.PoolError:
            # Jeśli wystąpi błąd, spróbuj zainicjować pulę ponownie
            init_db_pool()

def get_all(query, params=None):
    """Pobiera wszystkie rekordy z bazy danych używając connection pooling"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("❌ Błąd: Nie udało się uzyskać połączenia z bazą danych")
            return []
            
        cur = conn.cursor()
        try:
            if params:
                print(f"🔍 Wykonuję zapytanie: {query} z parametrami: {params}")
                cur.execute(query, params)
            else:
                print(f"🔍 Wykonuję zapytanie: {query}")
                cur.execute(query)
                
            rows = cur.fetchall()
            if not rows:
                print("ℹ️ Zapytanie nie zwróciło żadnych wyników")
                return []
                
            columns = [desc[0] for desc in cur.description]
            result = [dict(zip(columns, row)) for row in rows]
            print(f"✅ Znaleziono {len(result)} wyników")
            return result
            
        except Exception as e:
            print(f"❌ Błąd podczas wykonywania zapytania: {str(e)}")
            return []
        finally:
            cur.close()
    except Exception as e:
        print(f"❌ Błąd w get_all: {str(e)}")
        return []
    finally:
        if conn:
            return_db_connection(conn)

def get_one(query, params=None):
    """Pobiera pojedynczy rekord używając connection pooling"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            result = dict(zip(columns, row))
        else:
import qrcode
import base64
import io
from datetime import datetime
@app.route("/api/zawodnicy")
def zawodnicy():
    rows = get_all("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code,
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        ORDER BY z.nr_startowy
    """)
    return jsonify(rows)

@app.route("/api/kategorie")
def kategorie():
    # Pobierz kategorie
    kategorie_rows = get_all("SELECT DISTINCT kategoria FROM zawodnicy WHERE kategoria IS NOT NULL ORDER BY kategoria")
    kategorie_list = [row["kategoria"] for row in kategorie_rows]
    
    # Pobierz łączną liczbę zawodników
    total_rows = get_all("SELECT COUNT(*) as total FROM zawodnicy WHERE kategoria IS NOT NULL")
    total_zawodnikow = total_rows[0]["total"] if total_rows else 0
    
    return jsonify({
        "kategorie": kategorie_list,
        "total_zawodnikow": total_zawodnikow
    })

@app.route("/api/statystyki")
def statystyki():
    """Endpoint zwracający statystyki zawodników według kategorii i płci"""
    rows = get_all("""
