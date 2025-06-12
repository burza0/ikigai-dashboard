#!/bin/bash

echo "🌱 IKIGAI Dashboard - Uruchamianie aplikacji..."

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [ ! -f "package.json" ]; then
    echo "❌ Uruchom skrypt z głównego katalogu projektu!"
    exit 1
fi

# Sprawdź czy Node.js jest zainstalowany
if ! command -v node &> /dev/null; then
    echo "❌ Node.js nie jest zainstalowany!"
    exit 1
fi

# Sprawdź czy Python3 jest zainstalowany
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nie jest zainstalowany!"
    exit 1
fi

# Funkcja zatrzymania wszystkich procesów
cleanup() {
    echo ""
    echo "🛑 Zatrzymywanie aplikacji..."
    
    # Zatrzymaj backend
    pkill -f "python3 analytics_server.py" 2>/dev/null
    
    # Zatrzymaj frontend
    pkill -f "vite" 2>/dev/null
    
    echo "✅ Aplikacja zatrzymana"
    exit 0
}

# Obsługa Ctrl+C
trap cleanup SIGINT SIGTERM

# Sprawdź czy porty są wolne
if lsof -i:5001 &> /dev/null; then
    echo "⚠️  Port 5001 (backend) jest zajęty. Zatrzymywanie procesu..."
    pkill -f "python3 analytics_server.py" 2>/dev/null
    sleep 2
fi

if lsof -i:5173 &> /dev/null; then
    echo "⚠️  Port 5173 (frontend) jest zajęty. Zatrzymywanie procesu..."
    pkill -f "vite" 2>/dev/null
    sleep 2
fi

echo "🚀 Uruchamianie backendu (port 5001)..."
cd backend
nohup python3 analytics_server.py > server.log 2>&1 &
BACKEND_PID=$!

echo "⏳ Oczekiwanie na uruchomienie backendu..."
sleep 3

# Sprawdź czy backend działa
if ! curl -s http://localhost:5001/api/health > /dev/null; then
    echo "❌ Backend nie uruchomił się poprawnie!"
    echo "📋 Sprawdź logi: tail -f backend/server.log"
    exit 1
fi

echo "✅ Backend uruchomiony (PID: $BACKEND_PID)"
cd ..

echo "🚀 Uruchamianie frontendu (port 5173)..."
echo "🌐 Aplikacja będzie dostępna na: http://localhost:5173"
echo "🔧 Backend API dostępne na: http://localhost:5001"
echo ""
echo "📋 Konta demo:"
echo "   👑 Admin: admin / admin123"
echo "   👤 User: web_user / demo123"
echo ""
echo "💡 Aby zatrzymać aplikację, naciśnij Ctrl+C"
echo ""

# Uruchom frontend (w trybie interaktywnym)
npm run dev

# Jeśli frontend się zamknie, zatrzymaj wszystko
cleanup 