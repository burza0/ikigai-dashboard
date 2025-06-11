# 🌱 IKIGAI Dashboard v2.1.0

**Zdrowe automaty vendingowe z systemem QR i kompletnym workflow zamówień**

## 📱 Opis Projektu

IKIGAI Dashboard to kompletny system zarządzania zdrowymi automatami vendingowymi, zbudowany w oparciu o japońską filozofię **IKIGAI** (生き甲斐) - "powód istnienia". Aplikacja łączy zdrowe odżywianie z nowoczesną technologią, oferując:

- 🥣 **Kreator Mieszanek** - komponowanie personalizowanych mieszanek
- 🗺️ **Mapę Automatów** - 5 lokalizacji z interaktywną mapą i nawigacją
- 🏆 **Program Lojalnościowy** - punkty, wyzwania, nagrody, poziomy
- 📱 **Mobile QR App** - zarządzanie kodami QR, skanowanie, płatności mobilne

## 🚀 Główne Funkcje v2.1.0

### 1. 🥣 Kreator Mieszanek IKIGAI
- **3-krokowy kreator**: Baza → Dodatki → Nazwa
- **4 bazy**: Jogurt Grecki, Granola BIO, Owsianka OATLY, Smoothie Bowl
- **6 dodatków**: Mix Jagód, Migdały, Nasiona Chia, Banan, Kokos, Miód
- **Real-time podgląd**: wartości odżywcze, cena, etykiety dietetyczne
- **Top 5 rekomendacji** z punktacją popularności i zdrowia
- **Persystentne zapisywanie** w localStorage
- **Automatyczne generowanie QR kodów** do zamówień

### 2. 🗺️ Mapa Automatów Vendingowych
- **5 lokalizacji**: IKIGAI Central, Fitness, Office, University, Park
- **Interaktywne markery** z nazwami automatów i statusem online/offline
- **Pełnoekranowa mapa** z poziomym układem
- **Filtry**: status, stan magazynu, przycisk "Znajdź mnie"
- **Geolokalizacja użytkownika** z kalkulacją odległości
- **Pozioma lista automatów** pod mapą z przewijaniem
- **Real-time status** i informacje o stocku produktów

### 3. 🏆 Program Lojalnościowy
- **4 poziomy awansu**: 🌱 Początkujący → 🌿 Entuzjasta → 🏆 Mistrz → 👑 Legenda
- **5 wyzwań tygodniowych**: Zdrowy Tydzień, Vegan Warrior, Protein Power, Early Bird, Mix Master
- **Sklep nagród**: darmowe dodatki, mieszanki, podwójne punkty, ekskluzywne składniki
- **System punktów**: zdobywanie za zamówienia, wymiana na nagrody
- **Animowane progress bary** i powiadomienia o awansach

### 4. 📱 Mobile QR App - NOWE w v2.1.0!
- **🎫 Moje QR** - zarządzanie wygenerowanymi kodami QR z zamówieniami
- **Podgląd kodów QR** z nazwami, cenami i statusami (aktywny/użyty/wygasły)
- **Akcje na kodach**: pełnoekranowy podgląd, udostępnianie, usuwanie
- **QR Scanner**: symulowana kamera + ręczny input kodów
- **3 metody płatności**: BLIK, NFC/Contactless, Karta płatnicza
- **Payment Simulator**: kompletny workflow płatności mobilnych
- **Push Notifications**: real-time o statusie zamówień i promocjach
- **Order Tracking**: live progress (0-100%), szybkie zamówienia
- **Zarządzanie**: masowe usuwanie wygasłych kodów, eksport historii
- **Auto-usuwanie** z togglem on/off

## 🔄 Complete User Journey v2.1.0

1. **🥣 Komponowanie** mieszanki w Kreatorze
2. **💾 Zapisywanie** trwale w localStorage
3. **🎯 Zamówienie** → automatycznie tworzy Order + QR kod
4. **🎫 Zarządzanie** kodami QR w zakładce "Moje QR"
5. **📱 Skanowanie** QR w Mobile App lub udostępnianie
6. **💳 Płatność** mobilna (BLIK/NFC/Card)
7. **🏪 Przygotowanie** w jednym z 5 automatów
8. **🔔 Notifications** o gotowym zamówieniu
9. **🏆 Punkty lojalnościowe** za zakup
10. **🗑️ Zarządzanie** używanymi i wygasłymi kodami

## 🗺️ Nowe Lokalizacje Automatów

