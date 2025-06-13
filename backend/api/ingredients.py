"""
🥣 IKIGAI Ingredients Management
System składników i mieszanek - Kompozycja szczęścia
"""

from flask import Blueprint, request, jsonify
import uuid
import datetime
import time

ingredients_bp = Blueprint('ingredients', __name__)

# 🥄 BAZY - Fundament bowl
BASES = [
    # 🥛 BAZY TRADYCYJNE
    {
        "id": "yogurt_greek",
        "name": "Jogurt Grecki",
        "category": "base",
        "type": "traditional",
        "icon": "🥛",
        "price": 4.50,
        "description": "Kremowy jogurt grecki, wysokobiałkowy",
        "nutrition": {"protein": 15, "carbs": 6, "fat": 4, "kcal": 120},
        "dietary_labels": ["High-Protein", "Vegetarian", "Gluten-Free"],
        "safety_labels": ["Probiotyki", "Naturalny", "Bez konserwantów"],
        "origin": "Grecja"
    },
    {
        "id": "granola_bio",
        "name": "Granola BIO",
        "category": "base", 
        "type": "traditional",
        "icon": "🌾",
        "price": 3.80,
        "description": "Chrupiąca granola z płatków owsianych i orzechów",
        "nutrition": {"protein": 8, "carbs": 45, "fat": 12, "kcal": 280},
        "dietary_labels": ["Organic", "Vegan", "High-Fiber"],
        "safety_labels": ["BIO certyfikat", "Bez glutenu", "Naturalny"],
        "origin": "Polska"
    },
    {
        "id": "oatmeal_base",
        "name": "Owsianka OATLY",
        "category": "base",
        "type": "traditional",
        "icon": "🥣",
        "price": 2.90,
        "description": "Klasyczna owsianka na mleku owsianym OATLY",
        "nutrition": {"protein": 6, "carbs": 35, "fat": 3, "kcal": 180},
        "dietary_labels": ["Vegan", "Gluten-Free", "OATLY"],
        "safety_labels": ["Roślinny", "Bez laktozy", "Ekologiczny"],
        "origin": "Skandynavia"
    },
    {
        "id": "smoothie_bowl",
        "name": "Smoothie Bowl",
        "category": "base",
        "type": "traditional",
        "icon": "🍓",
        "price": 5.20,
        "description": "Kremowy smoothie bowl z owoców sezonowych",
        "nutrition": {"protein": 4, "carbs": 28, "fat": 2, "kcal": 140},
        "dietary_labels": ["Vegan", "Raw", "Antioxidant-Rich"],
        "safety_labels": ["Surowy", "Witaminy", "Naturalne cukry"],
        "origin": "Tropiki"
    },
    
    # 🥤 BAZY PŁYNNE W KUBECZKACH (BEZPIECZNE)
    {
        "id": "coconut_water",
        "name": "Woda Kokosowa Premium",
        "category": "base",
        "type": "liquid_cup",
        "icon": "🥥",
        "price": 4.20,
        "description": "Czysta woda kokosowa, naturalny elektrolit",
        "nutrition": {"protein": 1, "carbs": 9, "fat": 0, "kcal": 45},
        "dietary_labels": ["Vegan", "Natural-Electrolytes", "Hydrating"],
        "safety_labels": ["100% naturalna", "Sterylizowana", "Bez dodatków"],
        "origin": "Tajlandia"
    },
    {
        "id": "kombucha_ginger",
        "name": "Kombucha Imbirowa BIO",
        "category": "base", 
        "type": "liquid_cup",
        "icon": "🍃",
        "price": 6.50,
        "description": "Fermentowana kombucha z imbirem, probiotyki naturalne",
        "nutrition": {"protein": 0, "carbs": 4, "fat": 0, "kcal": 20},
        "dietary_labels": ["Vegan", "Probiotic", "Low-Sugar"],
        "safety_labels": ["Probiotyki żywe", "BIO fermentacja", "pH kontrolowany"],
        "origin": "Polska Manufaktura"
    },
    {
        "id": "matcha_premium",
        "name": "Matcha Premium w Kubeczku",
        "category": "base",
        "type": "liquid_cup", 
        "icon": "🍵",
        "price": 8.90,
        "description": "Ceremonialny matcha rozpuszczony w mleku kokosowym",
        "nutrition": {"protein": 2, "carbs": 6, "fat": 4, "kcal": 60},
        "dietary_labels": ["Vegan", "Antioxidant-Rich", "L-Theanine"],
        "safety_labels": ["Grade A matcha", "Pesticide-free", "Radiation tested"],
        "origin": "Uji, Japonia"
    },
    {
        "id": "golden_milk",
        "name": "Złote Mleko Kurkumowe",
        "category": "base",
        "type": "liquid_cup",
        "icon": "✨",
        "price": 5.80,
        "description": "Ayurvedyjskie złote mleko z kurkumą i przyprawami",
        "nutrition": {"protein": 3, "carbs": 8, "fat": 5, "kcal": 85},
        "dietary_labels": ["Vegan", "Anti-inflammatory", "Ayurvedic"],
        "safety_labels": ["Organiczna kurkuma", "Bez sztucznych barwników", "Tested purity"],
        "origin": "Indie - Ayurveda"
    },
    {
        "id": "lemon_ginger_water",
        "name": "Woda Cytrynowo-Imbirowa",
        "category": "base",
        "type": "liquid_cup",
        "icon": "🍋",
        "price": 3.20,
        "description": "Alkaliczna woda z cytryną i świeżym imbirem",
        "nutrition": {"protein": 0, "carbs": 2, "fat": 0, "kcal": 10},
        "dietary_labels": ["Vegan", "Alkaline", "Detox"],
        "safety_labels": ["pH 8.5", "Filtrowana woda", "Świeże składniki"],
        "origin": "Czyste Źródła"
    },
    {
        "id": "aloe_vera_juice",
        "name": "Sok z Aloesu Vera",
        "category": "base",
        "type": "liquid_cup", 
        "icon": "🌿",
        "price": 7.20,
        "description": "Czysty sok z aloesu vera, wsparcie trawienia",
        "nutrition": {"protein": 0, "carbs": 3, "fat": 0, "kcal": 15},
        "dietary_labels": ["Vegan", "Digestive-Support", "Raw"],
        "safety_labels": ["IASC certified", "Cold-pressed", "Filtrowany"],
        "origin": "Meksyk Organiczny"
    },
    
    # 🥄 BAZY DOSYPYWANE (PROSZKI BEZPIECZNE)
    {
        "id": "protein_vanilla",
        "name": "Proszek Proteinowy Wanilia",
        "category": "base",
        "type": "powder",
        "icon": "💪",
        "price": 6.90,
        "description": "Białko roślinne z groszku i ryżu, smak wanilia",
        "nutrition": {"protein": 25, "carbs": 3, "fat": 2, "kcal": 130},
        "dietary_labels": ["Vegan", "High-Protein", "Plant-Based"],
        "safety_labels": ["Heavy metals tested", "Organic", "3rd party verified"],
        "origin": "Europa BIO"
    },
    {
        "id": "collagen_marine",
        "name": "Kolagen Morski Peptidy",
        "category": "base",
        "type": "powder",
        "icon": "🐟",
        "price": 12.50,
        "description": "Kolagen morski z ryb głębinowych, typ I i III",
        "nutrition": {"protein": 18, "carbs": 0, "fat": 0, "kcal": 70},
        "dietary_labels": ["Pescatarian", "Collagen-Boost", "Anti-Aging"],
        "safety_labels": ["MSC certified", "Mercury tested", "Hydrolized"],
        "origin": "Nordyckie Morza"
    },
    {
        "id": "spirulina_powder",
        "name": "Spirulina Organiczna", 
        "category": "base",
        "type": "powder",
        "icon": "🌀",
        "price": 8.90,
        "description": "Spirulina platensis, superfood pełen białka",
        "nutrition": {"protein": 12, "carbs": 4, "fat": 2, "kcal": 80},
        "dietary_labels": ["Vegan", "Super-Food", "Iron-Rich"],
        "safety_labels": ["USDA Organic", "Radiation tested", "Pure culture"],
        "origin": "Hawaje Controlled"
    },
    {
        "id": "chlorella_powder",
        "name": "Chlorella Cracked Cell",
        "category": "base", 
        "type": "powder",
        "icon": "🟢",
        "price": 9.80,
        "description": "Chlorella vulgaris z łamaną ścianą komórkową",
        "nutrition": {"protein": 16, "carbs": 3, "fat": 3, "kcal": 95},
        "dietary_labels": ["Vegan", "Detox", "Chlorophyll-Rich"],
        "safety_labels": ["Cracked cell wall", "Pesticide-free", "CGF active"],
        "origin": "Japonia Controlled"
    },
    {
        "id": "barley_grass",
        "name": "Trawa Jęczmienna Young",
        "category": "base",
        "type": "powder",
        "icon": "🌱",
        "price": 7.40,
        "description": "Młoda trawa jęczmienna, alkaliczna i oczyszczająca",
        "nutrition": {"protein": 6, "carbs": 8, "fat": 1, "kcal": 60},
        "dietary_labels": ["Vegan", "Alkaline", "Enzyme-Rich"],
        "safety_labels": ["Young harvest", "Freeze-dried", "Enzyme active"],
        "origin": "Nowa Zelandia"
    }
]

