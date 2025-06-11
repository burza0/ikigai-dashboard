"""
🥤 IKIGAI Products Management
Katalog produktów zdrowotnych z automatów vendingowych
"""

from flask import Blueprint, request, jsonify

products_bp = Blueprint('products', __name__)

# 🍃 Demo produkty IKIGAI
IKIGAI_PRODUCTS = {
    'protein_shake': {
        'id': 'protein_shake',
        'name': 'Protein Shake',
        'category': 'shakes',
        'description': 'Wysokobiałkowy koktajl z naturalnym białkiem',
        'price': 12.99,
        'preparation_time': 45,  # sekundy
        'calories': 150,
        'protein': 25,
        'ingredients': ['whey_protein', 'almond_milk', 'vanilla', 'stevia'],
        'allergens': ['milk', 'nuts'],
        'dietary_labels': ['high_protein', 'low_sugar'],
        'available': True,
        'image': 'https://via.placeholder.com/200x200/4CAF50/white?text=Protein',
        'nutrition': {
            'calories': 150,
            'protein': 25,
            'carbs': 8,
            'fat': 3,
            'fiber': 2,
            'sugar': 4
        }
    },
    'green_smoothie': {
        'id': 'green_smoothie',
        'name': 'Green Power Smoothie',
        'category': 'smoothies',
        'description': 'Zielony smoothie pełen witamin i minerałów',
        'price': 9.99,
        'preparation_time': 60,
        'calories': 120,
        'protein': 8,
        'ingredients': ['spinach', 'banana', 'apple', 'ginger', 'coconut_water'],
        'allergens': [],
        'dietary_labels': ['vegan', 'raw', 'detox', 'vitamin_rich'],
        'available': True,
        'image': 'https://via.placeholder.com/200x200/8BC34A/white?text=Green',
        'nutrition': {
            'calories': 120,
            'protein': 8,
            'carbs': 28,
            'fat': 1,
            'fiber': 6,
            'sugar': 18
        }
    },
    'energy_bar': {
        'id': 'energy_bar',
        'name': 'Energy Bar',
        'category': 'bars',
        'description': 'Baton energetyczny z orzechami i owocami',
        'price': 5.99,
        'preparation_time': 10,
        'calories': 220,
        'protein': 12,
        'ingredients': ['almonds', 'dates', 'oats', 'chia_seeds', 'dark_chocolate'],
        'allergens': ['nuts'],
        'dietary_labels': ['vegan', 'gluten_free', 'energy_boost'],
        'available': True,
        'image': 'https://via.placeholder.com/200x200/FF9800/white?text=Energy',
        'nutrition': {
            'calories': 220,
            'protein': 12,
            'carbs': 25,
            'fat': 8,
            'fiber': 4,
            'sugar': 15
        }
    },
    'vitamin_water': {
        'id': 'vitamin_water',
        'name': 'Vitamin Water',
        'category': 'drinks',
        'description': 'Woda wzbogacona witaminami i minerałami',
        'price': 7.99,
        'preparation_time': 15,
        'calories': 50,
        'protein': 0,
        'ingredients': ['spring_water', 'vitamin_c', 'vitamin_b', 'electrolytes', 'natural_flavor'],
        'allergens': [],
        'dietary_labels': ['vitamin_enriched', 'hydrating', 'zero_fat'],
        'available': True,
        'image': 'https://via.placeholder.com/200x200/2196F3/white?text=Vitamin',
        'nutrition': {
            'calories': 50,
            'protein': 0,
            'carbs': 13,
            'fat': 0,
            'fiber': 0,
            'sugar': 12
        }
    },
    'fresh_juice': {
        'id': 'fresh_juice',
        'name': 'Fresh Orange Juice',
        'category': 'juices',
        'description': 'Świeżo wyciskany sok pomarańczowy',
        'price': 8.99,
        'preparation_time': 40,
        'calories': 110,
        'protein': 2,
        'ingredients': ['fresh_oranges', 'no_added_sugar'],
        'allergens': [],
        'dietary_labels': ['fresh', 'vitamin_c_rich', 'natural'],
        'available': True,
        'image': 'https://via.placeholder.com/200x200/FF5722/white?text=Orange',
        'nutrition': {
            'calories': 110,
            'protein': 2,
            'carbs': 26,
            'fat': 0,
            'fiber': 0,
            'sugar': 21
        }
    },
    'berry_bowl': {
        'id': 'berry_bowl',
        'name': 'Antioxidant Berry Bowl',
        'category': 'bowls',
        'description': 'Miska pełna antyoksydantów z jagód i orzechów',
        'price': 11.99,
        'preparation_time': 50,
        'calories': 180,
        'protein': 6,
        'ingredients': ['blueberries', 'strawberries', 'raspberries', 'granola', 'greek_yogurt'],
        'allergens': ['milk', 'gluten'],
        'dietary_labels': ['antioxidant_rich', 'probiotic', 'high_fiber'],
        'available': True,
        'image': 'https://via.placeholder.com/200x200/9C27B0/white?text=Berry',
        'nutrition': {
            'calories': 180,
            'protein': 6,
            'carbs': 35,
            'fat': 4,
            'fiber': 8,
            'sugar': 24
        }
    }
}

