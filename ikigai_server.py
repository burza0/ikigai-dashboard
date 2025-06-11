# -*- coding: utf-8 -*-
"""
IKIGAI Dashboard Backend - Modular Architecture v2.0
Wersja: 2.0.0
Zdrowe automaty vendingowe z QR kodami zamówień
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import sys
import os

# Dodaj backend do path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

print("🎯 Ładuję IKIGAI Modules...")
print("🛒 orders.py - QR Orders Workflow")
print("🛍️ products.py - Product Catalog & Vending Machines")
print("👤 zawodnicy.py - Users (legacy)")
print("🔲 qr_generation.py - QR Legacy")
print("🏁 centrum_startu.py - Legacy")

# Import blueprintów IKIGAI
try:
    from backend.api.orders import orders_bp
    print("✅ orders_bp imported")
except ImportError as e:
    print(f"❌ Error importing orders_bp: {e}")
    orders_bp = None

try:
    from backend.api.products import products_bp
    print("✅ products_bp imported")
except ImportError as e:
    print(f"❌ Error importing products_bp: {e}")
    products_bp = None

try:
    from backend.api.ingredients import ingredients_bp
    print("✅ ingredients_bp imported")
except ImportError as e:
    print(f"❌ Error importing ingredients_bp: {e}")
    ingredients_bp = None

try:
    from backend.api.loyalty import loyalty_bp
    print("✅ loyalty_bp imported")
except ImportError as e:
    print(f"❌ Error importing loyalty_bp: {e}")
    loyalty_bp = None

# Legacy blueprinty (do transformacji)
from backend.api.zawodnicy import zawodnicy_bp
from backend.api.qr_generation import qr_generation_bp
from backend.api.centrum_startu import centrum_startu_bp

def create_app():
    """Tworzenie aplikacji Flask IKIGAI"""
    app = Flask(__name__)
    
    # CORS dla wszystkich origins
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 🆕 IKIGAI Blueprinty
    if orders_bp:
        app.register_blueprint(orders_bp)
        print("✅ orders_bp registered")
    
    if products_bp:
        app.register_blueprint(products_bp)
        print("✅ products_bp registered")
    
    # 🔄 Legacy blueprinty (do transformacji)
    app.register_blueprint(zawodnicy_bp)
    app.register_blueprint(qr_generation_bp)
    app.register_blueprint(centrum_startu_bp)
    
    # 🏠 Strona główna IKIGAI - NOWOCZESNY DASHBOARD
    @app.route('/', methods=['GET'])
    def home():
        """IKIGAI Dashboard - Nowoczesny Kafelkowy Dashboard dla Automatów Vendingowych"""
        # Wczytaj nowy dashboard HTML
        try:
            with open('ikigai_dashboard.html', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return """
            <html><body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>🌱 IKIGAI Dashboard</h1>
                <p>Dashboard HTML file not found. Please check ikigai_dashboard.html</p>
                <a href="/api/version">API Version Info</a>
            </body></html>
            """
    
    # Endpoint główny wersji
    @app.route('/api/version', methods=['GET'])
    def get_version():
        """Informacje o wersji IKIGAI"""
        return {
            "success": True,
            "data": {
                "name": "IKIGAI Dashboard Backend",
                "version": "2.0.0",
                "architecture": "Modularna Architektura IKIGAI",
                "description": "System Zamówień QR dla zdrowych automatów vendingowych",
                "modules": [
                    "🛒 orders_bp - Zamówienia IKIGAI + Workflow QR" if orders_bp else "❌ orders_bp - NIEPOWODZENIE",
                    "🛍️ products_bp - Katalog Produktów + Automaty Vendingowe" if products_bp else "❌ products_bp - NIEPOWODZENIE", 
                    "👤 zawodnicy_bp - Użytkownicy (legacy → transformacja)",
                    "🔲 qr_generation_bp - QR Legacy (→ produkty)",
                    "🏁 centrum_startu_bp - Legacy (→ automaty)",
                    "👨‍🍳 ingredients_bp - Składniki",
                    "🏷️ loyalty_bp - Program lojalnościowy"
                ],
                "features": [
                    "📱 Kompozycja Zamówienia w Aplikacji Mobilnej",
                    "🎯 Generowanie Kodu QR dla Zamówień", 
                    "📱 Skanowanie QR w Automatach Vendingowych",
                    "🚀 Automatyczne Przygotowanie Zamówienia",
                    "📊 Śledzenie Statusu Zamówienia w Czasie Rzeczywistym",
                    "🛍️ Katalog Produktów z Informacjami Żywieniowymi",
                    "🏪 Lokalizacje i Status Automatów Vendingowych",
                    "🌱 Etykiety Dietetyczne i Filtrowanie",
                    "👨‍🍳 Składniki",
                    "🏷️ Program lojalnościowy"
                ],
                "workflow": [
                    "1. 📱 Użytkownik komponuje zamówienie w aplikacji mobilnej",
                    "2. 🎯 System generuje kod QR dla zamówienia", 
                    "3. 📱 Użytkownik skanuje QR w automacie vendingowym",
                    "4. 🚀 Automat automatycznie przygotowuje zamówienie",
                    "5. 📊 Śledzenie statusu w czasie rzeczywistym (0-100%)"
                ],
                "data_source": "Demo w Pamięci + Baza Danych Zamówień",
                "build_date": "2025-06-10",
                "transformation": "SKATECROSS → IKIGAI",
                "philosophy": "Japońska IKIGAI - Czynienie zdrowych wyborów łatwymi i dostępnymi"
            }
        }
    
    # 🏪 Demo: Automat Vendingowy
    @app.route('/automat', methods=['GET'])
    def vending_machine():
        """Strona automatu vendingowego z możliwością skanowania QR"""
        html = """
        <!DOCTYPE html>
        <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🏪 IKIGAI Automat Vendingowy</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    margin: 0;
                    padding: 20px;
                    color: white;
                    min-height: 100vh;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    padding: 40px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                    border: 2px solid rgba(255,255,255,0.2);
                }
                h1 {
                    text-align: center;
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    background: linear-gradient(45deg, #FFB6C1, #98FB98);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                .scanner-section {
                    background: rgba(255, 255, 255, 0.9);
                    color: #333;
                    padding: 30px;
                    border-radius: 15px;
                    margin: 20px 0;
                }
                .qr-input {
                    width: 100%;
                    padding: 15px;
                    font-size: 16px;
                    border: 2px solid #ddd;
                    border-radius: 10px;
                    margin: 10px 0;
                }
                .scan-btn {
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(45deg, #FF69B4, #32CD32);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 18px;
                    font-weight: 700;
                    cursor: pointer;
                    margin: 10px 0;
                }
                .scan-btn:hover {
                    transform: scale(1.02);
                }
                .result {
                    margin: 20px 0;
                    padding: 20px;
                    border-radius: 10px;
                    display: none;
                }
                .success {
                    background: #e8f5e8;
                    color: #2e7d32;
                    border: 2px solid #4caf50;
                }
                .error {
                    background: #ffebee;
                    color: #c62828;
                    border: 2px solid #f44336;
                }
                .preparation-steps {
                    background: #e3f2fd;
                    color: #1565c0;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }
                .step {
                    padding: 10px;
                    margin: 5px 0;
                    background: rgba(255, 255, 255, 0.8);
                    border-radius: 5px;
                    border-left: 4px solid #2196f3;
                }
                .step.completed {
                    background: rgba(76, 175, 80, 0.2);
                    border-left-color: #4caf50;
                }
                .step.current {
                    background: rgba(255, 193, 7, 0.2);
                    border-left-color: #ff9800;
                    animation: pulse 1s infinite;
                }
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.7; }
                    100% { opacity: 1; }
                }
                .status-display {
                    font-size: 1.5em;
                    text-align: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #98FB98, #87CEEB);
                    color: #333;
                    border-radius: 15px;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏪 IKIGAI Automat Vendingowy</h1>
                <p style="text-align: center; font-size: 1.2em; opacity: 0.8;">
                    Zeskanuj kod QR zamówienia, aby rozpocząć przygotowanie
                </p>
                
                <div class="scanner-section">
                    <h3>📱 Skanowanie Kodu QR</h3>
                    <input type="text" id="qr-input" class="qr-input" 
                           placeholder="Wklej kod QR lub wpisz: IKIGAI:ORDER:id:automat:cena">
                    <button onclick="scanQR()" class="scan-btn">🔍 Skanuj Kod QR</button>
                </div>
                
                <div id="result" class="result"></div>
                <div id="preparation" style="display: none;"></div>
                <div id="status" class="status-display" style="display: none;"></div>
            </div>
            
            <script>
                let currentOrderId = null;
                let preparationSteps = [];
                let currentStep = 0;
                
                async function scanQR() {
                    const qrCode = document.getElementById('qr-input').value.trim();
                    const resultDiv = document.getElementById('result');
                    
                    if (!qrCode) {
                        showError('Wprowadź kod QR');
                        return;
                    }
                    
                    try {
                        const response = await fetch('/api/orders/scan-qr', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                qr_string: qrCode,
                                machine_id: 'ikigai_central'  // Domyślny automat
                            })
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            currentOrderId = data.order.id;
                            preparationSteps = data.preparation_steps || [];
                            
                            showSuccess(`✅ Zamówienie zeskanowane pomyślnie!\\n` +
                                      `Zamówienie: ${data.order.id.substring(0, 8)}...\\n` +
                                      `Status: ${data.order.status}`);
                            
                            startPreparation();
                        } else {
                            showError('❌ Błąd skanowania: ' + data.error);
                        }
                    } catch (error) {
                        showError('❌ Błąd połączenia: ' + error.message);
                    }
                }
                
                function startPreparation() {
                    const prepDiv = document.getElementById('preparation');
                    const statusDiv = document.getElementById('status');
                    
                    prepDiv.style.display = 'block';
                    statusDiv.style.display = 'block';
                    
                    // Wyświetl kroki przygotowania
                    prepDiv.innerHTML = `
                        <div class="preparation-steps">
                            <h3>🚀 Przygotowanie zamówienia...</h3>
                            <div id="steps">
                                ${preparationSteps.map((step, index) => `
                                    <div class="step" id="step-${index}">
                                        ${index + 1}. ${step}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `;
                    
                    // Rozpocznij symulację przygotowania
                    currentStep = 0;
                    simulatePreparation();
                }
                
                function simulatePreparation() {
                    if (currentStep < preparationSteps.length) {
                        // Oznacz poprzedni krok jako ukończony
                        if (currentStep > 0) {
                            document.getElementById(`step-${currentStep - 1}`).classList.add('completed');
                        }
                        
                        // Oznacz aktualny krok
                        const currentStepEl = document.getElementById(`step-${currentStep}`);
                        currentStepEl.classList.add('current');
                        
                        // Aktualizuj status
                        const progress = Math.round(((currentStep + 1) / preparationSteps.length) * 100);
                        document.getElementById('status').innerHTML = `
                            📊 Postęp: ${progress}% | Krok: ${preparationSteps[currentStep]}
                        `;
                        
                        currentStep++;
                        
                        // Następny krok po 2 sekundach
                        setTimeout(simulatePreparation, 2000);
                    } else {
                        // Zakończenie przygotowania
                        document.getElementById(`step-${currentStep - 1}`).classList.add('completed');
                        document.getElementById('status').innerHTML = `
                            🎉 Zamówienie gotowe! Odbierz swoje zdrowe produkty IKIGAI!
                        `;
                        document.getElementById('status').style.background = 'linear-gradient(45deg, #4caf50, #8bc34a)';
                        
                        // Oznacz zamówienie jako gotowe
                        if (currentOrderId) {
                            completeOrder(currentOrderId);
                        }
                    }
                }
                
                async function completeOrder(orderId) {
                    try {
                        await fetch(`/api/orders/${orderId}/complete`, {
                            method: 'POST'
                        });
                    } catch (error) {
                        console.error('Error completing order:', error);
                    }
                }
                
                function showError(message) {
                    const resultDiv = document.getElementById('result');
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = message;
                    resultDiv.style.display = 'block';
                }
                
                function showSuccess(message) {
                    const resultDiv = document.getElementById('result');
                    resultDiv.className = 'result success';
                    resultDiv.innerHTML = message;
                    resultDiv.style.display = 'block';
                }
            </script>
        </body>
        </html>
        """
        return html
    
    return app

if __name__ == '__main__':
    print("🎯 IKIGAI Dashboard - Healthy Vending Machines")
    print("🔗 Rejestruję blueprinty...")
    app = create_app()
    
    # Rejestracja nowych blueprintów
    if ingredients_bp:
        app.register_blueprint(ingredients_bp)
        print("✅ ingredients_bp registered")
    
    if loyalty_bp:
        app.register_blueprint(loyalty_bp)
        print("✅ loyalty_bp registered")
    
    print("🚀 Uruchamiam IKIGAI Backend v2.0.0")
    if orders_bp:
        print("🛒 orders_bp - /api/orders/* (QR Order Workflow)")
    if products_bp:
        print("🛍️ products_bp - /api/products/*, /api/vending-machines/*")
    print("👤 zawodnicy_bp - /api/zawodnicy/* (legacy)")
    print("🔲 qr_generation_bp - /api/qr/* (legacy)")
    print("🏁 centrum_startu_bp - /api/grupy-startowe/* (legacy)")
    print("📊 Demo: 6 produktów + 3 automaty + kompletny QR workflow")
    print("🌐 Serwer dostępny na http://localhost:5001")
    print("🎯 WORKFLOW: Kompozycja → QR → Skanowanie → Przygotowanie")
    print("🌱 Filozofia IKIGAI: Zdrowe wybory łatwo dostępne")
    print("========================================================================")
    
    app.run(host='0.0.0.0', port=5001, debug=True) 