# 🍓 DODATKI - Składniki szczęścia (ROZSZERZONE O BEZPIECZNE)
TOPPINGS = [
    # 🫐 DODATKI TRADYCYJNE
    {
        "id": "berries_mix",
        "name": "Mix Jagód",
        "category": "topping",
        "icon": "🫐",
        "price": 2.20,
        "description": "Borówki, maliny, jeżyny - bomba antyoksydantów",
        "nutrition": {"protein": 1, "carbs": 12, "fat": 0, "kcal": 50},
        "dietary_labels": ["Vegan", "Antioxidant-Rich", "Super-Food"],
        "safety_labels": ["Pesticide-free", "Flash frozen", "Naturalne"],
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
        "safety_labels": ["Aflatoxin tested", "Raw organic", "Naturally roasted"],
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
        "safety_labels": ["Organic", "Salmonella tested", "Pure origin"],
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
        "safety_labels": ["Residue-free", "Fresh daily", "Tropical certified"],
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
        "safety_labels": ["Sulfite-free", "Raw dehydrated", "Pure coconut"],
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
        "safety_labels": ["Raw unprocessed", "Antibiotic-free", "Single origin"],
        "origin": "Polskie Pasieki"
    },
    
    # 🌟 NOWE DODATKI BEZPIECZNE DLA ZDROWIA (20 SZTUK)
    {
        "id": "goji_berries",
        "name": "Jagody Goji Himalajskie",
        "category": "topping",
        "icon": "🔴",
        "price": 3.20,
        "description": "Himalajskie jagody goji, adaptogen i superfood",
        "nutrition": {"protein": 4, "carbs": 13, "fat": 1, "kcal": 70},
        "dietary_labels": ["Vegan", "Adaptogen", "Immune-Boost"],
        "safety_labels": ["Pesticide-free", "Traditional harvest", "Grade A"],
        "origin": "Tybet/Himalaje"
    },
    {
        "id": "mulberries_white",
        "name": "Morwa Biała Suszona",
        "category": "topping",
        "icon": "⚪",
        "price": 2.80,
        "description": "Suszone owoce morwy, naturalnie słodkie",
        "nutrition": {"protein": 3, "carbs": 14, "fat": 0, "kcal": 65},
        "dietary_labels": ["Vegan", "Natural-Sugar", "Iron-Rich"],
        "safety_labels": ["Sun-dried", "No sulfites", "Traditional method"],
        "origin": "Turcja Organiczna"
    },
    {
        "id": "cacao_nibs",
        "name": "Surowe Ziarna Kakao",
        "category": "topping",
        "icon": "🍫",
        "price": 2.50,
        "description": "Surowe nibs kakao, naturalne endorfiny",
        "nutrition": {"protein": 5, "carbs": 8, "fat": 12, "kcal": 150},
        "dietary_labels": ["Vegan", "Raw", "Mood-Boost"],
        "safety_labels": ["Fair trade", "Heavy metals tested", "Fermented properly"],
        "origin": "Peru Sacred Valley"
    },
    {
        "id": "sunflower_seeds",
        "name": "Nasiona Słonecznika",
        "category": "topping",
        "icon": "🌻",
        "price": 1.30,
        "description": "Łuskane nasiona słonecznika, witamina E",
        "nutrition": {"protein": 6, "carbs": 4, "fat": 14, "kcal": 160},
        "dietary_labels": ["Vegan", "Vitamin-E", "Heart-Healthy"],
        "safety_labels": ["Shell-free", "Aflatoxin tested", "Fresh harvest"],
        "origin": "Ukraina Organic"
    },
    {
        "id": "pumpkin_seeds",
        "name": "Pestki Dyni Styria",
        "category": "topping",
        "icon": "🎃",
        "price": 2.10,
        "description": "Pestki dyni bez łuski, źródło cynku i magnezu",
        "nutrition": {"protein": 7, "carbs": 3, "fat": 13, "kcal": 150},
        "dietary_labels": ["Vegan", "Zinc-Rich", "Prostate-Health"],
        "safety_labels": ["Shell-free", "Austrian grade", "Oil-rich"],
        "origin": "Austria Styria"
    },
    {
        "id": "flax_seeds",
        "name": "Siemię Lniane Złote",
        "category": "topping",
        "icon": "🌾",
        "price": 1.40,
        "description": "Złote siemię lniane, omega-3 roślinne",
        "nutrition": {"protein": 5, "carbs": 3, "fat": 11, "kcal": 130},
        "dietary_labels": ["Vegan", "Omega-3", "Fiber-Rich"],
        "safety_labels": ["Fresh ground", "Cold-stored", "Lignans active"],
        "origin": "Kanada Prairie"
    },
    {
        "id": "turmeric_powder",
        "name": "Kurkuma w Proszku BIO",
        "category": "topping",
        "icon": "🟡",
        "price": 1.80,
        "description": "Organiczna kurkuma, naturalny przeciwzapalny",
        "nutrition": {"protein": 1, "carbs": 2, "fat": 0, "kcal": 10},
        "dietary_labels": ["Vegan", "Anti-inflammatory", "Antioxidant"],
        "safety_labels": ["3% curcumin", "Lead tested", "Organic certified"],
        "origin": "Indie Kerala"
    },
    {
        "id": "cinnamon_ceylon",
        "name": "Cynamon Cejloński",
        "category": "topping",
        "icon": "🤎",
        "price": 2.20,
        "description": "Prawdziwy cynamon cejloński, reguluje cukier",
        "nutrition": {"protein": 0, "carbs": 1, "fat": 0, "kcal": 5},
        "dietary_labels": ["Vegan", "Blood-Sugar", "Warming"],
        "safety_labels": ["True Ceylon", "Low coumarin", "Bark grade A"],
        "origin": "Sri Lanka"
    },
    {
        "id": "ginger_dried",
        "name": "Imbir Suszony Kandyzowany",
        "category": "topping",
        "icon": "🫚",
        "price": 1.90,
        "description": "Naturalnie kandyzowany imbir, wsparcie trawienia",
        "nutrition": {"protein": 0, "carbs": 15, "fat": 0, "kcal": 60},
        "dietary_labels": ["Vegan", "Digestive", "Warming"],
        "safety_labels": ["No sulfur", "Naturally sweetened", "Gingerol active"],
        "origin": "Tajlandia"
    },
    {
        "id": "maca_powder",
        "name": "Maca Żółta Peruwiańska",
        "category": "topping",
        "icon": "🟨",
        "price": 3.50,
        "description": "Maca root powder, adaptogen energetyczny",
        "nutrition": {"protein": 4, "carbs": 12, "fat": 1, "kcal": 70},
        "dietary_labels": ["Vegan", "Adaptogen", "Energy-Boost"],
        "safety_labels": ["Gelatinized", "High altitude", "Pure maca"],
        "origin": "Peru Junin"
    },
    {
        "id": "acai_powder",
        "name": "Acai Berry Proszek",
        "category": "topping",
        "icon": "🟣",
        "price": 4.20,
        "description": "Freeze-dried acai, potężny antyoksydant",
        "nutrition": {"protein": 2, "carbs": 6, "fat": 5, "kcal": 70},
        "dietary_labels": ["Vegan", "Antioxidant-Rich", "Heart-Health"],
        "safety_labels": ["Freeze-dried", "ORAC tested", "Wild harvested"],
        "origin": "Brazylia Amazonia"
    },
    {
        "id": "lucuma_powder",
        "name": "Lucuma Proszek",
        "category": "topping",
        "icon": "🟠",
        "price": 3.80,
        "description": "Lucuma powder, naturalna słodycz i karotenoidy",
        "nutrition": {"protein": 2, "carbs": 11, "fat": 1, "kcal": 60},
        "dietary_labels": ["Vegan", "Natural-Sweetener", "Low-Glycemic"],
        "safety_labels": ["Raw powder", "No additives", "Ancient superfruit"],
        "origin": "Peru Wysokogórze"
    },
    {
        "id": "baobab_powder",
        "name": "Baobab Proszek Afrykański",
        "category": "topping",
        "icon": "🌳",
        "price": 4.50,
        "description": "Miąższ baobaba, witamina C i błonnik",
        "nutrition": {"protein": 2, "carbs": 16, "fat": 0, "kcal": 70},
        "dietary_labels": ["Vegan", "Vitamin-C", "Prebiotic"],
        "safety_labels": ["Wild harvested", "Naturally dried", "Sustainably sourced"],
        "origin": "Senegal Wildlands"
    },
    {
        "id": "moringa_powder",
        "name": "Moringa Oleifera Proszek",
        "category": "topping",
        "icon": "🌿",
        "price": 3.20,
        "description": "Liście moringa, kompletne amino i witaminy",
        "nutrition": {"protein": 6, "carbs": 8, "fat": 1, "kcal": 65},
        "dietary_labels": ["Vegan", "Complete-Amino", "Iron-Rich"],
        "safety_labels": ["Shade-dried", "Microbial tested", "Pure leaves"],
        "origin": "Indie Organiczne"
    },
    {
        "id": "ashwagandha_powder",
        "name": "Ashwagandha KSM-66",
        "category": "topping",
        "icon": "🧘",
        "price": 5.20,
        "description": "Ashwagandha extract, adaptogen na stres",
        "nutrition": {"protein": 1, "carbs": 2, "fat": 0, "kcal": 15},
        "dietary_labels": ["Vegan", "Adaptogen", "Stress-Relief"],
        "safety_labels": ["KSM-66 extract", "Withanolides 5%", "Clinical grade"],
        "origin": "Indie Rajasthan"
    },
    {
        "id": "mct_oil",
        "name": "Olej MCT Premium",
        "category": "topping",
        "icon": "🥥",
        "price": 2.80,
        "description": "Medium Chain Triglycerides, szybka energia",
        "nutrition": {"protein": 0, "carbs": 0, "fat": 14, "kcal": 130},
        "dietary_labels": ["Keto", "Brain-Fuel", "Quick-Energy"],
        "safety_labels": ["C8/C10 only", "Triple distilled", "Coconut source"],
        "origin": "Filipiny Refined"
    },
    {
        "id": "bee_pollen",
        "name": "Pyłek Pszczeli Wielokwiatowy",
        "category": "topping",
        "icon": "🐝",
        "price": 3.60,
        "description": "Naturalny pyłek pszczeli, kompletne odżywianie",
        "nutrition": {"protein": 5, "carbs": 8, "fat": 1, "kcal": 60},
        "dietary_labels": ["Vegetarian", "Complete-Nutrition", "Energy-Boost"],
        "safety_labels": ["Antibiotic-free", "Wild flowers", "Fresh harvest"],
        "origin": "Polskie Łąki"
    },
    {
        "id": "propolis_powder",
        "name": "Propolis w Proszku",
        "category": "topping",
        "icon": "🍯",
        "price": 6.20,
        "description": "Propolis pszczeli, naturalne antybiotyk",
        "nutrition": {"protein": 1, "carbs": 2, "fat": 0, "kcal": 15},
        "dietary_labels": ["Vegetarian", "Antibacterial", "Immune-Support"],
        "safety_labels": ["Alcohol-free extract", "Standardized", "Pure propolis"],
        "origin": "Brasília Highlands"
    },
    {
        "id": "chlorella_tablets",
        "name": "Chlorella w Tabletkach",
        "category": "topping",
        "icon": "💊",
        "price": 4.80,
        "description": "Chlorella w tabletkach, detoks ciężkich metali",
        "nutrition": {"protein": 8, "carbs": 2, "fat": 1, "kcal": 50},
        "dietary_labels": ["Vegan", "Detox", "Heavy-Metal-Cleanse"],
        "safety_labels": ["Cracked cell", "Tablet form", "Binding agents free"],
        "origin": "Tajwan Pure"
    },
    {
        "id": "activated_charcoal",
        "name": "Węgiel Aktywny Kokosowy",
        "category": "topping",
        "icon": "⚫",
        "price": 2.40,
        "description": "Węgiel aktywny spożywczy, naturalny detoks",
        "nutrition": {"protein": 0, "carbs": 0, "fat": 0, "kcal": 0},
        "dietary_labels": ["Vegan", "Detox", "Digestive-Cleanse"],
        "safety_labels": ["Food grade", "Steam activated", "Coconut source"],
        "origin": "Sri Lanka Coconut"
    }
]