# 🏪 Demo automaty vendingowe
VENDING_MACHINES = {
    'vm001': {
        'id': 'vm001',
        'name': 'IKIGAI Central',
        'location': 'Centrum Handlowe - Poziom 1',
        'address': 'ul. Główna 123, Warszawa',
        'coordinates': {'lat': 52.2297, 'lng': 21.0122},
        'status': 'online',
        'available_products': ['protein_shake', 'green_smoothie', 'energy_bar', 'vitamin_water'],
        'capacity': 50,
        'current_stock': 42,
        'last_refill': '2025-06-10T08:00:00',
        'operating_hours': '06:00-22:00',
        'payment_methods': ['card', 'mobile', 'qr_code']
    },
    'vm002': {
        'id': 'vm002', 
        'name': 'IKIGAI Fitness',
        'location': 'Siłownia FitZone',
        'address': 'ul. Sportowa 45, Warszawa',
        'coordinates': {'lat': 52.2500, 'lng': 21.0000},
        'status': 'online',
        'available_products': ['protein_shake', 'energy_bar', 'vitamin_water', 'fresh_juice'],
        'capacity': 30,
        'current_stock': 28,
        'last_refill': '2025-06-10T07:30:00',
        'operating_hours': '05:00-23:00',
        'payment_methods': ['card', 'mobile', 'qr_code']
    },
    'vm003': {
        'id': 'vm003',
        'name': 'IKIGAI Office',
        'location': 'Biurowiec Alpha Tower',
        'address': 'ul. Biznesowa 78, Warszawa',
        'coordinates': {'lat': 52.2200, 'lng': 21.0300},
        'status': 'maintenance',
        'available_products': ['green_smoothie', 'berry_bowl', 'vitamin_water', 'fresh_juice'],
        'capacity': 40,
        'current_stock': 0,
        'last_refill': '2025-06-09T16:00:00',
        'operating_hours': '07:00-19:00',
        'payment_methods': ['card', 'mobile', 'qr_code']
    },
    'vm004': {
        'id': 'vm004',
        'name': 'IKIGAI University',
        'location': 'Uniwersytet Warszawski - Biblioteka',
        'address': 'ul. Krakowskie Przedmieście 26/28, Warszawa',
        'coordinates': {'lat': 52.2400, 'lng': 21.0200},
        'status': 'online',
        'available_products': ['green_smoothie', 'berry_bowl', 'energy_bar', 'vitamin_water'],
        'capacity': 35,
        'current_stock': 31,
        'last_refill': '2025-06-10T09:00:00',
        'operating_hours': '06:00-22:00',
        'payment_methods': ['card', 'mobile', 'qr_code']
    },
    'vm005': {
        'id': 'vm005',
        'name': 'IKIGAI Park',
        'location': 'Park Łazienkowski - Wejście główne',
        'address': 'ul. Agrykola 1, Warszawa',
        'coordinates': {'lat': 52.2150, 'lng': 21.0350},
        'status': 'online',
        'available_products': ['fresh_juice', 'vitamin_water', 'energy_bar', 'berry_bowl'],
        'capacity': 25,
        'current_stock': 23,
        'last_refill': '2025-06-10T07:00:00',
        'operating_hours': '05:30-21:00',
        'payment_methods': ['card', 'mobile', 'qr_code']
    }
}

@products_bp.route('/api/products', methods=['GET'])
def get_products():
    """🛍️ Pobierz katalog produktów"""
    category = request.args.get('category')
    dietary_filter = request.args.get('dietary')
    available_only = request.args.get('available', 'true').lower() == 'true'
    
    products = list(IKIGAI_PRODUCTS.values())
    
    # Filtruj według kategorii
    if category:
        products = [p for p in products if p['category'] == category]
    
    # Filtruj według oznaczeń dietetycznych
    if dietary_filter:
        products = [p for p in products if dietary_filter in p['dietary_labels']]
    
    # Filtruj dostępne produkty
    if available_only:
        products = [p for p in products if p['available']]
    
    return jsonify({
        'success': True,
        'products': products,
        'count': len(products),
        'categories': list(set(p['category'] for p in IKIGAI_PRODUCTS.values())),
        'dietary_labels': get_all_dietary_labels()
    })

