"""
🛒 IKIGAI Orders Management
Zarządzanie zamówieniami z QR kodami
"""

from flask import Blueprint, request, jsonify
import qrcode
import uuid
import datetime
import io
import base64
from PIL import Image

orders_bp = Blueprint('orders', __name__)

# 📦 In-memory storage dla zamówień (w produkcji: baza danych)
orders_db = {}
qr_codes_db = {}

@orders_bp.route('/api/orders', methods=['GET'])
def get_orders():
    """📋 Pobierz wszystkie zamówienia użytkownika"""
    user_id = request.args.get('user_id', 'demo_user')
    user_orders = [order for order in orders_db.values() if order['user_id'] == user_id]
    return jsonify({
        'success': True,
        'orders': user_orders,
        'count': len(user_orders)
    })

@orders_bp.route('/api/orders', methods=['POST'])
def create_order():
    """🆕 Utwórz nowe zamówienie"""
    try:
        data = request.get_json()
        
        # Walidacja danych
        required_fields = ['user_id', 'items', 'vending_machine_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Brak pola: {field}'}), 400
        
        # Tworzenie zamówienia
        order_id = str(uuid.uuid4())
        order = {
            'id': order_id,
            'user_id': data['user_id'],
            'items': data['items'],  # Lista składników/produktów
            'vending_machine_id': data['vending_machine_id'],
            'status': 'pending',  # pending, paid, preparing, ready, completed
            'total_price': calculate_order_price(data['items']),
            'created_at': datetime.datetime.now().isoformat(),
            'qr_code': None,
            'preparation_time': estimate_preparation_time(data['items'])
        }
        
        orders_db[order_id] = order
        
        return jsonify({
            'success': True,
            'order': order,
            'message': 'Zamówienie utworzone pomyślnie'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/api/orders/<order_id>/generate-qr', methods=['POST'])
def generate_order_qr(order_id):
    """🎯 Generuj QR kod dla zamówienia"""
    try:
        if order_id not in orders_db:
            return jsonify({'success': False, 'error': 'Zamówienie nie znalezione'}), 404
        
        order = orders_db[order_id]
        
        # Sprawdź czy zamówienie może być opłacone
        if order['status'] != 'pending':
            return jsonify({'success': False, 'error': 'Zamówienie już przetworzone'}), 400
        
        # Dane do QR kodu
        qr_data = {
            'type': 'IKIGAI_ORDER',
            'order_id': order_id,
            'user_id': order['user_id'],
            'vending_machine_id': order['vending_machine_id'],
            'total_price': order['total_price'],
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Generowanie QR kodu
        qr_string = f"IKIGAI:ORDER:{order_id}:{order['vending_machine_id']}:{order['total_price']}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_string)
        qr.make(fit=True)
        
        # Tworzenie obrazu QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Konwersja do base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Zapisz QR kod
        qr_codes_db[order_id] = {
            'qr_string': qr_string,
            'qr_data': qr_data,
            'generated_at': datetime.datetime.now().isoformat(),
            'used': False
        }
        
        # Aktualizuj zamówienie
        order['status'] = 'paid'
        order['qr_code'] = qr_string
        
        return jsonify({
            'success': True,
            'qr_code': f"data:image/png;base64,{qr_base64}",
            'qr_string': qr_string,
            'order': order,
            'message': 'QR kod wygenerowany pomyślnie'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/api/orders/scan-qr', methods=['POST'])
def scan_qr_code():
    """📱 Skanuj QR kod w automacie i rozpocznij przygotowanie"""
    try:
        data = request.get_json()
        qr_string = data.get('qr_string')
        machine_id = data.get('machine_id')
        
        if not qr_string or not machine_id:
            return jsonify({'success': False, 'error': 'Brak danych QR lub ID automatu'}), 400
        
        # Parsowanie QR kodu
        if not qr_string.startswith('IKIGAI:ORDER:'):
            return jsonify({'success': False, 'error': 'Nieprawidłowy format QR kodu'}), 400
        
        parts = qr_string.split(':')
        if len(parts) < 5:
            return jsonify({'success': False, 'error': 'Nieprawidłowy QR kod'}), 400
        
        order_id = parts[2]
        expected_machine_id = parts[3]
        
        # Weryfikacja automatu
        if machine_id != expected_machine_id:
            return jsonify({
                'success': False, 
                'error': f'QR kod przeznaczony dla automatu {expected_machine_id}'
            }), 400
        
        # Sprawdź czy zamówienie istnieje
        if order_id not in orders_db:
            return jsonify({'success': False, 'error': 'Zamówienie nie znalezione'}), 404
        
        order = orders_db[order_id]
        
        # Sprawdź czy QR kod nie był użyty
        if order_id in qr_codes_db and qr_codes_db[order_id]['used']:
            return jsonify({'success': False, 'error': 'QR kod już został użyty'}), 400
        
        # Rozpocznij przygotowanie
        order['status'] = 'preparing'
        order['preparation_started_at'] = datetime.datetime.now().isoformat()
        
        if order_id in qr_codes_db:
            qr_codes_db[order_id]['used'] = True
            qr_codes_db[order_id]['used_at'] = datetime.datetime.now().isoformat()
        
        # Symulacja przygotowania (w rzeczywistości: komunikacja z automatem)
        preparation_steps = generate_preparation_steps(order['items'])
        
        return jsonify({
            'success': True,
            'order': order,
            'preparation_steps': preparation_steps,
            'estimated_completion': calculate_completion_time(order['preparation_time']),
            'message': 'Przygotowanie zamówienia rozpoczęte!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/api/orders/<order_id>/status', methods=['GET'])
def get_order_status(order_id):
    """📊 Sprawdź status zamówienia"""
    if order_id not in orders_db:
        return jsonify({'success': False, 'error': 'Zamówienie nie znalezione'}), 404
    
    order = orders_db[order_id]
    
    # Aktualizuj status na podstawie czasu
    if order['status'] == 'preparing':
        if is_order_ready(order):
            order['status'] = 'ready'
            order['ready_at'] = datetime.datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'order': order,
        'progress': calculate_progress(order)
    })

@orders_bp.route('/api/orders/<order_id>/complete', methods=['POST'])
def complete_order(order_id):
    """✅ Oznacz zamówienie jako odebrane"""
    if order_id not in orders_db:
        return jsonify({'success': False, 'error': 'Zamówienie nie znalezione'}), 404
    
    order = orders_db[order_id]
    order['status'] = 'completed'
    order['completed_at'] = datetime.datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'order': order,
        'message': 'Zamówienie zakończone pomyślnie!'
    })

# 🔧 HELPER FUNCTIONS

def calculate_order_price(items):
    """💰 Oblicz cenę zamówienia"""
    total = 0
    price_list = {
        'protein_shake': 12.99,
        'green_smoothie': 9.99,
        'energy_bar': 5.99,
        'vitamin_water': 7.99,
        'fresh_juice': 8.99
    }
    
    for item in items:
        item_id = item.get('id', '')
        quantity = item.get('quantity', 1)
        total += price_list.get(item_id, 0) * quantity
    
    return round(total, 2)

def estimate_preparation_time(items):
    """⏱️ Oszacuj czas przygotowania (sekundy)"""
    base_time = 30  # 30 sekund bazowy czas
    time_per_item = {
        'protein_shake': 45,
        'green_smoothie': 60,
        'energy_bar': 10,
        'vitamin_water': 15,
        'fresh_juice': 40
    }
    
    total_time = base_time
    for item in items:
        item_id = item.get('id', '')
        quantity = item.get('quantity', 1)
        total_time += time_per_item.get(item_id, 20) * quantity
    
    return total_time

def generate_preparation_steps(items):
    """📋 Generuj kroki przygotowania"""
    steps = ['Weryfikacja składników', 'Przygotowanie pojemników']
    
    for item in items:
        name = item.get('name', 'Nieznany produkt')
        steps.append(f'Przygotowanie: {name}')
    
    steps.extend(['Mieszanie składników', 'Finalizacja', 'Gotowe do odbioru'])
    return steps

def calculate_completion_time(prep_time_seconds):
    """⏰ Oblicz przewidywany czas zakończenia"""
    completion_time = datetime.datetime.now() + datetime.timedelta(seconds=prep_time_seconds)
    return completion_time.isoformat()

def is_order_ready(order):
    """✅ Sprawdź czy zamówienie jest gotowe"""
    if 'preparation_started_at' not in order:
        return False
    
    start_time = datetime.datetime.fromisoformat(order['preparation_started_at'])
    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    return elapsed >= order['preparation_time']

def calculate_progress(order):
    """📊 Oblicz postęp zamówienia (0-100%)"""
    if order['status'] in ['pending', 'paid']:
        return 0
    elif order['status'] == 'completed':
        return 100
    elif order['status'] == 'ready':
        return 95
    elif order['status'] == 'preparing':
        if 'preparation_started_at' not in order:
            return 10
        
        start_time = datetime.datetime.fromisoformat(order['preparation_started_at'])
        elapsed = (datetime.datetime.now() - start_time).total_seconds()
        progress = min(90, (elapsed / order['preparation_time']) * 80 + 10)
        return int(progress)
    
    return 0 