# 🌱 IKIGAI Dashboard

**Zdrowe automaty vendingowe z systemem QR i kompletnym workflow zamówień**

## 📱 Opis Projektu

IKIGAI Dashboard to kompletny system zarządzania zdrowymi automatami vendingowymi, zbudowany w oparciu o japońską filozofię **IKIGAI** (生き甲斐) - "powód istnienia". Aplikacja łączy zdrowe odżywianie z nowoczesną technologią, oferując:

- 🥣 **Kreator Mieszanek** - komponowanie personalizowanych mieszanek
- 🗺️ **Mapę Automatów** - lokalizacja z geolokalizacją i nawigacją
- 🏆 **Program Lojalnościowy** - punkty, wyzwania, nagrody, poziomy
- 📱 **Mobile QR App** - skanowanie, płatności mobilne, push notifications

## 🚀 Główne Funkcje

### 1. 🥣 Kreator Mieszanek IKIGAI
- **3-krokowy kreator**: Baza → Dodatki → Nazwa
- **4 bazy**: Jogurt Grecki, Granola BIO, Owsianka OATLY, Smoothie Bowl
- **6 dodatków**: Mix Jagód, Migdały, Nasiona Chia, Banan, Kokos, Miód
- **Real-time podgląd**: wartości odżywcze, cena, etykiety dietetyczne
- **Top 5 rekomendacji** z punktacją popularności i zdrowia
- **Persystentne zapisywanie** w localStorage
- **Generowanie QR kodów** do zamówień

### 2. 🗺️ Mapa Automatów Vendingowych
- **3 lokalizacje**: IKIGAI Central, Fitness, Office
- **Geolokalizacja użytkownika** z kalkulacją odległości
- **Filtry**: według statusu (online/offline) i stanu magazynu
- **Google Maps integracja** dla nawigacji
- **Real-time status** i informacje o stocku
- **Responsive layout** z tooltips

### 3. 🏆 Program Lojalnościowy
- **4 poziomy awansu**: 🌱 Początkujący → 🌿 Entuzjasta → 🏆 Mistrz → 👑 Legenda
- **5 wyzwań tygodniowych**: Zdrowy Tydzień, Vegan Warrior, Protein Power, Early Bird, Mix Master
- **Sklep nagród**: darmowe dodatki, mieszanki, podwójne punkty, ekskluzywne składniki
- **System punktów**: zdobywanie za zamówienia, wymiana na nagrody
- **Animowane progress bary** i powiadomienia o awansach

### 4. 📱 Mobile QR App
- **QR Scanner**: symulowana kamera + ręczny input
- **3 metody płatności**: BLIK, NFC/Contactless, Karta płatnicza
- **Payment Simulator**: kompletny workflow płatności mobilnych
- **Push Notifications**: real-time o statusie zamówień i promocjach
- **Order Tracking**: live progress (0-100%), szybkie zamówienia
- **Historia transakcji** i skanów

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

## 🔄 Complete User Journey

1. **🥣 Komponowanie** mieszanki w Kreatorze
2. **💾 Zapisywanie** trwale w localStorage
3. **🎯 Zamówienie** → tworzy Order + QR kod (base64 PNG)
4. **📱 Skanowanie** QR w Mobile App
5. **💳 Płatność** mobilna (BLIK/NFC/Card)
6. **🏪 Przygotowanie** w automacie vendingowym
7. **🔔 Notifications** o gotowym zamówieniu
8. **🏆 Punkty lojalnościowe** za zakup

## 🎨 Design & UX

- **Mobile-first responsive design**
- **Dark mode support** z toggle
- **Purple/orange gradient theme** zgodny z IKIGAI
- **Smooth animations** i transitions
- **Japanese typography** z kanji 生 (życie)
- **Accessibility focus** z ARIA labels
- **Progressive enhancement**

## 🚀 Instalacja i Uruchomienie

### 1. Klonowanie repozytorium
```bash
git clone https://github.com/burza0/ikigai-dashboard.git
cd ikigai-dashboard
```

### 2. Frontend (Vue.js)
```bash
npm install
npm run dev
# Dostępne na http://localhost:5173
```

### 3. Backend (Python Flask)
```bash
cd backend
python3 start_server.py
# API dostępne na http://localhost:5001
```

### 4. Demo aplikacji
- **Dashboard**: http://localhost:5173
- **Demo automat**: http://localhost:5001/automat
- **API docs**: http://localhost:5001/api/version

## 📊 Funkcje Demo

### 🎯 Testowanie QR Workflow
1. Utwórz mieszankę w Kreatorze
2. Kliknij "🎯 Zamów" → generuje QR kod
3. Przejdź do Mobile QR App
4. Zeskanuj kod (lub wpisz ręcznie)
5. Symuluj płatność mobilną
6. Śledź postęp zamówienia

### 🏆 Program Lojalnościowy
1. Użyj "Symuluj zamówienie" w Loyalty Program
2. Obserwuj przyznawanie punktów (15 pkt za 15zł)
3. Awansuj poziomy (50 → 150 → 400 → 1000 pkt)
4. Wymieniaj punkty na nagrody w sklepie

### 📱 Mobile Features
- **Push notifications** przy każdej akcji
- **Payment simulator** z 3 metodami płatności
- **Real-time tracking** z progress bars
- **Interactive maps** z geolokalizacją

## 🌟 Zaawansowane Funkcje

- **LocalStorage persistence** - zapisane mieszanki nie znikają
- **Cross-component communication** między modułami
- **Real-time API integration** z backend services
- **Animated UI components** z Vue transitions
- **TypeScript type safety** w całym fronendzie
- **Mobile PWA ready** z service workers support

## 🎯 Philosophy IKIGAI

Aplikacja implementuje japońską koncepcję IKIGAI poprzez 4 filary:
- 🎯 **Co kochasz** - personalizowane mieszanki
- 💪 **W czym jesteś dobry** - rekomendacje AI
- 🌍 **Czego potrzebuje świat** - zdrowe odżywianie
- 💰 **Za co otrzymasz wynagrodzenie** - program lojalnościowy

**"Healthy choices made easy"** - to nasza misja! 🌱

---

**Zbudowane z ❤️ i filozofią IKIGAI dla zdrowego stylu życia**
