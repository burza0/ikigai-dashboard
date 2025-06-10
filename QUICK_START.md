# 🚀 Szybki Start - SKATECROSS QR Frontend

## ⚡ Uruchomienie w 3 krokach

### 1. Instalacja dependencies
```bash
npm install
```

### 2. Uruchomienie dev server
```bash
npm run dev
```

### 3. Otwórz w przeglądarce
```
http://localhost:5173
```

## 🔗 Połączenie z backendem

Upewnij się, że **backend SKATECROSS** działa na porcie `5001`:
```bash
cd ../backend
python api_server.py
```

Vite automatycznie przekierowuje zapytania `/api/*` na backend.

## 🎛️ Dostępne funkcje

### 🏁 Centrum Startu (`/start-line`)
- Zarządzanie grupami startowymi
- QR Scanner dla zawodników
- Kolejka startowa
- Dashboard statusu

### 🖨️ Drukowanie QR (`/qr-print`)
- Lista zawodników z filtrami
- Generowanie QR kodów
- System drukowania naklejek
- Operacje grupowe

## 🌙 Funkcje UI

- **Dark/Light Mode** - przełącznik w górnym pasku
- **Admin Mode** - toggle dla zaawansowanych funkcji
- **Responsive** - działa na mobile/tablet/desktop

## 🛠️ Komendy pomocnicze

```bash
# Build do produkcji
npm run build

# Podgląd buildu
npm run preview

# Reinstalacja dependencies
rm -rf node_modules && npm install
```

## 🔧 Troubleshooting

### Backend niedostępny
- Sprawdź czy backend działa na porcie 5001
- Uruchom: `cd ../backend && python api_server.py`

### Błędy TypeScript
- Uruchom: `npm run build` i sprawdź błędy

### Problemy z dependencies
- Usuń `node_modules` i uruchom `npm install`

---

**Gotowe! 🎉** Powinieneś mieć działającą aplikację SKATECROSS QR! 