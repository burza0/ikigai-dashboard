#!/usr/bin/env python3
"""
🔍 IKIGAI Data Explorer
Prosty eksplorator danych aplikacji IKIGAI
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:5001"

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def print_json(data, indent=2):
    print(json.dumps(data, indent=indent, ensure_ascii=False))

def explore_recipes():
    """Eksploruj przepisy"""
    print_header("PRZEPISY MIESZANEK")
    
    try:
        response = requests.get(f"{API_BASE}/api/meal-recipes")
        if response.status_code == 200:
            data = response.json()
            recipes = data.get('data', [])
            
            print(f"📋 Znaleziono {len(recipes)} przepisów:")
            for recipe in recipes:
                print(f"\n🍜 {recipe['name']}")
                print(f"   📂 Kategoria: {recipe['category']}")
                print(f"   💰 Cena: {recipe['price']}zł")
                print(f"   🏥 Health Score: {recipe['health_score']}/100")
                print(f"   🧪 Składniki: {', '.join(recipe['ingredients'])}")
        else:
            print(f"❌ Błąd: {response.status_code}")
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")

def explore_loyalty():
    """Eksploruj program lojalnościowy"""
    print_header("PROGRAM LOJALNOŚCIOWY")
    
    try:
        # Profil użytkownika
        response = requests.get(f"{API_BASE}/api/loyalty/profile/web_user")
        if response.status_code == 200:
            profile = response.json()['data']
            print(f"👤 Użytkownik: {profile['name']}")
            print(f"🏆 Poziom: {profile['level']} - {profile['level_name']}")
            print(f"⭐ Punkty: {profile['points']}")
            print(f"📧 Email: {profile['email']}")
            print(f"🛒 Zamówienia: {profile['total_orders']}")
            print(f"💸 Wydane: {profile['total_spent']}zł")
        
        # Wyzwania
        response = requests.get(f"{API_BASE}/api/loyalty/challenges/web_user")
        if response.status_code == 200:
            challenges = response.json()['data']
            print(f"\n🎯 Aktywne wyzwania ({len(challenges)}):")
            for challenge in challenges:
                status = "✅ Ukończone" if challenge['status'] == 'completed' else "🔄 W toku"
                print(f"   {challenge['name']} - {status}")
                print(f"   📊 Postęp: {challenge['progress']}/{challenge['target']}")
                print(f"   🎁 Nagroda: {challenge['reward_points']} punktów")
        
        # Nagrody
        response = requests.get(f"{API_BASE}/api/loyalty/rewards")
        if response.status_code == 200:
            rewards = response.json()['data']
            print(f"\n🏪 Dostępne nagrody ({len(rewards)}):")
            for reward in rewards:
                print(f"   🎁 {reward['name']} - {reward['cost']} punktów")
                
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")

def explore_analytics():
    """Eksploruj statystyki"""
    print_header("STATYSTYKI SPRZEDAŻY")
    
    try:
        response = requests.get(f"{API_BASE}/api/analytics/dashboard")
        if response.status_code == 200:
            data = response.json()['data']
            
            sales = data['sales']
            print(f"💰 Sprzedaż dzisiaj: {sales['today']}zł")
            print(f"📈 Wzrost dzienny: +{sales['growth_daily']}%")
            print(f"📅 Ten tydzień: {sales['this_week']}zł")
            print(f"📆 Ten miesiąc: {sales['this_month']}zł")
            
            orders = data['orders']
            print(f"\n🛒 Zamówienia:")
            print(f"   Łącznie: {orders['total']}")
            print(f"   Dzisiaj: {orders['today']}")
            print(f"   Ukończone: {orders['completed']}")
            print(f"   Oczekujące: {orders['pending']}")
            
            machines = data['machines']
            print(f"\n🤖 Automaty:")
            print(f"   Łącznie: {machines['total']}")
            print(f"   Online: {machines['online']}")
            print(f"   Uptime: {machines['uptime']}%")
            
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")

def explore_ingredients():
    """Eksploruj składniki"""
    print_header("SKŁADNIKI")
    
    try:
        response = requests.get(f"{API_BASE}/api/ingredients/categories")
        if response.status_code == 200:
            data = response.json()['categories']
            
            print("🧪 Kategorie składników:")
            for category, info in data.items():
                print(f"\n📂 {category.upper()}:")
                if 'items' in info:
                    for item in info['items'][:3]:  # Pokaz tylko pierwsze 3
                        print(f"   • {item.get('name', item)}")
                    if len(info['items']) > 3:
                        print(f"   ... i {len(info['items']) - 3} więcej")
                        
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")

def main():
    print(f"""
🎯 IKIGAI Data Explorer
Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Wybierz opcję:
1. 🍜 Przepisy mieszanek
2. 🏆 Program lojalnościowy  
3. 📊 Statystyki sprzedaży
4. 🧪 Składniki
5. 🌐 Wszystko
0. ❌ Wyjście
""")
    
    try:
        choice = input("Twój wybór (0-5): ").strip()
        
        if choice == "1":
            explore_recipes()
        elif choice == "2":
            explore_loyalty()
        elif choice == "3":
            explore_analytics()
        elif choice == "4":
            explore_ingredients()
        elif choice == "5":
            explore_recipes()
            explore_loyalty()
            explore_analytics()
            explore_ingredients()
        elif choice == "0":
            print("👋 Do widzenia!")
            return
        else:
            print("❌ Nieprawidłowy wybór")
            
    except KeyboardInterrupt:
        print("\n👋 Do widzenia!")
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    main() 