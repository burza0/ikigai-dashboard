# ===== SYSTEM ZAMÓWIEŃ =====

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Składanie nowego zamówienia z QR kodem"""
    try:
        data = request.get_json()
        required_fields = ["user_id", "recipe_id", "machine_id", "payment_method"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"status": "error", "message": f"Brak pola: {field}"}), 400
        
        order_id = str(uuid.uuid4())
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT price FROM recipes WHERE id = %s", (data["recipe_id"],))
                recipe = cursor.fetchone()
                
                if not recipe:
                    return jsonify({"status": "error", "message": "Przepis nie znaleziony"}), 404
                
                total_price = float(recipe["price"])
                
                # Generuj prosty QR kod
                qr_data = {
                    "order_id": order_id,
                    "user_id": data["user_id"],
                    "recipe_id": data["recipe_id"],
                    "machine_id": data["machine_id"],
                    "total_price": total_price
                }
                
                qr_content = json.dumps(qr_data)
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
                qr.add_data(qr_content)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                qr_code = f"data:image/png;base64,{img_base64}"
                
                # Zapisz zamówienie
                cursor.execute("""
                    INSERT INTO orders (id, user_id, recipe_id, status, total_price, 
                                      payment_method, machine_id, qr_code, created_at, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    order_id, data["user_id"], data["recipe_id"], "pending", 
                    total_price, data["payment_method"], data["machine_id"], 
                    qr_code, datetime.now(), data.get("notes", "")
                ))
                conn.commit()
                
                print(f"✅ Zamówienie {order_id} utworzone")
                
                return jsonify({
                    "status": "success",
                    "order_id": order_id,
                    "qr_code": qr_code,
                    "total_price": total_price,
                    "estimated_time": 5,
                    "message": "Zamówienie zostało złożone. Pokaż kod QR przy automacie."
                })
                
    except Exception as e:
        print(f"❌ Błąd tworzenia zamówienia: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Pobieranie listy zamówień"""
    try:
        user_id = request.args.get("user_id")
        limit = int(request.args.get("limit", 20))
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                if user_id:
                    cursor.execute("""
                        SELECT o.*, r.name as recipe_name 
                        FROM orders o LEFT JOIN recipes r ON o.recipe_id = r.id 
                        WHERE o.user_id = %s ORDER BY o.created_at DESC LIMIT %s
                    """, (user_id, limit))
                else:
                    cursor.execute("""
                        SELECT o.*, r.name as recipe_name 
                        FROM orders o LEFT JOIN recipes r ON o.recipe_id = r.id 
                        ORDER BY o.created_at DESC LIMIT %s
                    """, (limit,))
                
                orders = cursor.fetchall()
                
                orders_data = []
                for order in orders:
                    orders_data.append({
                        "id": order["id"],
                        "user_id": order["user_id"],
                        "recipe_name": order["recipe_name"],
                        "status": order["status"],
                        "total_price": float(order["total_price"]),
                        "payment_method": order["payment_method"],
                        "machine_id": order["machine_id"],
                        "created_at": order["created_at"].isoformat() if order["created_at"] else None,
                        "qr_code": order["qr_code"] if order["status"] == "pending" else None
                    })
                
                return jsonify({
                    "status": "success",
                    "data": orders_data,
                    "count": len(orders_data)
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania zamówień: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Aktualizacja statusu zamówienia"""
    try:
        data = request.get_json()
        new_status = data.get("status")
        
        if new_status not in ["pending", "preparing", "ready", "completed", "cancelled"]:
            return jsonify({"status": "error", "message": "Nieprawidłowy status"}), 400
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor()
                
                if new_status == "completed":
                    cursor.execute(
                        "UPDATE orders SET status = %s, completed_at = %s WHERE id = %s",
                        (new_status, datetime.now(), order_id)
                    )
                else:
                    cursor.execute(
                        "UPDATE orders SET status = %s WHERE id = %s",
                        (new_status, order_id)
                    )
                
                conn.commit()
                
                return jsonify({
                    "status": "success",
                    "message": f"Status zamówienia zmieniony na {new_status}"
                })
                
    except Exception as e:
        print(f"❌ Błąd aktualizacji statusu: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500 