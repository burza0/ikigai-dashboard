# 🌱 IKIGAI Dashboard

Kompletna aplikacja zarządzania zdrowym żywieniem z systemem lojalnościowym, kreator przepisów, mapą maszyn vendingowych i wyzwaniami społecznymi. **Wersja 4.1** z pełną kontrolą dostępu opartą na rolach.

## 🚀 Szybki start

### Uruchamianie aplikacji

```bash
# Uruchom całą aplikację jednym poleceniem
./start_ikigai.sh
```

### Zatrzymywanie aplikacji

```bash
# Zatrzymaj całą aplikację
./stop_ikigai.sh
```

## 🎯 Funkcjonalności

### 🌍 Dla wszystkich użytkowników (niezalogowanych):
- **🏠 Dashboard** - Przegląd główny z Top 5 Bowl IKIGAI i filozofią
- **🥣 Kreator** - Tworzenie przepisów z kalkulatorem kalorii i składników
- **🗺️ Mapa** - Interaktywna mapa z lokalizacjami automatów vendingowych (5 lokalizacji)
- **📱 Mobile QR** - Kody QR do aplikacji mobilnej i skanowania

### 🔐 Dla zalogowanych użytkowników:
- **🎯 Social Challenges** - Wyzwania społeczne Gen Z z rankingami i nagrodami
- **🏆 Loyalty Program** - Kompletny program lojalnościowy z punktami i wyzwaniami
- **🌟 Top 5 Bowl IKIGAI** - Możliwość zamawiania polecanych przepisów jednym kliknięciem
- **👥 Profile społecznościowe** - Aktywność znajomych i osiągnięcia

### 👑 Dla administratorów:
- **📊 Analytics** - Zaawansowana analityka sprzedaży i raportowanie
- **🎛️ Zarządzanie systemem** - Pełny dostęp do wszystkich funkcji
- **📈 Dashboard administratora** - Statystyki zamówień i użytkowników

## 👥 Konta demo

### Administrator
- **Login:** `admin`
- **Hasło:** `admin123`
- **Uprawnienia:** Pełny dostęp do wszystkich funkcji + Analytics

### Użytkownik testowy
- **Login:** `web_user`
- **Hasło:** `demo123`
- **Uprawnienia:** Social Challenges + Loyalty Program (2847 punktów)

## 🔧 Adresy aplikacji

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5001
- **Health Check:** http://localhost:5001/api/health
- **Live Demo:** Sprawdź czy oba serwery są uruchomione przed użyciem

## 📊 Struktura bazy danych

Aplikacja używa bazy SQLite (`backend/ikigai.db`) z tabelami:
- `users` - Użytkownicy z pełną autentykacją (hasła SHA-256)
- `recipes` - 5 gotowych przepisów/produktów z cenami
- `ingredients` - 7 składników bazowych (w tym nowa Protein Czekoladowy Premium)
- `categories` - Kategorie przepisów i składników
- `loyalty_challenges` - 3 wyzwania w programie lojalnościowym
- `loyalty_rewards` - 5 dostępnych nagród
- `user_challenge_progress` - Postęp użytkowników w wyzwaniach
- `orders` - Historia zamówień z metadanymi

## 🆕 Najnowsze zmiany (v4.1)

### ✅ Naprawiono:
- **Top 5 Bowl IKIGAI** - Teraz poprawnie wyświetla 3 polecane przepisy z cenami
- **Nawigacja oparta na rolach** - Różne menu dla niezalogowanych/zalogowanych/adminów
- **Social Challenges** - Ukryte dla niezalogowanych, widoczne tylko po logowaniu
- **Logika dostępu** - Kontrola uprawnień na poziomie interfejsu
- **Mapowanie danych API** - Poprawna integracja frontendu z backendem

### 🔐 Bezpieczeństwo:
- Automatyczne przekierowania dla nieuprawnionych użytkowników
- Ekrany blokujące z zachętą do logowania
- Sesyjne zarządzanie stanem uwierzytelnienia

## 🛠️ Rozwiązywanie problemów

### ⚡ Szybkie rozwiązania:
```bash
# Zatrzymaj wszystko i uruchom ponownie
./stop_ikigai.sh && ./start_ikigai.sh

# Sprawdź status serwerów
curl http://localhost:5001/api/health
curl http://localhost:5173
```

### Backend nie uruchamia się
```bash
# Sprawdź logi backendu
tail -f backend/server.log

# Sprawdź czy port 5001 jest wolny
lsof -i:5001

# Wymuś zatrzymanie procesów
./stop_ikigai.sh
```

### Frontend nie uruchamia się
```bash
# Sprawdź czy port 5173 jest wolny
lsof -i:5173

# Zainstaluj/aktualizuj zależności
npm install

# Uruchom ręcznie w trybie dev
npm run dev
```

### Problemy z bazą danych
```bash
# Sprawdź czy baza istnieje
ls -la backend/ikigai.db

# Sprawdź czy SQLite Browser nie blokuje
ps aux | grep -i sqlite

# Reinicjalizuj bazę (UWAGA: usuwa wszystkie dane!)
cd backend && python3 init_ikigai_db.py
```

## 📁 Struktura projektu

