from flask import jsonify
import psycopg2.extras
from datetime import datetime

def register_delete_order_endpoint(app, get_db_connection):
    """Rejestruje endpoint DELETE dla zamówień"""
    
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