@products_bp.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """📦 Pobierz szczegóły produktu"""
    if product_id not in IKIGAI_PRODUCTS:
        return jsonify({'success': False, 'error': 'Produkt nie znaleziony'}), 404
    
    return jsonify({
        'success': True,
        'product': IKIGAI_PRODUCTS[product_id]
    })

@products_bp.route('/api/vending-machines', methods=['GET'])
def get_vending_machines():
    """🏪 Pobierz listę automatów vendingowych"""
    status_filter = request.args.get('status')
    location = request.args.get('location')
    
    machines = list(VENDING_MACHINES.values())
    
    # Filtruj według statusu
    if status_filter:
        machines = [m for m in machines if m['status'] == status_filter]
    
    # Filtruj według lokalizacji (wyszukiwanie w nazwie/adresie)
    if location:
        location_lower = location.lower()
        machines = [m for m in machines if 
                   location_lower in m['location'].lower() or 
                   location_lower in m['address'].lower()]
    
    return jsonify({
        'success': True,
        'machines': machines,
        'count': len(machines),
        'online_count': len([m for m in machines if m['status'] == 'online'])
    })

@products_bp.route('/api/vending-machines/<machine_id>', methods=['GET'])
def get_vending_machine(machine_id):
    """🏪 Pobierz szczegóły automatu"""
    if machine_id not in VENDING_MACHINES:
        return jsonify({'success': False, 'error': 'Automat nie znaleziony'}), 404
    
    machine = VENDING_MACHINES[machine_id].copy()
    
    # Dodaj dostępne produkty z pełnymi informacjami
    available_products_details = []
    for product_id in machine['available_products']:
        if product_id in IKIGAI_PRODUCTS:
            available_products_details.append(IKIGAI_PRODUCTS[product_id])
    
    machine['available_products_details'] = available_products_details
    
    return jsonify({
        'success': True,
        'machine': machine
    })

@products_bp.route('/api/categories', methods=['GET'])
def get_categories():
    """📂 Pobierz kategorie produktów"""
    categories = {}
    for product in IKIGAI_PRODUCTS.values():
        cat = product['category']
        if cat not in categories:
            categories[cat] = {
                'name': cat,
                'count': 0,
                'products': []
            }
        categories[cat]['count'] += 1
        categories[cat]['products'].append(product['id'])
    
    return jsonify({
        'success': True,
        'categories': list(categories.values())
    })

@products_bp.route('/api/dietary-labels', methods=['GET'])
def get_dietary_labels():
    """🌱 Pobierz oznaczenia dietetyczne"""
    return jsonify({
        'success': True,
        'dietary_labels': get_all_dietary_labels()
    })

def get_all_dietary_labels():
    """📋 Pomocnicza funkcja - pobierz wszystkie oznaczenia dietetyczne"""
    labels = set()
    for product in IKIGAI_PRODUCTS.values():
        labels.update(product['dietary_labels'])
    
    # Mapowanie etykiet na opis
    label_descriptions = {
        'vegan': 'Wegańskie',
        'gluten_free': 'Bez glutenu',
        'high_protein': 'Wysokobiałkowe',
        'low_sugar': 'Mało cukru',
        'raw': 'Surowe',
        'detox': 'Detoks',
        'vitamin_rich': 'Bogate w witaminy',
        'energy_boost': 'Dodaje energii',
        'vitamin_enriched': 'Wzbogacone witaminami',
        'hydrating': 'Nawadniające',
        'zero_fat': 'Bez tłuszczu',
        'fresh': 'Świeże',
        'vitamin_c_rich': 'Bogate w witaminę C',
        'natural': 'Naturalne',
        'antioxidant_rich': 'Bogate w antyoksydanty',
        'probiotic': 'Probiotyczne',
        'high_fiber': 'Wysokobłonnikowe'
    }
    
    return [
        {
            'id': label,
            'name': label_descriptions.get(label, label.replace('_', ' ').title()),
            'count': sum(1 for p in IKIGAI_PRODUCTS.values() if label in p['dietary_labels'])
        }
        for label in sorted(labels)
    ] 