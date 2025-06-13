-- =====================================================
-- 🌱 IKIGAI - Nowe składniki do bazy PostgreSQL
-- 6 nowych baz + 20 nowych dodatków
-- =====================================================

-- ============== NOWE BAZY (6 sztuk) ==============
-- Różne bazy dla różnych grup użytkowników

-- 1. FITNESS/SPORT - Białko serwatkowe
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES (
    'whey_protein_vanilla', 'Białko Serwatkowe Waniliowe', 'proteins', 7.50, 'ml', 
    102, 20, 4, 1, 0, 'Premium białko serwatkowe o smaku waniliowym - idealne po treningu',
    'Nowa Zelandia', false, true, 
    '["regeneracja mięśni", "budowa masy", "szybka absorpcja", "aminokwasy BCAA"]',
    '["mleko", "soja"]'
);

-- 2. DETOX/ZDROWIE - Sok z selera
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES (
    'celery_juice_fresh', 'Sok z Selera Świeży', 'liquids', 4.20, 'ml', 
    16, 0.7, 3, 0.2, 1.6, 'Świeżo wyciskany sok z selera naciowego - naturalny detoks',
    'Polska BIO', true, true, 
    '["detoksykacja", "nawodnienie", "potas", "witamina K", "przeciwzapalne"]',
    '[]'
);

-- 3. WEGANIE/WEGETARIANIE - Mleko owsiane
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES (
    'oat_milk_premium', 'Mleko Owsiane Premium', 'liquids', 3.80, 'ml', 
    47, 1.0, 6.6, 1.5, 0.8, 'Kremowe mleko owsiane bez dodatków - 100% roślinne',
    'Szwecja', true, true, 
    '["roślinne", "beż laktozy", "beta-glukan", "błonnik", "zrównoważone"]',
    '["owies", "gluten"]'
);

-- 4. SENIORZY - Kolagen + Jogurt
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES (
    'collagen_yogurt', 'Jogurt z Kolagenem', 'proteins', 5.90, 'ml', 
    89, 12, 8, 2.5, 0, 'Naturalny jogurt wzbogacony kolagenem morskim - dla zdrowych stawów',
    'Grecja', false, true, 
    '["zdrowe stawy", "elastyczność skóry", "wapń", "probiotyki", "kolagen"]',
    '["mleko", "ryby"]'
);

-- 5. MŁODZI/STUDENCI - Energetyczny shake czekoladowy
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES (
    'chocolate_energy_base', 'Czekoladowa Baza Energetyczna', 'liquids', 4.70, 'ml', 
    95, 8, 12, 3, 2, 'Czekoladowa baza z kofeiną z guarany - naturalna energia na cały dzień',
    'Brazylia', true, true, 
    '["energia", "koncentracja", "kakao", "guarana", "magnez", "żelazo"]',
    '["kakao", "może zawierać orzechy"]'
);

-- 6. DIETA/ODCHUDZANIE - Niskokaloryczny shake zielony
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES (
    'green_slim_base', 'Zielona Baza Slim', 'liquids', 3.90, 'ml', 
    28, 4, 3, 0.5, 2.5, 'Niskokaloryczna baza z zielonych warzyw i algami - wspiera odchudzanie',
    'Holandia BIO', true, true, 
    '["odchudzanie", "detoks", "chlorofil", "błonnik", "metabolizm", "antyoksydanty"]',
    '[]'
);

-- ============== NOWE DODATKI (20 sztuk) ==============
-- Różnorodne dodatki dla wszystkich grup

-- SUPERFOODS (5 dodatków)
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES 
('acai_powder', 'Proszek Acai', 'superfoods', 8.90, 'g', 534, 8.1, 52.2, 32.5, 44.2, 'Liofilizowany proszek z jagód acai - król antyoksydantów', 'Brazylia', true, true, '["antyoksydanty", "antocyjany", "energia", "witamina C"]', '[]'),

