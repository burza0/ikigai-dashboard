from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
import math
import re
from psycopg2 import pool
from cache import app_cache
import qrcode
import base64
import io
from datetime import datetime

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
            result = None
        cur.close()
        return result
    finally:
        if conn:
            return_db_connection(conn)

def execute_query(query, params=None):
    """Wykonuje zapytanie używając connection pooling"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
        rowcount = cur.rowcount
        cur.close()
        return rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            return_db_connection(conn)

# Inicjalizacja puli przy starcie aplikacji
init_db_pool()

@app.route("/api/zawodnicy")
def zawodnicy():
    """Endpoint zwracający listę zawodników z QR kodami"""
    rows = get_all("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code,
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        ORDER BY z.nr_startowy
    """)
    return jsonify(rows)

@app.route("/api/qr/generate/<int:nr_startowy>", methods=['POST'])
def qr_generate_for_zawodnik(nr_startowy):
    """Generowanie QR kodu dla pojedynczego zawodnika"""
    try:
        # Sprawdź czy zawodnik istnieje
        zawodnik = get_one("SELECT * FROM zawodnicy WHERE nr_startowy = %s", (nr_startowy,))
        if not zawodnik:
            return jsonify({"error": "Zawodnik nie istnieje"}), 404
        
        # Wygeneruj QR kod
        qr_data = f"SKATECROSS_QR_{nr_startowy}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Zapisz QR kod do bazy danych
        execute_query(
            "UPDATE zawodnicy SET qr_code = %s WHERE nr_startowy = %s",
            (qr_data, nr_startowy)
        )
        
        # Wygeneruj obraz QR kodu jako base64
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "qr_code": qr_data,
            "qr_image": f"data:image/png;base64,{img_str}",
            "zawodnik": zawodnik
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd generowania QR: {str(e)}"
        }), 500

@app.route("/api/qr/generate-bulk", methods=['POST'])
def qr_generate_bulk():
    """Masowe generowanie QR kodów"""
    try:
        data = request.json
        numery_startowe = data.get('numery_startowe', [])
        
        if not numery_startowe:
            return jsonify({"error": "Brak numerów startowych"}), 400
        
        results = []
        
        for nr_startowy in numery_startowe:
            try:
                # Sprawdź czy zawodnik istnieje
                zawodnik = get_one("SELECT * FROM zawodnicy WHERE nr_startowy = %s", (nr_startowy,))
                if not zawodnik:
                    results.append({
                        "nr_startowy": nr_startowy,
                        "success": False,
                        "error": "Zawodnik nie istnieje"
                    })
                    continue
                
                # Wygeneruj QR kod
                qr_data = f"SKATECROSS_QR_{nr_startowy}"
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(qr_data)
                qr.make(fit=True)
                
                # Zapisz QR kod do bazy danych
                execute_query(
                    "UPDATE zawodnicy SET qr_code = %s WHERE nr_startowy = %s",
                    (qr_data, nr_startowy)
                )
                
                # Wygeneruj obraz QR kodu jako base64
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                results.append({
                    "nr_startowy": nr_startowy,
                    "success": True,
                    "qr_code": qr_data,
                    "qr_image": f"data:image/png;base64,{img_str}",
                    "zawodnik": zawodnik
                })
                
            except Exception as e:
                results.append({
                    "nr_startowy": nr_startowy,
                    "success": False,
                    "error": str(e)
                })
        
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        return jsonify({
            "success": True,
            "generated": len(successful),
            "failed": len(failed),
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd masowego generowania QR: {str(e)}"
        }), 500

@app.route("/api/qr/stats")
def qr_stats():
    """Statystyki QR kodów"""
    try:
        stats = get_one("""
            SELECT 
                COUNT(*) as total_zawodnikow,
                COUNT(qr_code) as z_qr_kodami,
                COUNT(*) - COUNT(qr_code) as bez_qr_kodow
            FROM zawodnicy
        """)
        
        return jsonify(stats or {})
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania statystyk QR: {str(e)}"}), 500

@app.route("/api/grupy-startowe")
def grupy_startowe():
    """Endpoint zwracający grupy startowe"""
    try:
        rows = get_all("""
            SELECT 
                q.kategoria,
                q.plec,
                q.numer_grupy,
                q.nazwa,
                COUNT(z.nr_startowy) as liczba_zawodnikow,
                q.status,
                q.estimated_time,
                STRING_AGG(z.nr_startowy::text, ', ' ORDER BY z.nr_startowy) as numery_startowe,
                STRING_AGG(z.imie || ' ' || z.nazwisko, ', ' ORDER BY z.nr_startowy) as lista_zawodnikow
            FROM start_queue q
            LEFT JOIN zawodnicy z ON z.kategoria = q.kategoria AND z.plec = q.plec
            GROUP BY q.kategoria, q.plec, q.numer_grupy, q.nazwa, q.status, q.estimated_time
            ORDER BY q.numer_grupy
        """)
        
        return jsonify(rows)
        
    except Exception as e:
        print(f"❌ Błąd w grupy-startowe: {str(e)}")
        return jsonify({"error": f"Błąd pobierania grup startowych: {str(e)}"}), 500