# 🌟 TOP 5 REKOMENDACJI IKIGAI (ROZSZERZONE O NOWE SKŁADNIKI)
TOP_RECOMMENDATIONS = [
    {
        "id": "morning_detox_warrior",
        "name": "🌅 Morning Detox Warrior",
        "description": "Oczyszczający start dnia - złote mleko kurkumowe z superfoodami",
        "base": "golden_milk",
        "toppings": ["turmeric_powder", "goji_berries", "chia_seeds", "honey_raw"],
        "total_price": 13.70,
        "popularity": 98,
        "health_score": 96,
        "tags": ["Detoks", "Anti-inflammatory", "Superfoods", "Ayurvedic"]
    },
    {
        "id": "adaptogen_power_bowl",
        "name": "🧘 Adaptogen Power Bowl", 
        "description": "Wspierający stres - spirulina z ashwagandha i maca",
        "base": "spirulina_powder",
        "toppings": ["ashwagandha_powder", "maca_powder", "cacao_nibs", "coconut_flakes"],
        "total_price": 17.80,
        "popularity": 92,
        "health_score": 98,
        "tags": ["Adaptogeny", "Stres-Relief", "Energy-Boost", "Vegan"]
    },
    {
        "id": "tropical_antioxidant_blast",
        "name": "🏝️ Tropical Antioxidant Blast",
        "description": "Antyoksydantowa bomba - woda kokosowa z acai i baobab",
        "base": "coconut_water",
        "toppings": ["acai_powder", "baobab_powder", "mulberries_white", "bee_pollen"],
        "total_price": 16.30,
        "popularity": 89,
        "health_score": 94,
        "tags": ["Antioxidanty", "Tropical", "Immune-Boost", "Vitamin-C"]
    },
    {
        "id": "brain_fuel_matcha",
        "name": "🧠 Brain Fuel Matcha Supreme",
        "description": "Koncentracja i energia - ceremonialny matcha z MCT i orzechami",
        "base": "matcha_premium",
        "toppings": ["mct_oil", "nuts_almonds", "moringa_powder"],
        "total_price": 14.90,
        "popularity": 85,
        "health_score": 91,
        "tags": ["Brain-Fuel", "Focus", "L-Theanine", "Keto"]
    },
    {
        "id": "complete_wellness_kombucha",
        "name": "🌱 Complete Wellness Kombucha",
        "description": "Kompleksowe zdrowie - probiotyki z supergreens i adaptogens",
        "base": "kombucha_ginger",
        "toppings": ["chlorella_tablets", "flax_seeds", "propolis_powder", "turmeric_powder"],
        "total_price": 17.70,
        "popularity": 87,
        "health_score": 97,
        "tags": ["Probiotyki", "Detoks", "Complete-Wellness", "Anti-inflammatory"]
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
        'message': 'Top 5 najpopularniejszych bowls IKIGAI'
    })