('maca_root_powder', 'Korzeń Maca w Proszku', 'superfoods', 6.70, 'g', 325, 10.2, 71.4, 1.2, 8.5, 'Peruwiański korzeń maca - naturalny adaptogen', 'Peru', true, true, '["energia", "libido", "hormony", "wytrzymałość", "adaptogen"]', '[]'),

('camu_camu_powder', 'Proszek Camu Camu', 'superfoods', 12.40, 'g', 473, 4.5, 94.4, 0.5, 24.3, 'Najwyższa naturalna zawartość witaminy C na świecie', 'Peru', true, true, '["witamina C", "odporność", "antyoksydanty", "żelazo"]', '[]'),

('baobab_powder', 'Proszek z Baobabu', 'superfoods', 7.20, 'g', 162, 2.3, 75.6, 0.4, 44.5, 'Proszek z owocu baobabu - bogaty w witaminę C i błonnik', 'Afryka', true, true, '["witamina C", "błonnik", "potas", "antyoksydanty", "probiotyki"]', '[]'),

('lucuma_powder', 'Proszek Lucuma', 'superfoods', 9.80, 'g', 329, 4.0, 75.7, 1.5, 23.3, 'Słodki proszek z owocu lucuma - naturalny słodzik', 'Peru', true, true, '["naturalny słodzik", "beta-karoten", "żelazo", "cynk"]', '[]');

-- OWOCE I BERRIES (4 dodatki)
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES 
('freeze_dried_strawberry', 'Liofilizowane Truskawki', 'superfoods', 4.50, 'g', 375, 7.4, 75.4, 4.4, 26.3, 'Chrupiące liofilizowane truskawki - intensywny smak', 'Polska', true, true, '["witamina C", "antocyjany", "błonnik", "folian"]', '[]'),

('mulberry_white', 'Morwa Biała Suszona', 'superfoods', 5.60, 'g', 344, 9.8, 69.7, 2.5, 14.0, 'Słodkie suszone owoce morwy białej - naturalne źródło resweratrolu', 'Turcja', true, true, '["resweratrol", "żelazo", "witamina C", "protein roślinny"]', '[]'),

('black_currant_powder', 'Proszek z Czarnej Porzeczki', 'superfoods', 6.30, 'g', 325, 5.2, 71.8, 1.8, 17.4, 'Skoncentrowany proszek z czarnej porzeczki', 'Nowa Zelandia', true, true, '["antocyjany", "witamina C", "rutyną", "odporność"]', '[]'),

('sea_buckthorn_berry', 'Rokitnik Pospolity', 'superfoods', 8.10, 'g', 82, 4.4, 7.8, 2.5, 10.6, 'Świeże jagody rokitnika - naturalne źródło omega-7', 'Rosja', true, true, '["omega-7", "witamina E", "karotenoidy", "skóra"]', '[]');

-- NASIONA I ORZECHY (4 dodatki)
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES 
('hemp_hearts_organic', 'Łuskane Nasiona Konopi', 'proteins', 7.90, 'g', 553, 31.6, 8.7, 48.8, 4.0, 'Łuskane nasiona konopi - kompletne białko roślinne', 'Kanada', true, true, '["białko kompletne", "omega-3", "omega-6", "magnez"]', '[]'),

('pumpkin_seeds_roasted', 'Prażone Pestki Dyni', 'proteins', 3.40, 'g', 559, 30.2, 10.7, 49.1, 6.0, 'Lekko prażone pestki dyni - bogate w cynk', 'Austria', true, true, '["cynk", "magnez", "żelazo", "prostatę"]', '[]'),

('brazil_nuts_organic', 'Orzechy Brazylijskie BIO', 'proteins', 12.50, 'g', 656, 14.3, 12.3, 66.4, 7.5, 'Organiczne orzechy brazylijskie - najlepsze źródło selenu', 'Brazylia', true, true, '["selen", "magnez", "tarczyca", "antyoksydanty"]', '["orzechy"]'),

