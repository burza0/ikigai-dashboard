-- =====================================================
-- 🌱 IKIGAI - Kompletne składniki PostgreSQL
-- 6 nowych baz + 20 nowych dodatków 
-- =====================================================

-- ============== 6 NOWYCH BAZ ==============

-- 1. FITNESS - Białko serwatkowe waniliowe
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('whey_protein_vanilla', 'Białko Serwatkowe Waniliowe', 'proteins', 7.50, 'ml', 102, 20, 4, 1, 0, 'Premium białko serwatkowe waniliowe', 'Nowa Zelandia', false, true, '["regeneracja", "budowa masy"]', '["mleko"]');

-- 2. WEGANIE - Mleko owsiane barista 
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('oat_milk_barista', 'Mleko Owsiane Barista', 'plant_milks', 4.20, 'ml', 45, 1.2, 6.5, 1.5, 0.8, 'Kremowe mleko owsiane do kawy', 'Szwecja', true, true, '["wegańskie", "beta-glukan"]', '["owies"]');

-- 3. KETO - Mleko kokosowe pełnotłuste
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('coconut_milk_full', 'Mleko Kokosowe Pełnotłuste', 'plant_milks', 5.80, 'ml', 180, 1.8, 2.8, 18.0, 0.5, 'Gęste mleko kokosowe z MCT', 'Tajlandia', true, true, '["ketogeniczne", "MCT"]', '["kokos"]');

-- 4. DETOX - Sok z selera naciowego
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('celery_juice_fresh', 'Sok z Selera Naciowego', 'vegetable_juices', 6.00, 'ml', 16, 0.7, 3.0, 0.2, 1.6, 'Świeży sok z selera - detoks', 'Polska', true, true, '["detox", "elektrolity"]', '["seler"]');

-- 5. PROBIOTYKI - Kombucha truskawkowa
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('kombucha_strawberry', 'Kombucha Truskawkowa', 'fermented', 8.50, 'ml', 25, 0.5, 5.5, 0.1, 0.3, 'Fermentowana kombucha z truskawkami', 'Polska', true, true, '["probiotyki", "witamina C"]', '[]');

-- 6. ENERGY - Matcha latte premium
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('matcha_latte_premium', 'Matcha Latte Premium', 'tea_blends', 12.00, 'ml', 65, 2.8, 8.5, 2.2, 1.0, 'Ceremonialna matcha z mlekiem kokosowym', 'Japonia', true, true, '["L-teanina", "energia"]', '[]');

-- ============== 20 NOWYCH DODATKÓW ==============

-- SUPERFOODS (5 składników)
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('freeze_dried_strawberry', 'Liofilizowane Truskawki', 'superfoods', 4.50, 'g', 375, 7.4, 75.4, 4.4, 26.3, 'Chrupiące liofilizowane truskawki', 'Polska', true, true, '["witamina C", "antyoksydanty"]', '[]'),
('mulberry_white', 'Morwa Biała Suszona', 'superfoods', 5.60, 'g', 344, 9.8, 69.7, 2.5, 14.0, 'Słodkie suszone owoce morwy', 'Turcja', true, true, '["resweratrol", "żelazo"]', '[]'),
('black_currant_powder', 'Proszek z Czarnej Porzeczki', 'superfoods', 6.30, 'g', 325, 5.2, 71.8, 1.8, 17.4, 'Proszek z czarnej porzeczki', 'Nowa Zelandia', true, true, '["witamina C", "antocyjany"]', '[]'),
('sea_buckthorn_berry', 'Rokitnik Pospolity', 'superfoods', 8.10, 'g', 82, 4.4, 7.8, 2.5, 10.6, 'Jagody rokitnika - omega-7', 'Rosja', true, true, '["omega-7", "witamina E"]', '[]'),
('goji_berry_premium', 'Jagody Goji Premium', 'superfoods', 9.20, 'g', 349, 14.3, 77.1, 0.4, 13.0, 'Premium jagody goji z Tybetu', 'Tybet', true, true, '["zeaksantyna", "energia"]', '[]');