@ingredients_bp.route('/mix', methods=['POST'])
def create_custom_mix():
    """🎨 Skomponuj własny bowl"""
    try:
        data = request.get_json()
        
        # Pobranie parametrów
        mix_name = data.get('name', 'Mój Bowl')
        selected_base = data.get('base')  # ID bazy
        selected_toppings = data.get('toppings', [])  # Lista ID dodatków
        
        if not selected_base:
            return jsonify({
                'success': False,
                'error': 'Musisz wybrać bazę dla swojego bowl'
            }), 400
        
        # Znajdź bazę
        base = None
        for base_item in BASES:
            if base_item['id'] == selected_base:
                base = base_item
                break
                
        if not base:
            return jsonify({
                'success': False,
                'error': 'Nie znaleziono wybranej bazy'
            }), 404
            
        # Stwórz bowl
        mix = {
            'id': f"custom_{int(time.time())}",
            'name': mix_name,
            'base': base,
            'toppings': [],
            'total_price': base['price'],
            'total_calories': base.get('calories', 0),
            'created_at': datetime.now().isoformat()
        }
        
        # Zapisz bowl
        CUSTOM_MIXES[mix['id']] = mix
        
        return jsonify({
            'success': True,
            'mix': mix,
            'message': f'Bowl "{mix_name}" został utworzony!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd tworzenia bowl: {str(e)}'
        }), 500

@ingredients_bp.route('/api/meal-recipes', methods=['GET'])
def get_meal_recipes():
    """🍽️ Pobierz gotowe przepisy na dania"""
    category = request.args.get('category')  # breakfast, lunch, dinner, snacks, specialty
    difficulty = request.args.get('difficulty')  # easy, medium, hard
    max_price = request.args.get('max_price', type=float)
    health_benefit = request.args.get('health_benefit')  # np. "Detox", "High-Protein"
    
    # Spłaszcz wszystkie przepisy do jednej listy
    all_recipes = []
    for category_name, recipes in MEAL_RECIPES.items():
        for recipe in recipes:
            recipe_copy = recipe.copy()
            recipe_copy['category'] = category_name
            all_recipes.append(recipe_copy)
    
    # Filtrowanie
    filtered_recipes = all_recipes
    
    if category:
        filtered_recipes = [r for r in filtered_recipes if r['category'] == category]
    
    if difficulty:
        filtered_recipes = [r for r in filtered_recipes if r['difficulty'] == difficulty]
        
    if max_price:
        filtered_recipes = [r for r in filtered_recipes if r['total_price'] <= max_price]
        
    if health_benefit:
        filtered_recipes = [r for r in filtered_recipes if health_benefit in r['health_benefits']]
    
    return jsonify({
        'success': True,
        'recipes': filtered_recipes,
        'count': len(filtered_recipes),
        'message': f'Znaleziono {len(filtered_recipes)} przepisów na dania',
        'available_filters': {
            'categories': list(MEAL_RECIPES.keys()),
            'difficulties': ['easy', 'medium', 'hard'],
            'health_benefits': list(set([benefit for recipe in all_recipes for benefit in recipe['health_benefits']]))
        }
    })