('sunflower_seeds_raw', 'Surowe Nasiona Słonecznika', 'proteins', 2.80, 'g', 584, 20.8, 20.0, 51.5, 8.6, 'Surowe łuskane nasiona słonecznika', 'Ukraina BIO', true, true, '["witamina E", "magnez", "folian", "zdrowe tłuszcze"]', '[]');

-- PRZYPRAWY I ZIOŁA (4 dodatki)
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES 
('turmeric_golden', 'Kurkuma Złota Premium', 'adaptogens', 4.20, 'g', 354, 7.8, 64.9, 9.9, 21.1, 'Najwyższej jakości kurkuma z wysoką zawartością kurkuminy', 'Indie', true, true, '["kurkumina", "przeciwzapalne", "antyoksydanty", "wątroba"]', '[]'),

('ginger_fresh_powder', 'Proszek z Świeżego Imbiru', 'adaptogens', 3.90, 'g', 335, 8.8, 71.6, 4.2, 14.1, 'Suszony w niskiej temperaturze świeży imbir', 'Peru', true, true, '["gingerol", "trawienie", "nudności", "rozgrzanie"]', '[]'),

('cinnamon_ceylon', 'Cynamon Cejloński', 'adaptogens', 5.70, 'g', 247, 3.9, 80.6, 1.2, 53.1, 'Prawdziwy cynamon cejloński - najcenniejszy gatunek', 'Sri Lanka', true, true, '["cukier we krwi", "antyoksydanty", "metabolizm", "cynnamaldehyd"]', '[]'),

('cardamom_green', 'Kardamon Zielony', 'adaptogens', 15.60, 'g', 311, 10.8, 68.5, 6.7, 28.0, 'Zielony kardamon - król przypraw', 'Gwatemala', true, true, '["trawienie", "oddech", "antyoksydanty", "olejki eteryczne"]', '[]');

-- ADAPTOGENY I GRZYBY (3 dodatki)
INSERT INTO ingredients (
    id, name, category_id, price, unit, calories_per_100g, protein_per_100g, 
    carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, 
    is_organic, is_available, benefits, allergens
) VALUES 
('lions_mane_powder', 'Proszek Soplówka Jeżowata', 'adaptogens', 18.90, 'g', 345, 20.0, 45.0, 3.2, 15.0, 'Liofilizowany proszek z grzyba soplówki jeżowatej', 'Chiny', true, true, '["funkcje kognitywne", "pamięć", "neuroplastyczność", "NGF"]', '[]'),

('reishi_extract', 'Ekstrakt Reishi 10:1', 'adaptogens', 22.40, 'g', 265, 12.0, 28.0, 1.8, 18.0, 'Skoncentrowany ekstrakt z grzyba reishi - król grzybów', 'Japonia', true, true, '["odporność", "stres", "sen", "wątroba", "longevity"]', '[]'),

('rhodiola_rosea', 'Różeniec Górski Ekstrakt', 'adaptogens', 16.70, 'g', 289, 8.5, 42.0, 2.1, 12.0, 'Standardyzowany ekstrakt z różeńca górskiego - 3% rozawin', 'Syberia', true, true, '["stres", "energia", "wytrzymałość", "nastrój", "adaptogen"]', '[]');

-- =====================================================
-- 🎯 PODSUMOWANIE:
-- Dodano 6 nowych baz dla różnych grup użytkowników:
-- 1. Białko serwatkowe (fitness)
-- 2. Sok z selera (detox) 
-- 3. Mleko owsiane (weganie)
-- 4. Jogurt z kolagenem (seniorzy)
-- 5. Baza czekoladowa (młodzi)
-- 6. Baza zielona slim (dieta)
--
-- Dodano 20 nowych dodatków:
-- - 5 superfoods (acai, maca, camu camu, baobab, lucuma)
-- - 4 owoce (truskawki, morwa, porzeczka, rokitnik)
-- - 4 nasiona/orzechy (konopie, dynia, brazylijskie, słonecznik)
-- - 4 przyprawy (kurkuma, imbir, cynamon, kardamon)
-- - 3 adaptogeny (lion's mane, reishi, rhodiola)
-- ===================================================== 