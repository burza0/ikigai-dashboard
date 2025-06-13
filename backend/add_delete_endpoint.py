import re

# Czytaj oryginalny plik
with open('analytics_server.py', 'r') as f:
    content = f.read()

# Znajdź miejsce przed if __name__
if_main_pattern = r"if __name__ == '__main__':\n    print\(\"🚀 Uruchamiam IKIGAI Analytics Server...\"\)\n    app\.run\(host='0\.0\.0\.0', port=5001, debug=True\)"

# Endpoint DELETE
delete_endpoint = '''
@app.route('/api/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Usuwanie zamówienia"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                # Sprawdź czy zamówienie istnieje
                cursor.execute("SELECT id, status FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Zamówienie nie znalezione"}), 404
                
                # Nie pozwalaj usuwać zamówień w trakcie przygotowania
                if order["status"] in ["preparing", "ready"]:
                    return jsonify({
                        "status": "error", 
                        "message": "Nie można usunąć zamówienia w trakcie przygotowania"
                    }), 400
                
                # Usuń zamówienie
                cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
                
                if cursor.rowcount == 0:
                    return jsonify({"status": "error", "message": "Nie udało się usunąć zamówienia"}), 500
                
                conn.commit()
                
                print(f"✅ Zamówienie {order_id} zostało usunięte")
                return jsonify({
                    "status": "success",
                    "message": "Zamówienie zostało usunięte"
                })
                
    except Exception as e:
        print(f"❌ Błąd usuwania zamówienia {order_id}: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

if __name__ == '__main__':
    print("🚀 Uruchamiam IKIGAI Analytics Server...")
    app.run(host='0.0.0.0', port=5001, debug=True)'''

# Zastąp końcówkę pliku
new_content = re.sub(if_main_pattern, delete_endpoint, content)

# Zapisz nowy plik
with open('analytics_server.py', 'w') as f:
    f.write(new_content)

print('✅ Endpoint DELETE dodany do analytics_server.py') 