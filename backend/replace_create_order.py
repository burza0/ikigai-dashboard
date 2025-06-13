import re

with open('analytics_server.py', 'r') as f:
    content = f.read()

# Find the create_order function and replace it
new_function = '''@app.route('/api/orders', methods=['POST'])
def create_order():
    """Składanie nowego zamówienia - simplified debug version"""
    try:
        print('📥 Received POST request to /api/orders')
        data = request.get_json()
        print(f'📊 Request data: {data}')
        
        # Simple validation
        if not data:
            print('❌ No JSON data received')
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        user_id = data.get('user_id')
        recipe_id = data.get('recipe_id') 
        machine_id = data.get('machine_id')
        payment_method = data.get('payment_method')
        
        print(f'📝 Data: user={user_id}, recipe={recipe_id}, machine={machine_id}, payment={payment_method}')
        
        if not all([user_id, recipe_id, machine_id, payment_method]):
            print('❌ Missing required fields')
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Generate order ID
        order_id = str(uuid.uuid4())
        print(f'🆔 Generated order ID: {order_id}')
        
        # Simple database insert
        with get_db_connection() as conn:
            if not conn:
                print('❌ No database connection')
                return jsonify({'status': 'error', 'message': 'Database not available'}), 500
            
            print('💾 Database connected')
            cursor = conn.cursor()
            
            # Insert order
            cursor.execute("""
                INSERT INTO orders (id, user_id, recipe_id, status, total_price, 
                                  payment_method, machine_id, created_at, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                order_id, user_id, recipe_id, 'pending', 
                21.0, payment_method, machine_id, 
                datetime.now(), data.get('notes', '')
            ))
            conn.commit()
            
            print(f'✅ Order {order_id} saved to database')
            
            return jsonify({
                'status': 'success',
                'order_id': order_id,
                'total_price': 21.0,
                'message': 'Zamówienie zostało złożone pomyślnie'
            })
        
    except Exception as e:
        print(f'❌ Error in create_order: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': f'Internal server error: {str(e)}'}), 500'''

# Find the start of create_order function 
start_pattern = r'@app\.route\(\'/api/orders\', methods=\[\'POST\'\]\)\s*\ndef create_order\(\):'
start_match = re.search(start_pattern, content)

if start_match:
    # Find the next function or end of file
    remaining_content = content[start_match.start():]
    
    # Look for the next @app.route or if __name__
    next_function_pattern = r'\n@app\.route|if __name__ == \'__main__\':'
    next_match = re.search(next_function_pattern, remaining_content[1:])  # Skip first character to avoid matching itself
    
    if next_match:
        end_pos = start_match.start() + next_match.start() + 1
    else:
        # If no next function found, assume it goes to the end
        end_pos = len(content)
    
    # Replace the function
    new_content = content[:start_match.start()] + new_function + '\n\n' + content[end_pos:]
    
    with open('analytics_server.py', 'w') as f:
        f.write(new_content)
    
    print('✅ Replaced create_order function with debug version')
else:
    print('❌ Could not find create_order function') 