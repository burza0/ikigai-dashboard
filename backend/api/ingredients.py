"""
🥣 IKIGAI Ingredients Management
System składników i mieszanek - Kompozycja szczęścia
"""

from flask import Blueprint, request, jsonify
import uuid
import datetime

ingredients_bp = Blueprint('ingredients', __name__)

# 🥄 BAZY - Fundament mieszanki
BASES = [
    {
        "id": "yogurt_greek",
        "name": "Jogurt Grecki",
        "category": "base",
        "icon": "🥛",
        "price": 4.50,
        "description": "Kremowy jogurt grecki, wysokobiałkowy",
        "nutrition": {"protein": 15, "carbs": 6, "fat": 4, "kcal": 120},
        "dietary_labels": ["High-Protein", "Vegetarian", "Gluten-Free"],
        "origin": "Grecja"
    },
    {
        "id": "granola_bio",
        "name": "Granola BIO",
        "category": "base", 
        "icon": "🌾",
        "price": 3.80,
        "description": "Chrupiąca granola z płatków owsianych i orzechów",
        "nutrition": {"protein": 8, "carbs": 45, "fat": 12, "kcal": 280},
        "dietary_labels": ["Organic", "Vegan", "High-Fiber"],
        "origin": "Polska"
    },
    {
        "id": "oatmeal_base",
        "name": "Owsianka OATLY",
        "category": "base",
        "icon": "🥣",
        "price": 2.90,
        "description": "Klasyczna owsianka na mleku owsianym OATLY",
        "nutrition": {"protein": 6, "carbs": 35, "fat": 3, "kcal": 180},
        "dietary_labels": ["Vegan", "Gluten-Free", "OATLY"],
        "origin": "Skandynavia"
    },
    {
        "id": "smoothie_bowl",
        "name": "Smoothie Bowl",
        "category": "base",
        "icon": "🍓",
        "price": 5.20,
        "description": "Kremowy smoothie bowl z owoców sezonowych",
        "nutrition": {"protein": 4, "carbs": 28, "fat": 2, "kcal": 140},
        "dietary_labels": ["Vegan", "Raw", "Antioxidant-Rich"],
        "origin": "Tropiki"
    }
]

# 🍓 DODATKI - Składniki szczęścia
TOPPINGS = [
    {
        "id": "berries_mix",
        "name": "Mix Jagód",
        "category": "topping",
        "icon": "🫐",
        "price": 2.20,
        "description": "Borówki, maliny, jeżyny - bomba antyoksydantów",
        "nutrition": {"protein": 1, "carbs": 12, "fat": 0, "kcal": 50},
        "dietary_labels": ["Vegan", "Antioxidant-Rich", "Super-Food"],
        "origin": "Lasy Skandynawskie"
    },
    {
        "id": "nuts_almonds",
        "name": "Migdały",
        "category": "topping",
        "icon": "🌰",
        "price": 1.80,
        "description": "Prażone migdały - źródło zdrowych tłuszczy",
        "nutrition": {"protein": 6, "carbs": 3, "fat": 14, "kcal": 160},
        "dietary_labels": ["Vegan", "High-Protein", "Keto-Friendly"],
        "origin": "California"
    },
    {
        "id": "chia_seeds",
        "name": "Nasiona Chia",
        "category": "topping", 
        "icon": "🌱",
        "price": 1.50,
        "description": "Superfood pełen omega-3 i błonnika",
        "nutrition": {"protein": 5, "carbs": 4, "fat": 9, "kcal": 130},
        "dietary_labels": ["Vegan", "Super-Food", "High-Fiber", "Omega-3"],
        "origin": "Ameryka Południowa"
    },
    {
        "id": "banana_sliced",
        "name": "Banan w plasterkach",
        "category": "topping",
        "icon": "🍌",
        "price": 1.20,
        "description": "Świeży banan - naturalny cukier i potas",
        "nutrition": {"protein": 1, "carbs": 20, "fat": 0, "kcal": 80},
        "dietary_labels": ["Vegan", "Natural-Sugar", "Potassium-Rich"],
        "origin": "Ekwador"
    },
    {
        "id": "coconut_flakes",
        "name": "Płatki Kokosowe",
        "category": "topping",
        "icon": "🥥",
        "price": 1.40,
        "description": "Suszone płatki kokosowe - egzotyczny smak",
        "nutrition": {"protein": 2, "carbs": 6, "fat": 18, "kcal": 180},
        "dietary_labels": ["Vegan", "Keto-Friendly", "Tropical"],
        "origin": "Filipiny"
    },
    {
        "id": "honey_raw",
        "name": "Miód Naturalny",
        "category": "topping",
        "icon": "🍯",
        "price": 1.60,
        "description": "Surowy miód - słodycz natury",
        "nutrition": {"protein": 0, "carbs": 17, "fat": 0, "kcal": 64},
        "dietary_labels": ["Vegetarian", "Natural-Sugar", "Antibacterial"],
        "origin": "Polskie Pasieki"
    }
]