### IKIGAI Central
- **Lokalizacja**: Centrum Handlowe - Poziom 1
- **Adres**: ul. Główna 123, Warszawa
- **Status**: Online ✅
- **Speciality**: Najpopularniejsze mieszanki

### IKIGAI Fitness  
- **Lokalizacja**: Siłownia FitZone
- **Adres**: ul. Sportowa 45, Warszawa
- **Status**: Online ✅
- **Speciality**: Protein shakes i energy bowls

### IKIGAI Office
- **Lokalizacja**: Business Center Plaza
- **Adres**: ul. Biznesowa 87, Warszawa  
- **Status**: Serwis 🔧
- **Speciality**: Healthy lunch options

### IKIGAI University - NOWY!
- **Lokalizacja**: Uniwersytet Warszawski (Biblioteka)
- **Adres**: ul. Krakowskie Przedmieście 26/28, Warszawa
- **Status**: Online ✅
- **Speciality**: Student-friendly prices

### IKIGAI Park - NOWY!
- **Lokalizacja**: Park Łazienkowski (Wejście główne)
- **Adres**: ul. Agrykoli 1, Warszawa
- **Status**: Online ✅  
- **Speciality**: Fresh fruit smoothies

## 🏗️ Architektura Techniczna

### Frontend
- **Vue 3 + TypeScript** - nowoczesny framework z type safety
- **Vite** - lightning fast build tool
- **Tailwind CSS** - utility-first styling z gradientami i animacjami
- **Composition API** - reactive programming
- **Axios** - HTTP client do komunikacji z API
- **QRCode.js** - generowanie kodów QR

### Backend
- **Python Flask** - REST API server
- **Modularna architektura** - oddzielne blueprinty dla każdej funkcji
- **In-memory storage** - demo data + localStorage persistence
- **CORS enabled** - cross-origin requests
- **QR Code generation** - Python qrcode library

### API Endpoints
```bash
# Składniki i mieszanki
GET  /api/ingredients/bases
GET  /api/ingredients/toppings  
GET  /api/recommendations
POST /api/mix/create

# Zamówienia i QR workflow
GET  /api/orders
POST /api/orders
POST /api/orders/{id}/generate-qr
POST /api/orders/scan-qr
GET  /api/orders/{id}/status

# Automaty vendingowe
GET  /api/vending-machines
GET  /api/products

# Program lojalnościowy
GET  /api/loyalty/profile/{user_id}
GET  /api/loyalty/challenges/{user_id}
GET  /api/loyalty/rewards
POST /api/loyalty/points/add
POST /api/loyalty/redeem

# System info
GET  /api/version
```

## 🎨 Design & UX

- **Mobile-first responsive design**
- **Dark mode support** z toggle
- **Purple/orange gradient theme** zgodny z IKIGAI
- **Smooth animations** i transitions
- **Japanese typography** z kanji 生 (życie)
- **Accessibility focus** z ARIA labels
- **Progressive enhancement**

## 📊 Funkcje Demo v2.1.0

### 🎯 Testowanie QR Workflow
1. Utwórz mieszankę w Kreatorze
2. Kliknij "🎯 Zamów" → automatycznie generuje QR kod
3. Przejdź do Mobile QR App → zakładka "🎫 Moje QR"
4. Zarządzaj swoimi kodami QR (podgląd, udostępnianie, usuwanie)
5. Przejdź do zakładki "📱 Skaner" 
6. Zeskanuj kod (lub wpisz ręcznie)
7. Symuluj płatność mobilną
8. Śledź postęp zamówienia w real-time

### 🗺️ Mapa 5 Automatów
1. Przejdź do sekcji "🗺️ Mapa Automatów"
2. Przetestuj filtry (Status, Stan magazynu)
3. Kliknij "Znajdź mnie" dla geolokalizacji
4. Eksploruj 5 lokalizacji: Central, Fitness, Office, University, Park
5. Przewijaj poziomą listę automatów pod mapą
6. Kliknij markery na mapie dla szczegółów

### 🏆 Program Lojalnościowy
1. Użyj "Symuluj zamówienie" w Loyalty Program
2. Obserwuj przyznawanie punktów (15 pkt za 15zł)
3. Awansuj poziomy (50 → 150 → 400 → 1000 pkt)
4. Wymieniaj punkty na nagrody w sklepie

