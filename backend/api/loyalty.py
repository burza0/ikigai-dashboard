"""
🏆 IKIGAI Loyalty Program
Program lojalnościowy - punkty, wyzwania, nagrody
"""

from flask import Blueprint, request, jsonify
import uuid
import datetime
from dateutil.relativedelta import relativedelta

loyalty_bp = Blueprint('loyalty', __name__)

# 🎯 WYZWANIA TYGODNIOWE
WEEKLY_CHALLENGES = [
    {
        "id": "healthy_week",
        "name": "🌱 Zdrowy Tydzień",
        "description": "Kup 5 mieszanek w ciągu tygodnia",
        "target": 5,
        "reward_points": 100,
        "reward_type": "points",
        "icon": "🌿",
        "difficulty": "easy"
    },
    {
        "id": "vegan_warrior",
        "name": "🌿 Vegan Warrior",
        "description": "Zamów 3 wegańskie bowls w tygodniu",
        "target": 3,
        "reward_points": 75,
        "reward_type": "points",
        "icon": "🌱",
        "difficulty": "medium"
    },
    {
        "id": "protein_power",
        "name": "💪 Protein Power",
        "description": "Wybierz 4 wysokobiałkowe bowls",
        "target": 4,
        "reward_points": 80,
        "reward_type": "points",
        "icon": "💪",
        "difficulty": "medium"
    },
    {
        "id": "early_bird",
        "name": "🌅 Early Bird",
        "description": "Zamów bowl przed 9:00 przez 3 dni",
        "target": 3,
        "reward_points": 60,
        "reward_type": "points",
        "icon": "⏰",
        "difficulty": "hard"
    },
    {
        "id": "mix_master",
        "name": "🎨 Mix Master",
        "description": "Stwórz 2 własne kompozycje",
        "target": 2,
        "reward_points": 120,
        "reward_type": "points",
        "icon": "🎯",
        "difficulty": "easy"
    }
]

# 🏅 NAGRODY I POZIOMY
LOYALTY_LEVELS = [
    {
        "level": 1,
        "name": "🌱 Początkujący",
        "points_required": 0,
        "benefits": ["5% zniżka na pierwszy bowl"],
        "badge": "🌱"
    },
    {
        "level": 2,
        "name": "🌿 Entuzjasta",
        "points_required": 200,
        "benefits": ["10% zniżka na wszystkie bowls", "Dostęp do ekskluzywnych składników"],
        "badge": "🌿"
    },
    {
        "level": 3,
        "name": "🏆 Mistrz IKIGAI",
        "points_required": 500,
        "benefits": ["15% zniżka", "Darmowy bowl co miesiąc", "Pierwszeństwo nowych składników"],
        "badge": "🏆"
    },
    {
        "level": 4,
        "name": "👑 Legenda Zdrowia",
        "points_required": 1000,
        "benefits": ["20% zniżka", "2 darmowe bowls miesięcznie", "Bezpłatna dostawa"],
        "badge": "👑"
    }
]

# 🎁 NAGRODY DO WYMIANY
REWARDS_SHOP = [
    {
        "id": "free_topping",
        "name": "🍓 Darmowy Dodatek",
        "description": "Dodaj jeden darmowy dodatek do bowl",
        "points_cost": 50,
        "type": "discount",
        "icon": "🍓"
    },
    {
        "id": "free_base",
        "name": "🥣 Darmowa Baza",
        "description": "Darmowa baza do następnego bowl",
        "points_cost": 80,
        "type": "discount",
        "icon": "🥣"
    },
    {
        "id": "free_mix",
        "name": "🎁 Darmowy Bowl",
        "description": "Całkowicie darmowy bowl",
        "points_cost": 150,
        "type": "freebie",
        "icon": "🎁"
    },
    {
        "id": "double_points",
        "name": "⚡ Podwójne Punkty",
        "description": "Podwójne punkty przez następne 3 zakupy",
        "points_cost": 100,
        "type": "multiplier",
        "icon": "⚡"
    },
    {
        "id": "exclusive_ingredient",
        "name": "⭐ Ekskluzywny Składnik",
        "description": "Dostęp do limitowanego składnika",
        "points_cost": 200,
        "type": "exclusive",
        "icon": "⭐"
    }
]

# 💾 In-memory storage
user_loyalty = {}
user_challenges = {}
user_rewards = {}