@ingredients_bp.route('/api/meal-recipes/categories', methods=['GET'])
def get_meal_categories():
    """📂 Pobierz kategorie przepisów z liczbą dań"""
    categories_stats = {}
    
    for category_name, recipes in MEAL_RECIPES.items():
        categories_stats[category_name] = {
            'name': category_name,
            'count': len(recipes),
            'price_range': {
                'min': min(r['total_price'] for r in recipes),
                'max': max(r['total_price'] for r in recipes)
            },
            'avg_health_score': round(sum(r['health_score'] for r in recipes) / len(recipes)),
            'popular_benefits': [benefit for recipe in recipes for benefit in recipe['health_benefits']][:5]
        }
    
    return jsonify({
        'success': True,
        'categories': categories_stats,
        'total_recipes': sum(len(recipes) for recipes in MEAL_RECIPES.values()),
        'message': 'Kategorie przepisów na dania'
    })

@ingredients_bp.route('/api/meal-recipes/<recipe_id>', methods=['GET'])
def get_meal_recipe_details(recipe_id):
    """🔍 Pobierz szczegóły konkretnego przepisu"""
    # Znajdź przepis we wszystkich kategoriach
    recipe = None
    for category_recipes in MEAL_RECIPES.values():
        recipe = next((r for r in category_recipes if r['id'] == recipe_id), None)
        if recipe:
            break
    
    if not recipe:
        return jsonify({
            'success': False,
            'error': f'Nie znaleziono przepisu o ID: {recipe_id}'
        }), 404
    
    # Pobierz szczegóły składników
    recipe_details = recipe.copy()
    
    # Znajdź bazę
    base_details = next((b for b in BASES if b['id'] == recipe['base']), None)
    if base_details:
        recipe_details['base_details'] = base_details
    
    # Znajdź dodatki  
    toppings_details = []
    for topping_id in recipe['toppings']:
        topping = next((t for t in TOPPINGS if t['id'] == topping_id), None)
        if topping:
            toppings_details.append(topping)
    recipe_details['toppings_details'] = toppings_details
    
    return jsonify({
        'success': True,
        'recipe': recipe_details,
        'message': f'Szczegóły przepisu: {recipe["name"]}'
    })

@ingredients_bp.route('/api/ingredients/categories', methods=['GET'])
def get_ingredient_categories():
    """📂 Pobierz składniki pogrupowane w kategorie"""
    
    # Kategoryzuj bazy
    bases_by_type = {
        'traditional': [b for b in BASES if b.get('type') == 'traditional'],
        'liquid_cup': [b for b in BASES if b.get('type') == 'liquid_cup'], 
        'powder': [b for b in BASES if b.get('type') == 'powder']
    }
    
    # Kategoryzuj dodatki (na podstawie origin i składników)
    superfoods = [t for t in TOPPINGS if any(keyword in t['name'].lower() for keyword in ['goji', 'acai', 'maca', 'spirulina', 'chlorella', 'moringa', 'ashwagandha', 'baobab'])]
    fruits_berries = [t for t in TOPPINGS if any(keyword in t['name'].lower() for keyword in ['jagod', 'morwa', 'banan', 'kokos'])]
    seeds_nuts = [t for t in TOPPINGS if any(keyword in t['name'].lower() for keyword in ['nasiona', 'pestki', 'migdał', 'siemię', 'chia'])]
    spices_herbs = [t for t in TOPPINGS if any(keyword in t['name'].lower() for keyword in ['kurkuma', 'cynamon', 'imbir', 'kakao'])]
    bee_products = [t for t in TOPPINGS if any(keyword in t['name'].lower() for keyword in ['miód', 'pyłek', 'propolis'])]
    detox_cleanse = [t for t in TOPPINGS if any(keyword in t['name'].lower() for keyword in ['węgiel', 'chlorella'])]
    
    return jsonify({
        'success': True,
        'categories': {
            'bases': {
                'traditional': {
                    'name': 'Bazy Tradycyjne',
                    'description': 'Klasyczne podstawy jak jogurt, granola, owsianka',
                    'items': bases_by_type['traditional'],
                    'count': len(bases_by_type['traditional'])
                },
                'liquid_cup': {
                    'name': 'Bazy Płynne w Kubeczkach',
                    'description': 'Gotowe napoje w kubeczkach - woda kokosowa, kombucha, matcha',
                    'items': bases_by_type['liquid_cup'],
                    'count': len(bases_by_type['liquid_cup'])
                },
                'powder': {
                    'name': 'Bazy Dosypywane',
                    'description': 'Proszki proteinowe, spirulina, chlorella, kolagen',
                    'items': bases_by_type['powder'],
                    'count': len(bases_by_type['powder'])
                }
            },
            'toppings': {
                'superfoods': {
                    'name': 'Superfoods & Adaptogeny',
                    'description': 'Goji, acai, maca, ashwagandha, moringa',
                    'items': superfoods,
                    'count': len(superfoods)
                },
                'fruits_berries': {
                    'name': 'Owoce & Jagody',
                    'description': 'Banany, morwa, jagody, kokos',
                    'items': fruits_berries,
                    'count': len(fruits_berries)
                },
                'seeds_nuts': {
                    'name': 'Nasiona & Orzechy',
                    'description': 'Chia, siemię lniane, migdały, pestki dyni',
                    'items': seeds_nuts,
                    'count': len(seeds_nuts)
                },
                'spices_herbs': {
                    'name': 'Przyprawy & Zioła',
                    'description': 'Kurkuma, cynamon, imbir, kakao nibs',
                    'items': spices_herbs,
                    'count': len(spices_herbs)
                },
                'bee_products': {
                    'name': 'Produkty Pszczele',
                    'description': 'Miód, pyłek pszczeli, propolis',
                    'items': bee_products,
                    'count': len(bee_products)
                },
                'detox_cleanse': {
                    'name': 'Detoks & Oczyszczanie',
                    'description': 'Węgiel aktywny, chlorella w tabletkach',
                    'items': detox_cleanse,
                    'count': len(detox_cleanse)
                }
            }
        },
        'total_ingredients': len(BASES) + len(TOPPINGS),
        'message': 'Składniki pogrupowane w kategorie'
    })