### 📱 Mobile QR Management - NOWE!
- **🎫 Moje QR** - zarządzaj wszystkimi kodami QR
- **Bulk actions** - usuń wszystkie wygasłe kody jednym klikiem
- **Export history** - pobierz historię zamówień  
- **Auto-delete toggle** - automatyczne czyszczenie
- **Push notifications** przy każdej akcji
- **Payment simulator** z 3 metodami płatności

## 🚀 Instalacja i Uruchomienie

### 1. Klonowanie repozytorium
```bash
git clone https://github.com/twoj-username/ikigai-dashboard.git
cd ikigai-dashboard
```

### 2. Frontend (Vue.js)
```bash
npm install
npm run dev
# Dostępne na http://localhost:5174
```

### 3. Backend (Python Flask)
```bash
cd backend
python3 start_server.py
# API dostępne na http://localhost:5001
```

### 4. Demo aplikacji
- **Dashboard**: http://localhost:5174
- **Mobile QR App**: http://localhost:5174 → kliknij kafelek "Mobile QR App"
- **API docs**: http://localhost:5001/api/version

### 5. Deployment na Heroku
```bash
# Build frontend
npm run build

# Deploy do Heroku
git add .
git commit -m "Release v2.1.0 - Enhanced Mobile QR & 5 Vending Locations"
git push heroku main

# Aplikacja dostępna na: https://ikigai-dashboard-dd738ec5fa6f.herokuapp.com/
```

## 🌟 Zaawansowane Funkcje

- **LocalStorage persistence** - zapisane mieszanki nie znikają
- **Cross-component communication** między modułami
- **Real-time API integration** z backend services
- **Animated UI components** z Vue transitions
- **TypeScript type safety** w całym fronendzie
- **Mobile PWA ready** z service workers support

## 🔮 Plany Rozbudowy Systemu

### 🥣 Kreator Mieszanek IKIGAI - Przyszłe Funkcje

#### 🤖 Inteligentne Rekomendacje
- **AI-powered suggestions** na podstawie historii zamówień
- **Machine Learning algorithms** do przewidywania preferencji
- **Seasonal recommendations** z sezonowymi składnikami
- **Collaborative filtering** - "Użytkownicy podobni do Ciebie lubią..."

#### 🧬 Zaawansowana Analiza Składników  
- **Pełne bazy składników odżywczych** z APIs (USDA, OpenFoodFacts)
- **Real-time kalkulator kalorii** i makroskładników
- **Mikroelementy tracking** (witaminy, minerały, antyoksydanty)
- **Allergen detection** z alertami dla użytkowników

#### 🎯 Personalizacja Dietetyczna
- **Specialized diet modes**: Keto, Vegan, Paleo, Mediterranean, DASH
- **Medical dietary restrictions** import z systemów zdrowotnych
- **Caloric goals tracking** z daily/weekly targets
- **Nutritionist-approved recipes** z certyfikacją specjalistów

#### 🌐 Social & Sharing Features
- **Recipe sharing** w mediach społecznościowych
- **Community ratings** i reviews mieszanek
- **User-generated content** - własne przepisy społeczności
- **Collaboration tools** dla tworzenia wspólnych mieszanek

### 🗺️ Mapa Automatów - Smart Infrastructure

#### 🔌 IoT Integration
- **Real-time inventory sensors** w automatach
- **Temperature monitoring** produktów
- **Predictive maintenance** alerts dla serwisu
- **Energy consumption optimization** z smart grid

#### 📱 Advanced User Experience
- **AR View Mode** - nakładka rozszerzonej rzeczywistości
- **Product reservation system** z 15-minutowym pick-up window
- **Multi-stop routing** - optymalna trasa do kilku automatów
- **Voice navigation** z asystentem głosowym

#### 🚌 Transport Integration
- **Public transport APIs** (timetables, delays)
- **Walking/cycling routes** z real-time traffic
- **Parking availability** near vending locations
- **Accessibility features** dla użytkowników z niepełnosprawnościami

#### 👥 Community Features
- **Crowdsourced reporting** o statusie automatów
- **User check-ins** z social rewards
- **Location reviews** i zdjęcia
- **Emergency contact** dla problemów technicznych

### 🏆 Program Lojalnościowy - Gamifikacja 2.0

#### 🎮 Advanced Gamification
- **Achievement system** z 50+ różnymi badges
- **Weekly/monthly competitions** między użytkownikami
- **Seasonal events** z limitowanymi nagrodami
- **Progress visualization** z interactive charts

