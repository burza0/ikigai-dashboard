#!/bin/bash

echo "🛑 IKIGAI Dashboard - Zatrzymywanie aplikacji..."

# Zatrzymaj backend
echo "🔌 Zatrzymywanie backendu..."
pkill -f "python3 analytics_server.py" 2>/dev/null

# Zatrzymaj frontend
echo "🔌 Zatrzymywanie frontendu..."
pkill -f "vite" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null

# Sprawdź czy porty są zwolnione
sleep 2

if lsof -i:5001 &> /dev/null; then
    echo "⚠️  Port 5001 nadal zajęty, wymuszam zatrzymanie..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
fi

if lsof -i:5173 &> /dev/null; then
    echo "⚠️  Port 5173 nadal zajęty, wymuszam zatrzymanie..."
    lsof -ti:5173 | xargs kill -9 2>/dev/null
fi

echo "✅ Aplikacja IKIGAI zatrzymana"

# Pokaż status portów
echo ""
echo "📊 Status portów:"
if lsof -i:5001 &> /dev/null; then
    echo "   ❌ Port 5001 (backend): ZAJĘTY"
else
    echo "   ✅ Port 5001 (backend): WOLNY"
fi

if lsof -i:5173 &> /dev/null; then
    echo "   ❌ Port 5173 (frontend): ZAJĘTY"
else
    echo "   ✅ Port 5173 (frontend): WOLNY"
fi

echo ""
echo "💡 Aby uruchomić aplikację ponownie, użyj: ./start_ikigai.sh" 