# 🍽️ GOTOWE PRZEPISY NA DANIA - PEŁNA BAZA (30 PRZEPISÓW)
MEAL_RECIPES = {
    "breakfast": [
        {
            "id": "energetic_morning_bowl",
            "name": "🌅 Energetyczny Start Dnia",
            "category": "breakfast",
            "description": "Pełnowartościowe śniadanie z proteinem i superfoods na całodzienną energię",
            "base": "protein_vanilla", 
            "toppings": ["goji_berries", "maca_powder", "nuts_almonds", "honey_raw", "cinnamon_ceylon"],
            "total_price": 16.60,
            "prep_time": "5 min",
            "nutrition": {"protein": 32, "carbs": 38, "fat": 20, "kcal": 415},
            "health_benefits": ["High-Protein", "Energy-Boost", "Adaptogen", "Natural-Sugar"],
            "best_for": ["Intensywny trening", "Długi dzień pracy", "Regeneracja"],
            "popularity": 94,
            "health_score": 96,
            "difficulty": "easy",
            "preparation": "Wymieszaj proszek proteinowy z wodą, dodaj maca powder, posyp goji, migdałami, polej miodem i posyp cynamonem."
        },
        {
            "id": "detox_morning_green", 
            "name": "🍃 Detox Green Morning",
            "category": "breakfast",
            "description": "Oczyszczające śniadanie z chlorellą, spiruliną i zielonymi superfoods",
            "base": "spirulina_powder",
            "toppings": ["chlorella_tablets", "barley_grass", "flax_seeds", "lemon_ginger_water"],
            "total_price": 21.00,
            "prep_time": "3 min", 
            "nutrition": {"protein": 24, "carbs": 18, "fat": 14, "kcal": 275},
            "health_benefits": ["Detox", "Chlorophyll-Rich", "Alkaline", "Heavy-Metal-Cleanse"],
            "best_for": ["Detoks organizmu", "Problemy trawienne", "Oczyszczanie"],
            "popularity": 78,
            "health_score": 98,
            "difficulty": "easy",
            "preparation": "Rozpuść spirulinę w wodzie, dodaj chlorellę, trawę jęczmienną, siemię lniane i zalej wodą cytrynowo-imbirową."
        },
        {
            "id": "tropical_breakfast_bowl",
            "name": "🏝️ Tropikalne Śniadanie", 
            "category": "breakfast",
            "description": "Egzotyczne śniadanie z kokosem, acai i owocami tropikalnymi",
            "base": "coconut_water",
            "toppings": ["acai_powder", "coconut_flakes", "lucuma_powder", "banana_sliced", "bee_pollen"],
            "total_price": 17.70,
            "prep_time": "4 min",
            "nutrition": {"protein": 6, "carbs": 42, "fat": 22, "kcal": 345},
            "health_benefits": ["Antioxidant-Rich", "Natural-Electrolytes", "Vitamin-C", "Tropical"],
            "best_for": ["Po treningu", "Upał", "Potrzeba witamin"],
            "popularity": 89,
            "health_score": 88,
            "difficulty": "easy", 
            "preparation": "Do wody kokosowej dodaj acai powder, wymieszaj, posyp płatkami kokosowymi, lucuma, plasterkami banana i pyłkiem."
        },
        {
            "id": "golden_morning_ritual",
            "name": "✨ Złoty Rytuał Poranny",
            "category": "breakfast", 
            "description": "Ayurvedyjskie śniadanie z kurkumą, ashwagandha i miodem na harmonię ciała",
            "base": "golden_milk",
            "toppings": ["ashwagandha_powder", "turmeric_powder", "honey_raw", "cinnamon_ceylon", "ginger_dried"],
            "total_price": 16.50,
            "prep_time": "5 min",
            "nutrition": {"protein": 5, "carbs": 27, "fat": 5, "kcal": 165},
            "health_benefits": ["Anti-inflammatory", "Adaptogen", "Stress-Relief", "Ayurvedic"],
            "best_for": ["Stres", "Stany zapalne", "Relaks", "Medytacja"],
            "popularity": 85,
            "health_score": 94,
            "difficulty": "easy",
            "preparation": "Podgrzej złote mleko, dodaj ashwagandha, kurkumę, miód, cynamon i kandyzowany imbir. Wymieszaj."
        },
        {
            "id": "brain_fuel_breakfast",
            "name": "🧠 Brain Fuel Breakfast", 
            "category": "breakfast",
            "description": "Śniadanie na koncentrację z matcha, MCT oil i nootropic foods",
            "base": "matcha_premium", 
            "toppings": ["mct_oil", "nuts_almonds", "moringa_powder", "flax_seeds"],
            "total_price": 16.60,
            "prep_time": "4 min",
            "nutrition": {"protein": 13, "carbs": 11, "fat": 39, "kcal": 425},
            "health_benefits": ["Brain-Fuel", "L-Theanine", "Omega-3", "Focus"],
            "best_for": ["Praca umysłowa", "Egzaminy", "Kreatywność"],
            "popularity": 91,
            "health_score": 92,
            "difficulty": "medium",
            "preparation": "Przygotuj matcha latte, dodaj MCT oil, wymieszaj z moringą, posyp migdałami i siemieniem lnianym."
        }
    ],
    
    "lunch": [
        {
            "id": "complete_wellness_lunch",
            "name": "🌱 Complete Wellness Bowl",
            "category": "lunch",
            "description": "Kompletny obiad z probiotykami, supergreens i adaptogens dla pełnego zdrowia",
            "base": "kombucha_ginger",
            "toppings": ["chlorella_powder", "propolis_powder", "pumpkin_seeds", "turmeric_powder", "sunflower_seeds"],
            "total_price": 18.40,
            "prep_time": "6 min",
            "nutrition": {"protein": 19, "carbs": 12, "fat": 30, "kcal": 370},
            "health_benefits": ["Probiotic", "Anti-inflammatory", "Immune-Support", "Complete-Nutrition"],
            "best_for": ["Choroby", "Słaba odporność", "Problemy jelitowe"],
            "popularity": 82,
            "health_score": 97,
            "difficulty": "medium",
            "preparation": "Kombucha + chlorella powder jako baza, posyp propolis, pestkami dyni, kurkumą i nasionami słonecznika."
        },
        {
            "id": "power_protein_lunch", 
            "name": "💪 Power Protein Bowl",
            "category": "lunch",
            "description": "Wysokobiałkowy obiad z kolagenem morskim i nasionami na budowę mięśni",
            "base": "collagen_marine",
            "toppings": ["nuts_almonds", "pumpkin_seeds", "chia_seeds", "hemp_hearts", "cacao_nibs"],
            "total_price": 20.30,
            "prep_time": "5 min", 
            "nutrition": {"protein": 38, "carbs": 16, "fat": 41, "kcal": 550},
            "health_benefits": ["High-Protein", "Collagen-Boost", "Anti-Aging", "Muscle-Building"],
            "best_for": ["Po treningu", "Sport", "Regeneracja mięśni"],
            "popularity": 88,
            "health_score": 91,
            "difficulty": "easy",
            "preparation": "Rozpuść kolagen w wodzie, dodaj migdały, pestki dyni, chia, konopie i ziarna kakao."
        },
        {
            "id": "alkaline_detox_lunch",
            "name": "🌿 Alkaline Detox Bowl", 
            "category": "lunch", 
            "description": "Alkaliczny obiad detoksykujący z aloe vera, chlorellą i zielonymi superfoods",
            "base": "aloe_vera_juice",
            "toppings": ["chlorella_tablets", "barley_grass", "moringa_powder", "activated_charcoal"],
            "total_price": 19.60,
            "prep_time": "4 min",
            "nutrition": {"protein": 14, "carbs": 17, "fat": 4, "kcal": 155},
            "health_benefits": ["Detox", "Alkaline", "Digestive-Support", "Heavy-Metal-Cleanse"],
            "best_for": ["Detoks", "Problemy żołądkowe", "Oczyszczanie organizmu"],
            "popularity": 75,
            "health_score": 95,
            "difficulty": "easy", 
            "preparation": "Sok aloe vera jako baza, dodaj chlorellę w tabletkach, trawę jęczmienną, moringę i węgiel aktywny."
        },
        {
            "id": "antioxidant_power_lunch",
            "name": "🟣 Antioxidant Power Bowl",
            "category": "lunch",
            "description": "Przeciwutleniająca bomba z acai, baobab, jagodami goji i antyoksydantami",
            "base": "yogurt_greek", 
            "toppings": ["acai_powder", "baobab_powder", "goji_berries", "mulberries_white", "cacao_nibs"],
            "total_price": 18.70,
            "prep_time": "4 min",
            "nutrition": {"protein": 23, "carbs": 57, "fat": 17, "kcal": 445},
            "health_benefits": ["Antioxidant-Rich", "Vitamin-C", "Heart-Health", "Anti-Aging"],
            "best_for": ["Starzenie się", "Choroby serca", "Ochrona komórek"],
            "popularity": 86,
            "health_score": 93,
            "difficulty": "easy",
            "preparation": "Jogurt grecki + acai powder, posyp baobab, goji, morwą białą i ziarnami kakao."
        },
        {
            "id": "stress_relief_lunch",
            "name": "🧘 Stress Relief Bowl",
            "category": "lunch", 
            "description": "Lunch przeciwstresowy z ashwagandha, maca i adaptogenami na spokój umysłu",
            "base": "oatmeal_base",
            "toppings": ["ashwagandha_powder", "maca_powder", "honey_raw", "cinnamon_ceylon", "nuts_almonds"],
            "total_price": 14.80,
            "prep_time": "5 min",
            "nutrition": {"protein": 16, "carbs": 54, "fat": 19, "kcal": 420},
            "health_benefits": ["Adaptogen", "Stress-Relief", "Calming", "Energy-Balance"],
            "best_for": ["Stres", "Przepracowanie", "Problemy ze snem"],
            "popularity": 79,
            "health_score": 89,
            "difficulty": "easy", 
            "preparation": "Owsianka + ashwagandha i maca powder, słodzenie miodem, cynamon, migdały na wierzch."
        }
    ],
    
    "dinner": [
        {
            "id": "regenerative_evening_bowl",
            "name": "🌙 Regeneracyjny Wieczór",
            "category": "dinner",
            "description": "Lekka kolacja regenerująca z kolagenem, adaptogens i uspokajającymi składnikami",
            "base": "golden_milk",
            "toppings": ["collagen_marine", "ashwagandha_powder", "honey_raw", "cinnamon_ceylon"],
            "total_price": 24.50,
            "prep_time": "6 min",
            "nutrition": {"protein": 21, "carbs": 25, "fat": 5, "kcal": 220},
            "health_benefits": ["Collagen-Boost", "Stress-Relief", "Anti-Aging", "Sleep-Support"],
            "best_for": ["Regeneracja", "Przed snem", "Anti-aging"],
            "popularity": 84,
            "health_score": 94,
            "difficulty": "medium",
            "preparation": "Złote mleko + kolagen morski, ashwagandha, miód i cynamon. Podgrzej i wymieszaj."
        },
        {
            "id": "digestive_harmony_dinner",
            "name": "🌿 Harmony Trawienia",
            "category": "dinner",
            "description": "Kolacja wspierająca trawienie z aloe vera, imbirem i probiotykami",
            "base": "aloe_vera_juice", 
            "toppings": ["ginger_dried", "propolis_powder", "turmeric_powder", "honey_raw"],
            "total_price": 17.10,
            "prep_time": "4 min",
            "nutrition": {"protein": 1, "carbs": 22, "fat": 0, "kcal": 95},
            "health_benefits": ["Digestive-Support", "Anti-inflammatory", "Antibacterial", "Soothing"],
            "best_for": ["Problemy żołądkowe", "Zaparcia", "Wzdęcia"],
            "popularity": 77,
            "health_score": 92,
            "difficulty": "easy",
            "preparation": "Sok aloe vera + kandyzowany imbir, propolis, kurkuma i miód. Delikatnie wymieszaj."
        },
        {
            "id": "calming_night_bowl",
            "name": "😴 Uspokajający Wieczór", 
            "category": "dinner",
            "description": "Kolacja relaksująca z adaptogens i składnikami uspokajającymi na dobry sen",
            "base": "lemon_ginger_water",
            "toppings": ["ashwagandha_powder", "honey_raw", "cinnamon_ceylon", "bee_pollen"],
            "total_price": 12.50,
            "prep_time": "3 min",
            "nutrition": {"protein": 6, "carbs": 27, "fat": 1, "kcal": 140},
            "health_benefits": ["Stress-Relief", "Sleep-Support", "Calming", "Adaptogen"],
            "best_for": ["Bezsenność", "Stres", "Relaks wieczorny"],
            "popularity": 81,
            "health_score": 88,
            "difficulty": "easy",
            "preparation": "Woda cytrynowo-imbirowa + ashwagandha, miód, cynamon i pyłek pszczeli."
        }
    ],
    
    "snacks": [
        {
            "id": "pre_workout_energy",
            "name": "⚡ Pre-Workout Energy",
            "category": "snack",
            "description": "Przekąska przed treningiem z maca, kofeiną z matcha i szybką energią",
            "base": "matcha_premium",
            "toppings": ["maca_powder", "mct_oil", "banana_sliced", "cacao_nibs"],
            "total_price": 16.60,
            "prep_time": "3 min",
            "nutrition": {"protein": 7, "carbs": 26, "fat": 22, "kcal": 310},
            "health_benefits": ["Energy-Boost", "Pre-Workout", "L-Theanine", "Quick-Energy"],
            "best_for": ["Przed treningiem", "Energia poranna", "Koncentracja"],
            "popularity": 92,
            "health_score": 87,
            "difficulty": "easy",
            "preparation": "Matcha latte + maca powder, MCT oil, plasterki banana i ziarna kakao."
        },
        {
            "id": "post_workout_recovery",
            "name": "💪 Post-Workout Recovery",
            "category": "snack", 
            "description": "Regeneracyjna przekąska po treningu z proteiną, kolagenem i elektrolitami",
            "base": "coconut_water",
            "toppings": ["protein_vanilla", "collagen_marine", "banana_sliced", "honey_raw"],
            "total_price": 24.80,
            "prep_time": "4 min",
            "nutrition": {"protein": 44, "carbs": 31, "fat": 2, "kcal": 320},
            "health_benefits": ["Post-Workout", "High-Protein", "Electrolytes", "Recovery"],
            "best_for": ["Po treningu", "Regeneracja mięśni", "Rehydratacja"],
            "popularity": 89,
            "health_score": 93,
            "difficulty": "easy",
            "preparation": "Woda kokosowa + proszek proteinowy, kolagen, banana i miód. Shake well."
        },
        {
            "id": "immunity_boost_snack", 
            "name": "🛡️ Immunity Boost",
            "category": "snack",
            "description": "Przekąska wzmacniająca odporność z propolis, pyłkiem pszczelim i witaminą C",
            "base": "lemon_ginger_water",
            "toppings": ["propolis_powder", "bee_pollen", "baobab_powder", "goji_berries"],
            "total_price": 17.50,
            "prep_time": "3 min", 
            "nutrition": {"protein": 8, "carbs": 33, "fat": 1, "kcal": 175},
            "health_benefits": ["Immune-Support", "Vitamin-C", "Antibacterial", "Antioxidant"],
            "best_for": ["Choroby", "Słaba odporność", "Jesień/zima"],
            "popularity": 85,
            "health_score": 95,
            "difficulty": "easy",
            "preparation": "Woda cytrynowo-imbirowa + propolis, pyłek pszczeli, baobab i jagody goji."
        },
        {
            "id": "brain_focus_snack",
            "name": "🧠 Brain Focus Snack", 
            "category": "snack",
            "description": "Przekąska na koncentrację z nootropics, omega-3 i brain-boosting foods",
            "base": "smoothie_bowl",
            "toppings": ["moringa_powder", "flax_seeds", "nuts_almonds", "cacao_nibs"],
            "total_price": 13.30,
            "prep_time": "4 min",
            "nutrition": {"protein": 16, "carbs": 35, "fat": 28, "kcal": 420},
            "health_benefits": ["Brain-Fuel", "Omega-3", "Focus", "Memory-Support"],
            "best_for": ["Praca umysłowa", "Nauka", "Koncentracja"],
            "popularity": 83,
            "health_score": 90,
            "difficulty": "easy",
            "preparation": "Smoothie bowl + moringa powder, siemię lniane, migdały i ziarna kakao."
        },
        {
            "id": "detox_cleanse_snack",
            "name": "🌿 Detox Cleanse",
            "category": "snack",
            "description": "Oczyszczająca przekąska z węglem aktywnym, chlorellą i detox superfoods", 
            "base": "coconut_water",
            "toppings": ["activated_charcoal", "chlorella_tablets", "lemon_ginger_water"],
            "total_price": 11.40,
            "prep_time": "2 min",
            "nutrition": {"protein": 9, "carbs": 14, "fat": 1, "kcal": 100},
            "health_benefits": ["Detox", "Heavy-Metal-Cleanse", "Digestive-Cleanse", "Alkaline"],
            "best_for": ["Detoks", "Toksyny", "Oczyszczanie jelit"],
            "popularity": 72,
            "health_score": 94,
            "difficulty": "easy",
            "preparation": "Woda kokosowa + węgiel aktywny, chlorella w tabletkach. Mix carefully."
        }
    ],
    
    "specialty": [
        {
            "id": "longevity_elixir",
            "name": "🧬 Longevity Elixir",
            "category": "specialty",
            "description": "Eliksir długowieczności z najlepszymi anti-aging superfoods i adaptogenami",
            "base": "kombucha_ginger", 
            "toppings": ["collagen_marine", "ashwagandha_powder", "goji_berries", "propolis_powder", "turmeric_powder"],
            "total_price": 26.90,
            "prep_time": "8 min",
            "nutrition": {"protein": 24, "carbs": 23, "fat": 0, "kcal": 190},
            "health_benefits": ["Anti-Aging", "Longevity", "Adaptogen", "Collagen-Boost", "Immunity"],
            "best_for": ["Dojrzały wiek", "Prewencja", "Regeneracja komórek"],
            "popularity": 88,
            "health_score": 99,
            "difficulty": "medium",
            "preparation": "Kombucha + kolagen morski, ashwagandha, goji, propolis i kurkuma. Premium blend."
        },
        {
            "id": "athletic_performance", 
            "name": "🏃 Athletic Performance",
            "category": "specialty",
            "description": "Formuła dla atletów z kompletnymi aminokwasami, elektrolitami i endurance boost",
            "base": "coconut_water",
            "toppings": ["spirulina_powder", "maca_powder", "bee_pollen", "mct_oil", "cacao_nibs"],
            "total_price": 22.10,
            "prep_time": "5 min",
            "nutrition": {"protein": 18, "carbs": 25, "fat": 18, "kcal": 320},
            "health_benefits": ["Athletic-Performance", "Endurance", "Electrolytes", "Complete-Amino"],
            "best_for": ["Sport wyczynowy", "Maraton", "Wydolność"],
            "popularity": 91,
            "health_score": 96, 
            "difficulty": "medium",
            "preparation": "Woda kokosowa + spirulina, maca, pyłek pszczeli, MCT oil i kakao nibs."
        },
        {
            "id": "hormonal_balance",
            "name": "⚖️ Hormonal Balance",
            "category": "specialty", 
            "description": "Formuła balansująca hormony z adaptogens, maca i składnikami regulującymi",
            "base": "aloe_vera_juice",
            "toppings": ["ashwagandha_powder", "maca_powder", "flax_seeds", "pumpkin_seeds"],
            "total_price": 19.30,
            "prep_time": "6 min",
            "nutrition": {"protein": 16, "carbs": 19, "fat": 25, "kcal": 345},
            "health_benefits": ["Hormonal-Balance", "Adaptogen", "Women-Health", "Reproductive-Health"],
            "best_for": ["PCOS", "Menopauza", "Problemy hormonalne"],
            "popularity": 79,
            "health_score": 92,
            "difficulty": "medium",
            "preparation": "Sok aloe vera + ashwagandha, maca, siemię lniane i pestki dyni. Blend thoroughly."
        },
        {
            "id": "cognitive_enhancement",
            "name": "🎯 Cognitive Enhancement", 
            "category": "specialty",
            "description": "Enhancement kognitywny z nootropics, DHA i brain-optimizing compounds",
            "base": "matcha_premium",
            "toppings": ["moringa_powder", "mct_oil", "flax_seeds", "cacao_nibs", "ginger_dried"],
            "total_price": 19.20,
            "prep_time": "7 min",
            "nutrition": {"protein": 9, "carbs": 18, "fat": 25, "kcal": 320},
            "health_benefits": ["Cognitive-Enhancement", "Brain-Fuel", "Memory-Boost", "Focus"],
            "best_for": ["Praca analityczna", "Studia", "Kreatywność"],
            "popularity": 86,
            "health_score": 94,
            "difficulty": "hard",
            "preparation": "Matcha premium + moringa, MCT oil, siemię lniane, kakao nibs i imbir. Precise preparation."
        },
        {
            "id": "ultimate_detox",
            "name": "🌪️ Ultimate Detox", 
            "category": "specialty",
            "description": "Najsilniejszy detoks z activated charcoal, chlorellą i heavy-metal cleansing",
            "base": "lemon_ginger_water",
            "toppings": ["activated_charcoal", "chlorella_powder", "barley_grass", "spirulina_powder"],
            "total_price": 17.90,
            "prep_time": "5 min",
            "nutrition": {"protein": 20, "carbs": 17, "fat": 3, "kcal": 175},
            "health_benefits": ["Ultimate-Detox", "Heavy-Metal-Cleanse", "Liver-Support", "Deep-Cleansing"],
            "best_for": ["Intensywny detoks", "Zatrucia", "Reset organizmu"],
            "popularity": 74,
            "health_score": 97,
            "difficulty": "hard",
            "preparation": "Woda cytrynowo-imbirowa + węgiel aktywny, chlorella, trawa jęczmienna, spirulina. Advanced detox."
        }
    ]
}