@loyalty_bp.route('/api/loyalty/profile/<user_id>', methods=['GET'])
def get_loyalty_profile(user_id):
    """👤 Pobierz profil lojalnościowy użytkownika"""
    
    # Domyślny profil dla nowego użytkownika
    if user_id not in user_loyalty:
        user_loyalty[user_id] = {
            'user_id': user_id,
            'points': 0,
            'level': 1,
            'total_orders': 0,
            'total_spent': 0.0,
            'joined_date': datetime.datetime.now().isoformat(),
            'badges': ['🌱'],
            'favorite_base': None,
            'favorite_toppings': []
        }
    
    profile = user_loyalty[user_id]
    
    # Określ aktualny poziom na podstawie punktów
    current_level = 1
    for level_info in LOYALTY_LEVELS:
        if profile['points'] >= level_info['points_required']:
            current_level = level_info['level']
        else:
            break
    
    profile['level'] = current_level
    current_level_info = next(l for l in LOYALTY_LEVELS if l['level'] == current_level)
    
    # Następny poziom
    next_level_info = None
    if current_level < len(LOYALTY_LEVELS):
        next_level_info = next((l for l in LOYALTY_LEVELS if l['level'] == current_level + 1), None)
    
    return jsonify({
        'success': True,
        'profile': profile,
        'current_level': current_level_info,
        'next_level': next_level_info,
        'points_to_next_level': next_level_info['points_required'] - profile['points'] if next_level_info else 0
    })

