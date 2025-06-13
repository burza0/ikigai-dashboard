-- =====================================================
-- 🌱 IKIGAI - PRZEPROJEKTOWANIE BAZY DANYCH
-- Nowa struktura relacyjna z FK i migracja danych
-- =====================================================

-- BACKUP starych tabel
CREATE TABLE backup_ingredients AS SELECT * FROM ingredients;
CREATE TABLE backup_categories AS SELECT * FROM categories;
CREATE TABLE backup_recipes AS SELECT * FROM recipes;
CREATE TABLE backup_users AS SELECT * FROM users;

-- ============== NOWA STRUKTURA ==============

-- 1. KATEGORIE SKŁADNIKÓW
CREATE TABLE ingredient_categories (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(10),
    color VARCHAR(7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. SKŁADNIKI Z FOREIGN KEYS
CREATE TABLE ingredients_new (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES ingredient_categories(id),
    price DECIMAL(8,2) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    calories_per_100g INTEGER DEFAULT 0,
    protein_per_100g DECIMAL(5,2) DEFAULT 0,
    carbs_per_100g DECIMAL(5,2) DEFAULT 0,
    fat_per_100g DECIMAL(5,2) DEFAULT 0,
    fiber_per_100g DECIMAL(5,2) DEFAULT 0,
    description TEXT,
    origin VARCHAR(100),
    is_organic BOOLEAN DEFAULT false,
    is_available BOOLEAN DEFAULT true,
    benefits JSONB,
    allergens JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. KATEGORIE PRZEPISÓW
CREATE TABLE recipe_categories (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(10),
    color VARCHAR(7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. PRZEPISY Z FOREIGN KEYS
CREATE TABLE recipes_new (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES recipe_categories(id),
    description TEXT,
    long_description TEXT,
    calories INTEGER DEFAULT 0,
    protein DECIMAL(5,2) DEFAULT 0,
    carbs DECIMAL(5,2) DEFAULT 0,
    fat DECIMAL(5,2) DEFAULT 0,
    fiber DECIMAL(5,2) DEFAULT 0,
    sugar DECIMAL(5,2) DEFAULT 0,
    health_score INTEGER DEFAULT 0,
    prep_time INTEGER DEFAULT 0,
    price DECIMAL(8,2) DEFAULT 0,
    difficulty INTEGER DEFAULT 1,
    tags JSONB,
    instructions TEXT,
    tips TEXT,
    is_featured BOOLEAN DEFAULT false,
    is_available BOOLEAN DEFAULT true,
    popularity_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. SKŁADNIKI W PRZEPISACH (Many-to-Many)
CREATE TABLE recipe_ingredients_new (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER NOT NULL REFERENCES recipes_new(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients_new(id) ON DELETE CASCADE,
    amount DECIMAL(8,2) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    is_required BOOLEAN DEFAULT true,
    preparation_note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(recipe_id, ingredient_id)
);

-- 6. UŻYTKOWNICY Z FOREIGN KEYS
CREATE TABLE users_new (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'user',
    loyalty_level INTEGER DEFAULT 1,
    loyalty_points INTEGER DEFAULT 0,
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0,
    favorite_recipe_id INTEGER REFERENCES recipes_new(id),
    is_active BOOLEAN DEFAULT true,
    member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============== MIGRACJA DANYCH ==============

-- Kategorie składników
INSERT INTO ingredient_categories (slug, name, description, icon, color) VALUES
('adaptogens', 'Adaptogeny', 'Naturalne adaptogeny', '🍄', '#FD79A8'),
('proteins', 'Białka', 'Białka roślinne i zwierzęce', '🥜', '#A29BFE'),
('liquids', 'Płyny bazowe', 'Podstawy płynne do mieszanek', '🥛', '#74B9FF'),
('superfoods', 'Superfoods', 'Składniki o wysokiej wartości odżywczej', '⭐', '#6C5CE7'),
('vitamins', 'Witaminy', 'Witaminy i minerały', '💊', '#FDCB6E');

-- Kategorie przepisów (migracja ze starych categories)
INSERT INTO recipe_categories (slug, name, description, icon, color)
SELECT 
    id as slug,
    name,
    description,
    icon,
    color
FROM categories;

-- Migracja składników
INSERT INTO ingredients_new (
    slug, name, category_id, price, unit, calories_per_100g, 
    protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g,
    description, origin, is_organic, is_available, benefits, allergens
)
SELECT 
    i.id as slug,
    i.name,
    ic.id as category_id,
    COALESCE(i.price, 0),
    COALESCE(i.unit, 'g'),
    COALESCE(i.calories_per_100g, 0),
    COALESCE(i.protein_per_100g, 0),
    COALESCE(i.carbs_per_100g, 0),
    COALESCE(i.fat_per_100g, 0),
    COALESCE(i.fiber_per_100g, 0),
    i.description,
    i.origin,
    COALESCE(i.is_organic, false),
    COALESCE(i.is_available, true),
    CASE 
        WHEN i.benefits IS NOT NULL THEN i.benefits::jsonb
        ELSE '[]'::jsonb
    END,
    CASE 
        WHEN i.allergens IS NOT NULL THEN i.allergens::jsonb
        ELSE '[]'::jsonb
    END
FROM ingredients i
LEFT JOIN ingredient_categories ic ON i.category_id = ic.slug;

-- Migracja przepisów
INSERT INTO recipes_new (
    slug, name, category_id, description, long_description,
    calories, protein, carbs, fat, fiber, sugar, health_score,
    prep_time, price, difficulty, tags, instructions, tips,
    is_featured, is_available, popularity_score
)
SELECT 
    r.id as slug,
    r.name,
    rc.id as category_id,
    r.description,
    r.long_description,
    COALESCE(r.calories, 0),
    COALESCE(r.protein, 0),
    COALESCE(r.carbs, 0),
    COALESCE(r.fat, 0),
    COALESCE(r.fiber, 0),
    COALESCE(r.sugar, 0),
    COALESCE(r.health_score, 0),
    COALESCE(r.prep_time, 0),
    COALESCE(r.price, 0),
    COALESCE(r.difficulty, 1),
    CASE 
        WHEN r.tags IS NOT NULL THEN r.tags::jsonb
        ELSE '[]'::jsonb
    END,
    r.instructions,
    r.tips,
    COALESCE(r.is_featured, false),
    COALESCE(r.is_available, true),
    COALESCE(r.popularity_score, 0)
FROM recipes r
LEFT JOIN recipe_categories rc ON r.category_id = rc.slug;

-- Migracja recipe_ingredients
INSERT INTO recipe_ingredients_new (recipe_id, ingredient_id, amount, unit, is_required, preparation_note)
SELECT 
    rn.id as recipe_id,
    inn.id as ingredient_id,
    COALESCE(ri.amount, 1),
    COALESCE(ri.unit, 'g'),
    COALESCE(ri.is_required, true),
    ri.preparation_note
FROM recipe_ingredients ri
JOIN recipes_new rn ON ri.recipe_id = rn.slug
JOIN ingredients_new inn ON ri.ingredient_id = inn.slug;

-- Migracja użytkowników
INSERT INTO users_new (
    username, email, password_hash, phone, role,
    loyalty_level, loyalty_points, total_orders, total_spent,
    is_active, member_since, last_activity
)
SELECT 
    COALESCE(name, 'user_' || id) as username,
    COALESCE(email, 'user_' || id || '@example.com'),
    COALESCE(password_hash, 'temp_hash'),
    phone,
    COALESCE(role, 'user'),
    COALESCE(loyalty_level, 1),
    COALESCE(loyalty_points, 0),
    COALESCE(total_orders, 0),
    COALESCE(total_spent, 0),
    COALESCE(is_active, true),
    COALESCE(member_since, CURRENT_TIMESTAMP),
    COALESCE(last_activity, CURRENT_TIMESTAMP)
FROM users;

-- ============== INDEXES I TRIGGERY ==============

-- Indexes dla performance
CREATE INDEX idx_ingredients_category ON ingredients_new(category_id);
CREATE INDEX idx_ingredients_available ON ingredients_new(is_available);
CREATE INDEX idx_ingredients_slug ON ingredients_new(slug);
CREATE INDEX idx_recipes_category ON recipes_new(category_id);
CREATE INDEX idx_recipes_featured ON recipes_new(is_featured);
CREATE INDEX idx_recipes_slug ON recipes_new(slug);
CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients_new(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients_new(ingredient_id);
CREATE INDEX idx_users_email ON users_new(email);
CREATE INDEX idx_users_username ON users_new(username);

-- Trigger dla updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_ingredients_updated_at
    BEFORE UPDATE ON ingredients_new
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_recipes_updated_at
    BEFORE UPDATE ON recipes_new
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users_new
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============== ZAMIANA TABEL ==============

-- Usuń stare tabele i zmień nazwy nowych
DROP TABLE IF EXISTS recipe_ingredients CASCADE;
DROP TABLE IF EXISTS ingredients CASCADE;
DROP TABLE IF EXISTS recipes CASCADE;
DROP TABLE IF EXISTS users CASCADE;

ALTER TABLE ingredients_new RENAME TO ingredients;
ALTER TABLE recipes_new RENAME TO recipes;
ALTER TABLE recipe_ingredients_new RENAME TO recipe_ingredients;
ALTER TABLE users_new RENAME TO users;

-- ============== DODANIE PRZYKŁADOWYCH DANYCH ==============

-- 6 nowych baz dla różnych grup użytkowników
INSERT INTO ingredients (slug, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
('whey_protein_vanilla', 'Białko Serwatkowe Waniliowe', (SELECT id FROM ingredient_categories WHERE slug = 'proteins'), 7.50, 'ml', 102, 20, 4, 1, 0, 'Premium białko serwatkowe waniliowe', 'Nowa Zelandia', false, true, '["regeneracja", "budowa masy"]'::jsonb, '["mleko"]'::jsonb),
('oat_milk_barista', 'Mleko Owsiane Barista', (SELECT id FROM ingredient_categories WHERE slug = 'liquids'), 4.20, 'ml', 45, 1.2, 6.5, 1.5, 0.8, 'Kremowe mleko owsiane do kawy', 'Szwecja', true, true, '["wegańskie", "beta-glukan"]'::jsonb, '["owies"]'::jsonb),
('coconut_milk_full', 'Mleko Kokosowe Pełnotłuste', (SELECT id FROM ingredient_categories WHERE slug = 'liquids'), 5.80, 'ml', 180, 1.8, 2.8, 18.0, 0.5, 'Gęste mleko kokosowe z MCT', 'Tajlandia', true, true, '["ketogeniczne", "MCT"]'::jsonb, '["kokos"]'::jsonb),
('celery_juice_fresh', 'Sok z Selera Naciowego', (SELECT id FROM ingredient_categories WHERE slug = 'liquids'), 6.00, 'ml', 16, 0.7, 3.0, 0.2, 1.6, 'Świeży sok z selera - detoks', 'Polska', true, true, '["detox", "elektrolity"]'::jsonb, '["seler"]'::jsonb),
('kombucha_strawberry', 'Kombucha Truskawkowa', (SELECT id FROM ingredient_categories WHERE slug = 'liquids'), 8.50, 'ml', 25, 0.5, 5.5, 0.1, 0.3, 'Fermentowana kombucha z truskawkami', 'Polska', true, true, '["probiotyki", "witamina C"]'::jsonb, '[]'::jsonb),
('green_tea_matcha', 'Zielona Herbata Matcha', (SELECT id FROM ingredient_categories WHERE slug = 'liquids'), 9.20, 'ml', 35, 2.8, 5.5, 1.2, 1.0, 'Premium matcha ceremonialnej jakości', 'Japonia', true, true, '["L-teanina", "energia"]'::jsonb, '[]'::jsonb);

-- 20 nowych dodatków
INSERT INTO ingredients (slug, name, category_id, price, unit, calories_per_100g, protein_per_100g, carbs_per_100g, fat_per_100g, fiber_per_100g, description, origin, is_organic, is_available, benefits, allergens) VALUES 
-- SUPERFOODS (10)
('freeze_dried_strawberry', 'Liofilizowane Truskawki', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 4.50, 'g', 375, 7.4, 75.4, 4.4, 26.3, 'Chrupiące liofilizowane truskawki', 'Polska', true, true, '["witamina C", "antyoksydanty"]'::jsonb, '[]'::jsonb),
('mulberry_white', 'Morwa Biała Suszona', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 5.60, 'g', 344, 9.8, 69.7, 2.5, 14.0, 'Słodkie suszone owoce morwy', 'Turcja', true, true, '["resweratrol", "żelazo"]'::jsonb, '[]'::jsonb),
('black_currant_powder', 'Proszek z Czarnej Porzeczki', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 6.30, 'g', 325, 5.2, 71.8, 1.8, 17.4, 'Proszek z czarnej porzeczki', 'Nowa Zelandia', true, true, '["witamina C", "antocyjany"]'::jsonb, '[]'::jsonb),
('sea_buckthorn_berry', 'Rokitnik Pospolity', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 8.10, 'g', 82, 4.4, 7.8, 2.5, 10.6, 'Jagody rokitnika - omega-7', 'Rosja', true, true, '["omega-7", "witamina E"]'::jsonb, '[]'::jsonb),
('goji_berry_premium', 'Jagody Goji Premium', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 9.20, 'g', 349, 14.3, 77.1, 0.4, 13.0, 'Premium jagody goji z Tybetu', 'Tybet', true, true, '["zeaksantyna", "energia"]'::jsonb, '[]'::jsonb),
('macadamia_crushed', 'Makadamia Pokruszona', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 12.50, 'g', 718, 7.9, 13.8, 75.8, 8.6, 'Pokruszone orzechy makadamia', 'Australia', true, true, '["zdrowe tłuszcze", "magnez"]'::jsonb, '["orzechy"]'::jsonb),
('hemp_hearts', 'Łuskane Nasiona Konopi', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 8.90, 'g', 553, 31.6, 8.7, 48.8, 4.0, 'Nasiona konopi - kompletne białko', 'Kanada', true, true, '["omega-3", "białko"]'::jsonb, '[]'::jsonb),
('brazil_nuts_chopped', 'Orzechy Brazylijskie', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 15.40, 'g', 656, 14.3, 12.3, 66.4, 7.5, 'Pokrojone orzechy brazylijskie', 'Brazylia', true, true, '["selen", "witamina E"]'::jsonb, '["orzechy"]'::jsonb),
('coconut_flakes', 'Płatki Kokosowe', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 6.80, 'g', 660, 6.9, 23.7, 64.5, 16.3, 'Naturalne płatki kokosowe', 'Filipiny', true, true, '["MCT", "błonnik"]'::jsonb, '["kokos"]'::jsonb),
('cacao_nibs', 'Ziarna Kakao', (SELECT id FROM ingredient_categories WHERE slug = 'superfoods'), 11.20, 'g', 456, 20.4, 28.9, 43.1, 9.0, 'Surowe ziarna kakao', 'Ekwador', true, true, '["antyoksydanty", "magnez"]'::jsonb, '[]'::jsonb),

-- BIAŁKA (3)
('pea_protein_vanilla', 'Białko Grochowe Waniliowe', (SELECT id FROM ingredient_categories WHERE slug = 'proteins'), 6.80, 'g', 375, 80.0, 8.0, 2.5, 6.0, 'Izolat białka grochowego', 'Francja', true, true, '["wegańskie", "BCAA"]'::jsonb, '[]'::jsonb),
('hemp_protein_powder', 'Białko Konopne', (SELECT id FROM ingredient_categories WHERE slug = 'proteins'), 7.90, 'g', 338, 50.0, 12.0, 11.0, 18.0, 'Naturalne białko konopne', 'Kanada', true, true, '["omega-3", "błonnik"]'::jsonb, '[]'::jsonb),
('collagen_marine', 'Kolagen Morski', (SELECT id FROM ingredient_categories WHERE slug = 'proteins'), 18.50, 'g', 335, 90.0, 0.0, 0.5, 0.0, 'Hydrolizowany kolagen z ryb', 'Norwegia', false, true, '["skóra", "stawy"]'::jsonb, '["ryby"]'::jsonb),

-- ADAPTOGENY (4)
('ashwagandha_powder', 'Ashwagandha w Proszku', (SELECT id FROM ingredient_categories WHERE slug = 'adaptogens'), 13.50, 'g', 245, 4.0, 49.9, 0.3, 32.3, 'Organiczna ashwagandha', 'Indie', true, true, '["redukcja stresu", "energia"]'::jsonb, '[]'::jsonb),
('reishi_mushroom_powder', 'Grzyb Reishi', (SELECT id FROM ingredient_categories WHERE slug = 'adaptogens'), 16.80, 'g', 103, 7.3, 75.4, 1.8, 26.2, 'Suszony grzyb reishi', 'Chiny', true, true, '["immunitet", "sen"]'::jsonb, '[]'::jsonb),
('maca_root_powder', 'Korzeń Maca', (SELECT id FROM ingredient_categories WHERE slug = 'adaptogens'), 9.40, 'g', 325, 10.2, 71.4, 2.2, 8.5, 'Żółty korzeń maca z Andów', 'Peru', true, true, '["energia", "hormony"]'::jsonb, '[]'::jsonb),
('rhodiola_extract', 'Różeniec Górski', (SELECT id FROM ingredient_categories WHERE slug = 'adaptogens'), 18.90, 'g', 56, 1.8, 13.6, 0.1, 2.8, 'Ekstrakt różeńca górskiego', 'Syberya', true, true, '["koncentracja", "stres"]'::jsonb, '[]'::jsonb),

-- WITAMINY (3)
('vitamin_c_powder', 'Witamina C w Proszku', (SELECT id FROM ingredient_categories WHERE slug = 'vitamins'), 15.20, 'g', 0, 0.0, 0.0, 0.0, 0.0, 'Naturalna witamina C z aceroli', 'Brazylia', true, true, '["immunitet", "kolagen"]'::jsonb, '[]'::jsonb),
('b_complex_blend', 'Kompleks Witamin B', (SELECT id FROM ingredient_categories WHERE slug = 'vitamins'), 18.50, 'g', 0, 0.0, 0.0, 0.0, 0.0, 'Naturalny kompleks witamin B', 'USA', true, true, '["energia", "system nerwowy"]'::jsonb, '[]'::jsonb),
('omega3_algae', 'Omega-3 z Alg', (SELECT id FROM ingredient_categories WHERE slug = 'vitamins'), 25.80, 'ml', 900, 0.0, 0.0, 100.0, 0.0, 'Wegańskie omega-3 z mikroalg', 'Holandia', true, true, '["EPA", "DHA", "wegańskie"]'::jsonb, '[]'::jsonb);

-- ============== RAPORT KOŃCOWY ==============
SELECT 'PRZEPROJEKTOWANIE BAZY ZAKOŃCZONE POMYŚLNIE!' as message;
SELECT 'Kategorie składników: ' || COUNT(*) FROM ingredient_categories;
SELECT 'Składniki: ' || COUNT(*) FROM ingredients;
SELECT 'Kategorie przepisów: ' || COUNT(*) FROM recipe_categories;
SELECT 'Przepisy: ' || COUNT(*) FROM recipes;
SELECT 'Recipe ingredients: ' || COUNT(*) FROM recipe_ingredients;
SELECT 'Użytkownicy: ' || COUNT(*) FROM users;
SELECT 'Foreign keys: ' || COUNT(*) FROM pg_constraint WHERE contype = 'f'; 