# 🏁 SKATECROSS - Centrum Startu & QR

> **Uproszczona wersja systemu SKATECROSS** zawierająca tylko **Centrum Startu** i **Drukowanie QR kodów**.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Vue](https://img.shields.io/badge/vue-3.5-brightgreen.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.8-blue.svg)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-3.4-06B6D4.svg)

## 🎯 Funkcjonalności

### 🏁 Centrum Startu
- ✅ **Zarządzanie grupami startowymi** - aktywacja/deaktywacja grup
- 📱 **QR Scanner** - skanowanie kodów QR zawodników
- 📊 **Kolejka startowa** - zarządzanie kolejnością startów
- ⚡ **Real-time sync** - synchronizacja z backendem
- 🎛️ **Dashboard** - przegląd statusu grup i zawodników

### 🖨️ Drukowanie QR kodów
- 📋 **Zarządzanie zawodnikami** - lista z filtrami
- 🔲 **Generowanie QR** - masowe i pojedyncze generowanie
- 🖨️ **System drukowania** - gotowe do wydruku naklejki
- 🏷️ **Filtry zaawansowane** - po kategorii, klubie, statusie QR
- ⚡ **Operacje grupowe** - zaznaczanie całych kategorii/klubów

## 🛠️ Stack technologiczny

- **Vue 3.5** - Framework UI
- **TypeScript 5.8** - Typowanie
- **Vite 6.3** - Build tool & dev server
- **TailwindCSS 3.4** - Styling
- **Heroicons 2.2** - Ikony
- **Axios 1.9** - HTTP client
- **QRCode.js 1.5** - Generowanie QR kodów

## 🚀 Instalacja i uruchomienie

### Wymagania
- Node.js 18+
- npm lub yarn

### 1. Instalacja dependencies
```bash
npm install
```

### 2. Uruchomienie środowiska deweloperskiego
```bash
npm run dev
```

### 3. Build do produkcji
```bash
npm run build
```

### 4. Podgląd produkcyjnego buildu
```bash
npm run preview
```

## ⚙️ Konfiguracja

### Backend API
Upewnij się, że backend SKATECROSS działa na porcie 5000. Vite proxy automatycznie przekieruje żądania `/api/*` na `http://localhost:5001`.

### Dark Mode
Aplikacja automatycznie zapisuje preferencje dark mode w localStorage.

### Admin Mode
Toggle admin mode umożliwia dostęp do zaawansowanych funkcji. Domyślnie włączony.

## 📁 Struktura projektu

```
skatecross-qr-frontend/
├── 📂 src/
│   ├── 📂 components/
│   │   ├── 📄 StartLineScanner.vue    # Centrum Startu
│   │   ├── 📄 QrPrint.vue             # Drukowanie QR
│   │   └── 📄 StatusBadge.vue         # Komponent statusu
│   ├── 📄 App.vue                     # Główny komponent
│   ├── 📄 main.ts                     # Entry point
│   └── 📄 style.css                   # Style (Tailwind + custom)
├── 📄 package.json                    # Dependencies
├── 📄 vite.config.ts                  # Konfiguracja Vite
├── 📄 tailwind.config.js              # Konfiguracja TailwindCSS
└── 📄 tsconfig.json                   # Konfiguracja TypeScript
```

## 🎨 Funkcje UI

### Responsywność
- ✅ **Mobile-first** - optymalizacja dla urządzeń mobilnych
- ✅ **Tablet-friendly** - dostosowany layout dla tabletów
- ✅ **Desktop** - pełna funkcjonalność na dużych ekranach

### Dark Mode
- 🌙 **Auto-detection** - automatyczne wykrywanie preferencji systemu
- 💾 **Persistence** - zapamiętywanie wyboru w localStorage
- ⚡ **Smooth transitions** - płynne przejścia między trybami

### Dostępność
- ♿ **ARIA labels** - etykiety dla screen readerów
- ⌨️ **Keyboard navigation** - nawigacja klawiaturą
- 🎨 **High contrast** - wysoki kontrast w dark mode

## 🔗 API Endpoints

### Centrum Startu
- `GET /api/grupy-startowe` - Lista grup startowych
- `POST /api/grupa-aktywna` - Aktywacja/deaktywacja grupy
- `GET /api/kolejka` - Aktualny stan kolejki
- `POST /api/qr-scan` - Skanowanie QR kodu

### Drukowanie QR
- `GET /api/zawodnicy` - Lista zawodników
- `POST /api/qr/generate/{id}` - Generowanie QR dla zawodnika
- `POST /api/qr/generate-bulk` - Masowe generowanie QR

## 🎛️ Komendy NPM

```bash
# Uruchomienie dev server
npm run dev

# Build produkcyjny
npm run build

# Podgląd buildu
npm run preview

# Type checking
npm run type-check
```

## 🔧 Rozszerzenia

Projekt jest zaprojektowany tak, aby można było łatwo dodać:
- Dodatkowe komponenty z głównego systemu SKATECROSS
- Nowe funkcje QR (np. check-in zawodników)
- Integracje z innymi systemami

## 📞 Wsparcie

Projekt jest wydzieloną częścią większego systemu SKATECROSS Tournament System.

## 📄 Licencja

MIT License - zobacz pełny projekt SKATECROSS dla szczegółów.

---

<div align="center">

**Stworzone dla społeczności SKATECROSS** 🏁

</div> 