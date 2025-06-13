# ===== SYSTEM ZAMÓWIEŃ I QR KODÓW =====

def generate_qr_code(order_id, order_data):
    """Generuje kod QR dla zamówienia"""
    try:
        # Dane do QR kodu - JSON z informacjami o zamówieniu
        qr_data = {
            "order_id": order_id,
            "user_id": order_data.get("user_id"),
            "recipe_id": order_data.get("recipe_id"),
            "machine_id": order_data.get("machine_id"),
            "total_price": order_data.get("total_price"),
            "timestamp": datetime.now().isoformat()
        }
        
        # Konwertuj do JSON string
        qr_content = json.dumps(qr_data)
        
        # Generuj QR kod
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        # Konwertuj do base64 dla API
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
        
    except Exception as e:
        print(f"❌ Błąd generowania QR kodu: {e}")
        return None

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Składanie nowego zamówienia z generowaniem QR kodu"""
    try:
        data = request.get_json()
        
        # Walidacja danych
        required_fields = ["user_id", "recipe_id", "machine_id", "payment_method"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"status": "error", "message": f"Brak pola: {field}"}), 400
        
        # Generuj unikalny ID zamówienia
        order_id = str(uuid.uuid4())
        
        # Pobierz cenę przepisu
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT price FROM recipes WHERE id = %s", (data["recipe_id"],))
                recipe = cursor.fetchone()
                
                if not recipe:
                    return jsonify({"status": "error", "message": "Przepis nie znaleziony"}), 404
                
                total_price = float(recipe["price"])
                
                # Przygotuj dane zamówienia
                order_data = {
                    "user_id": data["user_id"],
                    "recipe_id": data["recipe_id"],
                    "machine_id": data["machine_id"],
                    "total_price": total_price,
                    "payment_method": data["payment_method"],
                    "notes": data.get("notes", "")
                }
                
                # Generuj QR kod
                qr_code = generate_qr_code(order_id, order_data)
                
                # Zapisz zamówienie do bazy
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
                
                print(f"✅ Zamówienie {order_id} utworzone dla użytkownika {data['user_id']}")
                
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
        status = request.args.get("status")
        limit = int(request.args.get("limit", 20))
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                
                # Buduj query
                query = """
                    SELECT o.*, r.name as recipe_name, r.description as recipe_description
                    FROM orders o
                    LEFT JOIN recipes r ON o.recipe_id = r.id
                    WHERE 1=1
                """
                params = []
                
                if user_id:
                    query += " AND o.user_id = %s"
                    params.append(user_id)
                    
                if status:
                    query += " AND o.status = %s"
                    params.append(status)
                    
                query += " ORDER BY o.created_at DESC LIMIT %s"
                params.append(limit)
                
                cursor.execute(query, params)
                orders = cursor.fetchall()
                
                # Format response
                orders_data = []
                for order in orders:
                    orders_data.append({
                        "id": order["id"],
                        "user_id": order["user_id"],
                        "recipe": {
                            "id": order["recipe_id"],
                            "name": order["recipe_name"],
                            "description": order["recipe_description"]
                        },
                        "status": order["status"],
                        "total_price": float(order["total_price"]),
                        "payment_method": order["payment_method"],
                        "machine_id": order["machine_id"],
                        "created_at": order["created_at"].isoformat() if order["created_at"] else None,
                        "completed_at": order["completed_at"].isoformat() if order["completed_at"] else None,
                        "notes": order["notes"],
                        "qr_code": order["qr_code"] if order["status"] == "pending" else None
                    })
                
                print(f"✅ Pobrano {len(orders_data)} zamówień")
                return jsonify({
                    "status": "success",
                    "data": orders_data,
                    "count": len(orders_data)
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania zamówień: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Pobieranie szczegółów zamówienia"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("""
                    SELECT o.*, r.name as recipe_name, r.description as recipe_description,
                           r.ingredients, r.calories, r.protein
                    FROM orders o
                    LEFT JOIN recipes r ON o.recipe_id = r.id
                    WHERE o.id = %s
                """, (order_id,))
                
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Zamówienie nie znalezione"}), 404
                
                order_data = {
                    "id": order["id"],
                    "user_id": order["user_id"],
                    "recipe": {
                        "id": order["recipe_id"],
                        "name": order["recipe_name"],
                        "description": order["recipe_description"],
                        "ingredients": order["ingredients"],
                        "calories": order["calories"],
                        "protein": order["protein"]
                    },
                    "status": order["status"],
                    "total_price": float(order["total_price"]),
                    "payment_method": order["payment_method"],
                    "machine_id": order["machine_id"],
                    "created_at": order["created_at"].isoformat() if order["created_at"] else None,
                    "completed_at": order["completed_at"].isoformat() if order["completed_at"] else None,
                    "notes": order["notes"],
                    "qr_code": order["qr_code"]
                }
                
                return jsonify({
                    "status": "success",
                    "data": order_data
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania zamówienia {order_id}: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Braz połączenia z bazą"}), 500

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Aktualizacja statusu zamówienia (dla automatów)"""
    try:
        data = request.get_json()
        new_status = data.get("status")
        
        if new_status not in ["pending", "preparing", "ready", "completed", "cancelled"]:
            return jsonify({"status": "error", "message": "Nieprawidłowy status"}), 400
        
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor()
                
                # Aktualizuj status
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
                
                if cursor.rowcount == 0:
                    return jsonify({"status": "error", "message": "Zamówienie nie znalezione"}), 404
                
                conn.commit()
                
                print(f"✅ Status zamówienia {order_id} zmieniony na {new_status}")
                return jsonify({
                    "status": "success",
                    "message": f"Status zamówienia zmieniony na {new_status}"
                })
                
    except Exception as e:
        print(f"❌ Błąd aktualizacji statusu {order_id}: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500

@app.route('/api/orders/<order_id>/qr', methods=['GET'])
def get_order_qr(order_id):
    """Pobieranie kodu QR dla zamówienia"""
    try:
        with get_db_connection() as conn:
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute("SELECT qr_code, status FROM orders WHERE id = %s", (order_id,))
                order = cursor.fetchone()
                
                if not order:
                    return jsonify({"status": "error", "message": "Zamówienie nie znalezione"}), 404
                
                if order["status"] not in ["pending", "preparing"]:
                    return jsonify({"status": "error", "message": "Kod QR nieaktywny dla tego statusu"}), 400
                
                return jsonify({
                    "status": "success",
                    "qr_code": order["qr_code"],
                    "order_status": order["status"]
                })
                
    except Exception as e:
        print(f"❌ Błąd pobierania QR dla {order_id}: {e}")
        return jsonify({"status": "error", "message": "Błąd serwera"}), 500
    
    return jsonify({"status": "error", "message": "Brak połączenia z bazą"}), 500 