@loyalty_bp.route('/api/loyalty/challenges/<user_id>', methods=['GET'])
def get_user_challenges(user_id):
    """🎯 Pobierz wyzwania użytkownika"""
    
    # Inicjalizuj wyzwania jeśli nie istnieją
    if user_id not in user_challenges:
        user_challenges[user_id] = {}
        
        # Przypisz 3 losowe wyzwania na tydzień
        import random
        weekly_challenges = random.sample(WEEKLY_CHALLENGES, 3)
        
        for challenge in weekly_challenges:
            challenge_id = challenge['id']
            user_challenges[user_id][challenge_id] = {
                'challenge': challenge,
                'progress': 0,
                'completed': False,
                'assigned_date': datetime.datetime.now().isoformat(),
                'expires_date': (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
            }
    
    # Sprawdź wygaśnięte wyzwania
    current_time = datetime.datetime.now()
    for challenge_id, challenge_data in list(user_challenges[user_id].items()):
        expires_date = datetime.datetime.fromisoformat(challenge_data['expires_date'])
        if current_time > expires_date and not challenge_data['completed']:
            # Usuń wygaśnięte wyzwanie
            del user_challenges[user_id][challenge_id]
    
    return jsonify({
        'success': True,
        'challenges': list(user_challenges[user_id].values()),
        'count': len(user_challenges[user_id])
    })

@loyalty_bp.route('/api/loyalty/rewards', methods=['GET'])
def get_rewards_shop():
    """🎁 Pobierz sklep nagród"""
    return jsonify({
        'success': True,
        'rewards': REWARDS_SHOP,
        'count': len(REWARDS_SHOP)
    })

@loyalty_bp.route('/api/loyalty/redeem', methods=['POST'])
def redeem_reward():
    """🏆 Wymień punkty na nagrodę"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        reward_id = data.get('reward_id')
        
        if not user_id or not reward_id:
            return jsonify({'success': False, 'error': 'Brak user_id lub reward_id'}), 400
        
        # Sprawdź nagrodę
        reward = next((r for r in REWARDS_SHOP if r['id'] == reward_id), None)
        if not reward:
            return jsonify({'success': False, 'error': 'Nagroda nie znaleziona'}), 404
        
        # Sprawdź profil użytkownika
        if user_id not in user_loyalty:
            return jsonify({'success': False, 'error': 'Profil użytkownika nie znaleziony'}), 404
        
        profile = user_loyalty[user_id]
        
        # Sprawdź czy użytkownik ma wystarczająco punktów
        if profile['points'] < reward['points_cost']:
            return jsonify({
                'success': False, 
                'error': f'Niewystarczająco punktów. Potrzebujesz {reward["points_cost"]}, masz {profile["points"]}'
            }), 400
        
        # Pobierz punkty
        profile['points'] -= reward['points_cost']
        
        # Zapisz wykorzystaną nagrodę
        if user_id not in user_rewards:
            user_rewards[user_id] = []
        
        redeemed_reward = {
            'reward': reward,
            'redeemed_date': datetime.datetime.now().isoformat(),
            'used': False,
            'expires_date': (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
        }
        
        user_rewards[user_id].append(redeemed_reward)
        
        return jsonify({
            'success': True,
            'message': f'Pomyślnie wymieniono: {reward["name"]}',
            'reward': redeemed_reward,
            'remaining_points': profile['points']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@loyalty_bp.route('/api/loyalty/points/add', methods=['POST'])
def add_points():
    """⭐ Dodaj punkty użytkownikowi (po zakupie)"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        points = data.get('points', 0)
        reason = data.get('reason', 'Zakup')
        order_amount = data.get('order_amount', 0)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'Brak user_id'}), 400
        
        # Inicjalizuj profil jeśli nie istnieje
        if user_id not in user_loyalty:
            user_loyalty[user_id] = {
                'user_id': user_id,
                'points': 0,
                'level': 1,
                'total_orders': 0,
                'total_spent': 0.0,
                'joined_date': datetime.datetime.now().isoformat(),
                'badges': ['🌱'],
                'favorite_base': None,
                'favorite_toppings': []
            }
        
        profile = user_loyalty[user_id]
        
        # Oblicz punkty na podstawie kwoty zamówienia (1 punkt za każde 1 PLN)
        if order_amount > 0:
            points = int(order_amount)
        
        # Dodaj punkty
        profile['points'] += points
        profile['total_orders'] += 1
        profile['total_spent'] += order_amount
        
        # Sprawdź czy użytkownik awansował na wyższy poziom
        old_level = profile['level']
        new_level = 1
        
        for level_info in LOYALTY_LEVELS:
            if profile['points'] >= level_info['points_required']:
                new_level = level_info['level']
            else:
                break
        
        level_up = new_level > old_level
        profile['level'] = new_level
        
        if level_up:
            new_level_info = next(l for l in LOYALTY_LEVELS if l['level'] == new_level)
            profile['badges'].append(new_level_info['badge'])
        
        return jsonify({
            'success': True,
            'points_added': points,
            'total_points': profile['points'],
            'level_up': level_up,
            'new_level': new_level if level_up else None,
            'message': f'Dodano {points} punktów za {reason}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@loyalty_bp.route('/api/loyalty/challenge/progress', methods=['POST'])
def update_challenge_progress():
    """📈 Aktualizuj postęp w wyzwaniu"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        challenge_type = data.get('challenge_type')  # np. 'vegan_order', 'morning_order', etc.
        
        if not user_id or not challenge_type:
            return jsonify({'success': False, 'error': 'Brak user_id lub challenge_type'}), 400
        
        if user_id not in user_challenges:
            return jsonify({'success': True, 'message': 'Brak aktywnych wyzwań'})
        
        completed_challenges = []
        
        # Sprawdź wszystkie aktywne wyzwania użytkownika
        for challenge_id, challenge_data in user_challenges[user_id].items():
            if challenge_data['completed']:
                continue
                
            challenge = challenge_data['challenge']
            
            # Logika aktualizacji postępu na podstawie typu wyzwania
            should_update = False
            
            if challenge_id == 'healthy_week':
                should_update = True  # Każdy zakup liczy się
            elif challenge_id == 'vegan_warrior' and challenge_type == 'vegan_order':
                should_update = True
            elif challenge_id == 'protein_power' and challenge_type == 'protein_order':
                should_update = True
            elif challenge_id == 'early_bird' and challenge_type == 'morning_order':
                should_update = True
            elif challenge_id == 'mix_master' and challenge_type == 'custom_mix':
                should_update = True
            
            if should_update:
                challenge_data['progress'] += 1
                
                # Sprawdź czy wyzwanie zostało ukończone
                if challenge_data['progress'] >= challenge['target']:
                    challenge_data['completed'] = True
                    challenge_data['completed_date'] = datetime.datetime.now().isoformat()
                    
                    # Dodaj punkty za ukończenie wyzwania
                    if user_id in user_loyalty:
                        user_loyalty[user_id]['points'] += challenge['reward_points']
                    
                    completed_challenges.append({
                        'challenge': challenge,
                        'reward_points': challenge['reward_points']
                    })
        
        return jsonify({
            'success': True,
            'completed_challenges': completed_challenges,
            'message': f'Zaktualizowano postęp dla {len(completed_challenges)} wyzwań'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 