# 🌟 TOP 5 REKOMENDACJI IKIGAI
TOP_RECOMMENDATIONS = [
    {
        "id": "morning_warrior",
        "name": "🌅 Morning Warrior",
        "description": "Energetyczny start dnia - owsianka z jagodami i migdałami",
        "base": "oatmeal_base",
        "toppings": ["berries_mix", "nuts_almonds", "honey_raw"],
        "total_price": 7.80,
        "popularity": 95,
        "health_score": 92,
        "tags": ["Energetyczne", "High-Protein", "Antioxidanty"]
    },
    {
        "id": "tropical_bliss",
        "name": "🏝️ Tropical Bliss", 
        "description": "Egzotyczna przyjemność - smoothie bowl z kokosem i bananem",
        "base": "smoothie_bowl",
        "toppings": ["banana_sliced", "coconut_flakes", "chia_seeds"],
        "total_price": 8.90,
        "popularity": 88,
        "health_score": 85,
        "tags": ["Tropikalne", "Vegan", "Omega-3"]
    },
    {
        "id": "protein_power",
        "name": "💪 Protein Power",
        "description": "Białkowa bomba - jogurt grecki z orzechami",
        "base": "yogurt_greek",
        "toppings": ["nuts_almonds", "chia_seeds"],
        "total_price": 7.80,
        "popularity": 91,
        "health_score": 96,
        "tags": ["High-Protein", "Post-Workout", "Super-Food"]
    },
    {
        "id": "antioxidant_boost",
        "name": "🫐 Antioxidant Boost",
        "description": "Naturalna ochrona - granola z mix jagód i miodem",
        "base": "granola_bio", 
        "toppings": ["berries_mix", "honey_raw"],
        "total_price": 7.60,
        "popularity": 82,
        "health_score": 89,
        "tags": ["Antioxidanty", "Organic", "Detoks"]
    },
    {
        "id": "vegan_delight",
        "name": "🌱 Vegan Delight",
        "description": "Roślinne szczęście - wszystko co najlepsze dla wegan",
        "base": "oatmeal_base",
        "toppings": ["banana_sliced", "chia_seeds"],
        "total_price": 5.60,
        "popularity": 79,
        "health_score": 87,
        "tags": ["100% Vegan", "Super-Food", "Energia"]
    }
]

# 🎯 In-memory storage
user_mixes = {}

@ingredients_bp.route('/api/ingredients/bases', methods=['GET'])
def get_bases():
    """🥄 Pobierz wszystkie dostępne bazy"""
    return jsonify({
        'success': True,
        'bases': BASES,
        'count': len(BASES)
    })

@ingredients_bp.route('/api/ingredients/toppings', methods=['GET'])
def get_toppings():
    """🍓 Pobierz wszystkie dostępne dodatki"""
    return jsonify({
        'success': True,
        'toppings': TOPPINGS,
        'count': len(TOPPINGS)
    })

@ingredients_bp.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """🌟 Pobierz Top 5 rekomendacji IKIGAI"""
    return jsonify({
        'success': True,
        'recommendations': TOP_RECOMMENDATIONS,
        'count': len(TOP_RECOMMENDATIONS),
        'message': 'Top 5 najpopularniejszych mieszanek IKIGAI'
    })

@ingredients_bp.route('/api/mix/create', methods=['POST'])
def create_custom_mix():
    """🎨 Skomponuj własną mieszankę"""
    try:
        data = request.get_json()
        
        base_id = data.get('base_id')
        topping_ids = data.get('topping_ids', [])
        mix_name = data.get('name', 'Moja Mieszanka')
        user_id = data.get('user_id', 'anonymous')
        
        # Znajdź bazę
        base = next((b for b in BASES if b['id'] == base_id), None)
        if not base:
            return jsonify({'success': False, 'error': 'Nieznana baza'}), 400
        
        # Znajdź dodatki
        toppings = []
        for topping_id in topping_ids:
            topping = next((t for t in TOPPINGS if t['id'] == topping_id), None)
            if topping:
                toppings.append(topping)
        
        # Oblicz wartości
        total_nutrition = base['nutrition'].copy()
        total_price = base['price']
        all_labels = set(base['dietary_labels'])
        
        for topping in toppings:
            total_price += topping['price']
            for key in total_nutrition:
                total_nutrition[key] += topping['nutrition'][key]
            all_labels.update(topping['dietary_labels'])
        
        # Stwórz mieszankę
        mix_id = str(uuid.uuid4())
        custom_mix = {
            'id': mix_id,
            'name': mix_name,
            'user_id': user_id,
            'base': base,
            'toppings': toppings,
            'total_nutrition': total_nutrition,
            'total_price': round(total_price, 2),
            'dietary_labels': sorted(list(all_labels)),
            'created_at': datetime.datetime.now().isoformat()
        }
        
        # Zapisz mieszankę
        if user_id not in user_mixes:
            user_mixes[user_id] = []
        user_mixes[user_id].append(custom_mix)
        
        return jsonify({
            'success': True,
            'mix': custom_mix,
            'message': f'Mieszanka "{mix_name}" została utworzona!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