-- ORZECHY I NASIONA (5 składników)
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('macadamia_crushed', 'Makadamia Pokruszona', 'nuts_seeds', 12.50, 'g', 718, 7.9, 13.8, 75.8, 8.6, 'Pokruszone orzechy makadamia', 'Australia', true, true, '["zdrowe tłuszcze", "magnez"]', '["orzechy"]'),
('hemp_hearts', 'Łuskane Nasiona Konopi', 'nuts_seeds', 8.90, 'g', 553, 31.6, 8.7, 48.8, 4.0, 'Nasiona konopi - kompletne białko', 'Kanada', true, true, '["omega-3", "białko"]', '[]'),
('brazil_nuts_chopped', 'Orzechy Brazylijskie', 'nuts_seeds', 15.40, 'g', 656, 14.3, 12.3, 66.4, 7.5, 'Pokrojone orzechy brazylijskie', 'Brazylia', true, true, '["selen", "witamina E"]', '["orzechy"]'),
('pumpkin_seeds_roasted', 'Pestki Dyni Prażone', 'nuts_seeds', 4.80, 'g', 559, 30.2, 10.7, 49.1, 6.0, 'Prażone pestki dyni', 'Austria', true, true, '["cynk", "magnez"]', '[]'),
('sunflower_seeds_hulled', 'Nasiona Słonecznika', 'nuts_seeds', 3.20, 'g', 584, 20.8, 20.0, 51.5, 8.6, 'Łuskane nasiona słonecznika', 'Ukraina', true, true, '["witamina E", "selen"]', '[]');

-- BIAŁKA ROŚLINNE (3 składniki)
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('pea_protein_vanilla', 'Białko Grochowe Waniliowe', 'proteins', 6.80, 'g', 375, 80.0, 8.0, 2.5, 6.0, 'Izolat białka grochowego', 'Francja', true, true, '["wegańskie", "BCAA"]', '[]'),
('hemp_protein_powder', 'Białko Konopne', 'proteins', 7.90, 'g', 338, 50.0, 12.0, 11.0, 18.0, 'Naturalne białko konopne', 'Kanada', true, true, '["omega-3", "błonnik"]', '[]'),
('spirulina_powder', 'Spirulina w Proszku', 'proteins', 11.20, 'g', 290, 57.5, 23.9, 7.7, 3.6, 'Organiczna spirulina', 'Hawaje', true, true, '["B12", "chlorofil"]', '[]');

-- ADAPTOGENY (4 składniki)
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('ashwagandha_powder', 'Ashwagandha w Proszku', 'adaptogens', 13.50, 'g', 245, 4.0, 49.9, 0.3, 32.3, 'Organiczna ashwagandha', 'Indie', true, true, '["redukcja stresu", "energia"]', '[]'),
('reishi_mushroom_powder', 'Grzyb Reishi', 'adaptogens', 16.80, 'g', 103, 7.3, 75.4, 1.8, 26.2, 'Suszony grzyb reishi', 'Chiny', true, true, '["immunitet", "sen"]', '[]'),
('maca_root_powder', 'Korzeń Maca', 'adaptogens', 9.40, 'g', 325, 10.2, 71.4, 2.2, 8.5, 'Żółty korzeń maca z Andów', 'Peru', true, true, '["energia", "hormony"]', '[]'),
('rhodiola_extract', 'Różeniec Górski', 'adaptogens', 18.90, 'g', 56, 1.8, 13.6, 0.1, 2.8, 'Ekstrakt różeńca górskiego', 'Syberya', true, true, '["koncentracja", "stres"]', '[]');

-- SŁODZIKI (3 składniki)
INSERT INTO ingredients (id, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('coconut_nectar', 'Nektar Kokosowy', 'sweeteners', 8.70, 'ml', 302, 1.2, 75.8, 0.2, 0.0, 'Nektar z kwiatów palmy', 'Filipiny', true, true, '["niski IG", "prebiotyki"]', '[]'),
('monk_fruit_sweetener', 'Owoc Mnicha', 'sweeteners', 22.50, 'g', 0, 0.0, 0.0, 0.0, 0.0, 'Słodzik bez kalorii', 'Chiny', true, true, '["zero kalorii", "naturalny"]', '[]'),
('yacon_syrup', 'Syrop z Yakonu', 'sweeteners', 14.30, 'ml', 267, 0.4, 69.2, 0.1, 0.5, 'Prebiotyczny słodzik', 'Peru', true, true, '["prebiotyki", "niski IG"]', '[]');

-- Sprawdzenie wyników
SELECT 'Dodano 6 nowych baz i 20 nowych składników do IKIGAI!' as message; 