#### 👥 Social Loyalty Features
- **Friends & family circles** z shared challenges
- **Referral program** - punkty za zaproszenia
- **Team challenges** dla firm i grup
- **Leaderboards** z weekly/monthly rankings

#### 🎁 Premium Rewards Ecosystem
- **VIP tiers** z exclusive benefits (early access, special discounts)
- **Brand partnerships** - nagrody od partnerów (odzież sportowa, suplementy)
- **Experience rewards** - warsztaty kulinarne, konsultacje dietetyczne
- **Charity donations** - wymiana punktów na dobroczynność

#### 📊 Personalized Analytics
- **Health impact tracking** - jak wybory żywieniowe wpływają na samopoczucie
- **Spending insights** z recommended budget optimization
- **Habit formation tracking** z behavioral psychology
- **Milestone celebrations** z personalized messages

### 📱 Mobile QR App - Next-Gen Experience

#### 🗣️ Voice & AI Interface
- **Voice ordering** z Natural Language Processing
- **Smart assistant** do recommendations i help
- **Multilingual support** (Polski, Angielski, Niemiecki, Ukraiński)
- **Conversation memory** - context-aware interactions

#### 🔐 Advanced Security & Payments
- **Biometric authentication** (FaceID, TouchID, fingerprint)
- **Multi-factor authentication** dla high-value transactions
- **Cryptocurrency payments** (Bitcoin, Ethereum)
- **Digital wallet integration** (Apple Pay, Google Pay, Samsung Pay)

#### 🌐 Offline & Sync Capabilities
- **Offline mode** z full functionality bez internetu
- **Smart synchronization** kiedy wraca łączność
- **Cached content** dla faster loading
- **Background updates** z intelligent scheduling

#### 🔔 Smart Notifications System
- **Machine learning predictions** dla optimal notification timing
- **Location-based alerts** kiedy jesteś blisko automatów
- **Behavioral pattern recognition** - personalized reminders
- **Silent hours** z user-defined Do Not Disturb periods

### 🏥 Integracja z Systemami Zdrowotnymi

#### 📱 Fitness Apps Integration
- **Apple HealthKit** - synchronizacja activity i health data
- **Google Fit** - calories burned, steps, workouts
- **Fitbit API** - heart rate, sleep patterns, exercise tracking
- **Strava Integration** - dla sportowców i biegaczy
- **MyFitnessPal** - comprehensive food diary sync
- **Samsung Health** - complete ecosystem integration

#### 🩺 Medical Systems Integration
- **Electronic Health Records (EHR)** import dietary restrictions
- **Telemedicine platforms** - shared nutrition data z lekarzami
- **Pharmacy systems** - drug-food interaction warnings
- **Hospital nutrition departments** - meal planning dla pacjentów
- **Insurance providers** - wellness program integration
- **Clinical research platforms** - anonymized data dla badań

#### 👨‍⚕️ Professional Healthcare Tools
- **Nutritionist dashboard** - monitoring clients' progress
- **Dietitian prescription system** - recommended meal plans
- **Doctor portal** - patient nutrition insights
- **Therapy integration** - eating disorder support tools
- **Medical alert system** - emergency dietary needs

#### 📊 Health Analytics & Insights
- **Biomarker correlation** - jak żywienie wpływa na parametry krwi
- **Mental health tracking** - mood vs nutrition patterns
- **Sleep quality correlation** z dietary choices
- **Energy levels monitoring** throughout the day
- **Chronic disease management** (diabetes, hypertension, cholesterol)
- **Preventive health scoring** z long-term predictions

#### 🔬 Research & Development Features
- **Anonymized data collection** dla nutrition research
- **Clinical trial participation** opportunities
- **Personalized nutrition algorithms** based on genetic data
- **Microbiome analysis integration** dla gut health
- **Continuous glucose monitoring** sync
- **Wearable devices ecosystem** (smartwatches, rings, patches)

## 🎯 Philosophy IKIGAI

Aplikacja implementuje japońską koncepcję IKIGAI poprzez 4 filary:
- 🎯 **Co kochasz** - personalizowane mieszanki
- 💪 **W czym jesteś dobry** - rekomendacje AI
- 🌍 **Czego potrzebuje świat** - zdrowe odżywianie
- 💰 **Za co otrzymasz wynagrodzenie** - program lojalnościowy

**"Healthy choices made easy"** - to nasza misja! 🌱

---

**Zbudowane z ❤️ i filozofią IKIGAI dla zdrowego stylu życia**