@app.route("/api/grupa-aktywna", methods=['GET'])
def get_grupa_aktywna():
    """Pobieranie aktywnej grupy"""
    try:
        row = get_one("""
            SELECT * FROM start_queue 
            WHERE status = 'ACTIVE' 
            ORDER BY numer_grupy LIMIT 1
        """)
        
        if row:
            return jsonify({
                "success": True,
                "grupa": row
            })
        else:
            return jsonify({
                "success": True,
                "grupa": None
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd pobierania aktywnej grupy: {str(e)}"
        }), 500

@app.route("/api/grupa-aktywna", methods=['POST'])
def set_grupa_aktywna():
    """Ustawianie/usuwanie aktywnej grupy"""
    try:
        data = request.json
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        nazwa = data.get('nazwa')
        
        # Sprawdź czy grupa już jest aktywna
        isActive = get_one("""
            SELECT * FROM start_queue 
            WHERE kategoria = %s AND plec = %s AND status = 'ACTIVE'
        """, (kategoria, plec))
        
        if isActive:
            # Deaktywuj grupę
            execute_query("""
                UPDATE start_queue 
                SET status = 'WAITING'
                WHERE kategoria = %s AND plec = %s
            """, (kategoria, plec))
            
            return jsonify({
                "success": True,
                "action": "removed",
                "message": f"Grupa {nazwa} została deaktywowana"
            })
        else:
            # Deaktywuj wszystkie inne grupy
            execute_query("UPDATE start_queue SET status = 'WAITING'")
            
            # Aktywuj wybraną grupę
            execute_query("""
                UPDATE start_queue 
                SET status = 'ACTIVE'
                WHERE kategoria = %s AND plec = %s
            """, (kategoria, plec))
    
    return jsonify({
                "success": True,
                "action": "added",
                "message": f"Grupa {nazwa} została aktywowana"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd toggle grupy aktywnej: {str(e)}"
        }), 500

@app.route("/api/start-queue", methods=['GET'])
def get_start_queue():
    """Pobieranie kolejki startowej"""
    try:
    rows = get_all("""
            SELECT DISTINCT
                z.nr_startowy,
                z.imie,
                z.nazwisko,
                z.kategoria,
                z.plec,
                z.klub,
                z.qr_code,
                'AKTYWNA_GRUPA' as source_type,
                z.ostatni_skan
            FROM zawodnicy z
            INNER JOIN start_queue sq ON z.kategoria = sq.kategoria AND z.plec = sq.plec
            WHERE sq.status = 'ACTIVE'
            
            UNION
            
            SELECT DISTINCT
                z.nr_startowy,
                z.imie,
                z.nazwisko,
                z.kategoria,
                z.plec,
                z.klub,
                z.qr_code,
                'SKANOWANY' as source_type,
                z.ostatni_skan
            FROM zawodnicy z
            WHERE z.checked_in = true
            
            ORDER BY nr_startowy
        """)
        
        return jsonify(rows)
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania kolejki startowej: {str(e)}"}), 500

@app.route("/api/qr/scan-result", methods=['POST'])
def qr_scan_result():
    """Endpoint dla skanowania QR kodów w centrum startu"""
    try:
        data = request.json
        qr_code = data.get('qr_code', '').strip()
        
        if not qr_code:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": "Pusty kod QR"
            }), 400
        
        # Spróbuj wyciągnąć numer startowy z QR kodu
        if qr_code.startswith('SKATECROSS_QR_'):
            nr_startowy_str = qr_code.replace('SKATECROSS_QR_', '')
        else:
            nr_startowy_str = qr_code
        
        try:
            nr_startowy = int(nr_startowy_str)
        except ValueError:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": f"Nieprawidłowy format kodu QR: {qr_code}"
            }), 400
        
        # Sprawdź czy zawodnik istnieje
        zawodnik = get_one("""
            SELECT z.*, w.status as wynik_status
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.nr_startowy = %s
        """, (nr_startowy,))
        
        if not zawodnik:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": f"Zawodnik z numerem {nr_startowy} nie istnieje"
            }), 404
        
        # Sprawdź czy już jest w kolejce
        if zawodnik.get('checked_in'):
            return jsonify({
                "success": True,
                "action": "OSTRZEZENIE",
                "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} jest już w kolejce",
                "zawodnik": zawodnik
            })
        
        # Dodaj zawodnika do kolejki
        execute_query("""
            UPDATE zawodnicy 
            SET checked_in = true, check_in_time = NOW(), ostatni_skan = NOW()
            WHERE nr_startowy = %s
        """, (nr_startowy,))
        
        return jsonify({
            "success": True,
            "action": "AKCEPTUJ",
            "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} dodany do kolejki",
            "zawodnik": zawodnik
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "action": "ODRZUC",
            "message": f"Błąd skanowania: {str(e)}"
        }), 500

@app.route("/api/version")
def get_version():
    """Endpoint zwracający wersję systemu"""
    try:
        return jsonify({
            "version": "1.0.0",
            "name": "SKATECROSS QR System",
            "features": ["QR Generation", "QR Printing", "Start Queue", "Scanner"],
            "status": "production",
            "environment": "standalone"
        })
    except Exception as e:
        return jsonify({"version": "unknown", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