```
ikigai-dashboard/
├── src/                    # Frontend Vue.js + TypeScript
│   ├── components/         # Komponenty Vue (Dashboard, Loyalty, Social, etc.)
│   ├── App.vue            # Główny komponent z nawigacją i autentykacją
│   └── style.css          # Globalne style Tailwind CSS
├── backend/               # Backend Flask + SQLite
│   ├── analytics_server.py # Główny serwer API z pełną autentykacją
│   ├── ikigai.db          # Baza danych SQLite z danymi demo
│   ├── init_ikigai_db.py  # Skrypt inicjalizacji bazy
│   └── server.log         # Logi serwera (tworzone automatycznie)
├── start_ikigai.sh        # 🚀 Skrypt uruchamiający (z kontrolą portów)
├── stop_ikigai.sh         # 🛑 Skrypt zatrzymujący (czyste zamknięcie)
├── package.json           # Zależności npm (Vue 3, Vite, TypeScript)
└── README.md              # Ta dokumentacja
```

## 🔐 System autentykacji

### Funkcje bezpieczeństwa:
- **Haszowanie haseł:** SHA-256 z bezpiecznym przechowywaniem
- **Sesje:** Zarządzane przez Flask z cookies
- **Role:** Admin vs User z różnymi uprawnieniami
- **Blokada:** Automatyczna blokada po 5 nieudanych próbach
- **Logout:** Bezpieczne wylogowanie z czyszczeniem sesji

### Flow autentykacji:
1. Użytkownik loguje się przez LoginForm
2. Backend weryfikuje dane i tworzy sesję
3. Frontend otrzymuje dane użytkownika
4. Nawigacja dostosowuje się do roli użytkownika
5. Automatyczne sprawdzenie statusu przy starcie aplikacji

## 📝 API Endpoints

### 🔐 Autentykacja
- `POST /api/auth/login` - Logowanie (username + password)
- `POST /api/auth/register` - Rejestracja nowego użytkownika
- `POST /api/auth/logout` - Bezpieczne wylogowanie
- `GET /api/auth/profile` - Profil aktualnego użytkownika
- `GET /api/auth/users` - Lista użytkowników (tylko admin)

### 🍜 Przepisy i składniki
- `GET /api/meal-recipes` - Lista wszystkich przepisów (5)
- `GET /api/meal-recipes/categories` - Kategorie przepisów
- `GET /api/ingredients` - Lista składników (7)
- `GET /api/ingredients/categories` - Kategorie składników
- `GET /api/recommendations` - Top polecane przepisy (3)

### 🏆 Program lojalnościowy
- `GET /api/loyalty/profile/{user_id}` - Profil użytkownika (punkty, poziom)
- `GET /api/loyalty/challenges/{user_id}` - Wyzwania użytkownika (3)
- `GET /api/loyalty/rewards` - Dostępne nagrody (5)

### 📊 Analityka (tylko admin)
- `GET /api/analytics/dashboard` - Dane analityczne
- `GET /api/vending-machines` - Lokalizacje automatów (5)
- `GET /api/orders` - Historia wszystkich zamówień

### 🏥 System
- `GET /api/health` - Status zdrowia systemu i bazy danych

## 💡 Najlepsze praktyki

### 🚀 Development:
1. **Hot Reload:** Frontend i backend obsługują automatyczne przeładowanie
2. **Logi:** Zawsze sprawdzaj `backend/server.log` przy problemach
3. **Porty:** Używaj skryptów start/stop aby uniknąć konfliktów
4. **Baza:** Regularne backupy `ikigai.db` przed większymi zmianami

### 🎨 UX:
1. **Responsywność:** Aplikacja działa na desktop i mobile
2. **Dark Mode:** Automatyczne przełączanie między trybami
3. **Loading States:** Wszystkie asynchroniczne operacje mają wskaźniki
4. **Error Handling:** Przyjazne komunikaty błędów dla użytkownika

## 🔄 Przepływ użytkownika

### Niezalogowany:
1. **Dashboard** → Zobacz filozofię IKIGAI i zachętę do logowania
2. **Kreator** → Tworzenie własnych przepisów
3. **Mapa** → Znajdź najbliższy automat
4. **Mobile QR** → Pobierz aplikację mobilną

### Zalogowany:
1. **Dashboard** → Social Challenges + Top 5 Bowl z możliwością zamawiania
2. **Social Challenges** → Rywalizacja, rankingi, osiągnięcia  
3. **Loyalty** → Zbieranie punktów, wyzwania, nagrody
4. Wszystkie funkcje z poziomu niezalogowanego

### Administrator:
1. **Analytics** → Pełna analityka biznesowa
2. **Zarządzanie** → Dostęp do wszystkich danych
3. Wszystkie funkcje użytkownika zalogowanego

## 🆘 Pomoc i wsparcie

### Najczęstsze problemy:
1. **Pusta sekcja Top 5:** Sprawdź czy backend odpowiada na `/api/recommendations`
2. **Błąd logowania:** Sprawdź czy baza danych nie jest zablokowana
3. **Porty zajęte:** Użyj `./stop_ikigai.sh` przed ponownym uruchomieniem

### Komenda diagnostyczna:
```bash
# Pełna diagnostyka systemu
echo "=== Status portów ===" && lsof -i:5001,5173
echo "=== Procesy ===" && ps aux | grep -E "(python3|vite|npm)"
echo "=== API Health ===" && curl -s http://localhost:5001/api/health
echo "=== Logi ===" && tail -3 backend/server.log
```

---

*Wersja: 4.1 z pełną kontrolą dostępu i naprawionymi rekomendacjami* 🌱✨
