from flask import Flask, jsonify, request
from flask_cors import CORS
import qrcode
import base64
import io
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Przykładowe dane w pamięci (zamiast bazy danych)
zawodnicy_data = [
    {"nr_startowy": 1, "imie": "Jan", "nazwisko": "Kowalski", "kategoria": "Senior", "plec": "M", "klub": "KTH Krynica", "qr_code": None, "checked_in": False},
    {"nr_startowy": 2, "imie": "Anna", "nazwisko": "Nowak", "kategoria": "Senior", "plec": "K", "klub": "UKS Boots", "qr_code": None, "checked_in": False},
    {"nr_startowy": 3, "imie": "Piotr", "nazwisko": "Wiśniewski", "kategoria": "Junior", "plec": "M", "klub": "KTH Krynica", "qr_code": None, "checked_in": False},
    {"nr_startowy": 4, "imie": "Maria", "nazwisko": "Wójcik", "kategoria": "Junior", "plec": "K", "klub": "UKS Boots", "qr_code": None, "checked_in": False},
    {"nr_startowy": 5, "imie": "Tomasz", "nazwisko": "Kowalczyk", "kategoria": "Senior", "plec": "M", "klub": "SKL Zakopane", "qr_code": None, "checked_in": False},
]

grupy_startowe_data = [
    {"kategoria": "Senior", "plec": "M", "numer_grupy": 1, "nazwa": "Senior Mężczyźni", "status": "WAITING"},
    {"kategoria": "Senior", "plec": "K", "numer_grupy": 2, "nazwa": "Senior Kobiety", "status": "WAITING"},
    {"kategoria": "Junior", "plec": "M", "numer_grupy": 3, "nazwa": "Junior Mężczyźni", "status": "WAITING"},
    {"kategoria": "Junior", "plec": "K", "numer_grupy": 4, "nazwa": "Junior Kobiety", "status": "WAITING"},
]

@app.route("/api/zawodnicy")
def zawodnicy():
    """Endpoint zwracający listę zawodników z QR kodami"""
    return jsonify(zawodnicy_data)

@app.route("/api/qr/generate/<int:nr_startowy>", methods=['POST'])
def qr_generate_for_zawodnik(nr_startowy):
    """Generowanie QR kodu dla pojedynczego zawodnika"""
    try:
        # Znajdź zawodnika
        zawodnik = None
        for z in zawodnicy_data:
            if z["nr_startowy"] == nr_startowy:
                zawodnik = z
                break
        
        if not zawodnik:
            return jsonify({"error": "Zawodnik nie istnieje"}), 404
        
        # Wygeneruj QR kod
        qr_data = f"SKATECROSS_QR_{nr_startowy}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Zapisz QR kod w pamięci
        zawodnik["qr_code"] = qr_data
        
        # Wygeneruj obraz QR kodu jako base64
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "qr_code": qr_data,
            "qr_image": f"data:image/png;base64,{img_str}",
            "zawodnik": zawodnik
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd generowania QR: {str(e)}"
        }), 500

@app.route("/api/qr/generate-bulk", methods=['POST'])
def qr_generate_bulk():
    """Masowe generowanie QR kodów"""
    try:
        data = request.json
        numery_startowe = data.get('numery_startowe', [])
        
        if not numery_startowe:
            return jsonify({"error": "Brak numerów startowych"}), 400
        
        results = []
        
        for nr_startowy in numery_startowe:
            try:
                # Znajdź zawodnika
                zawodnik = None
                for z in zawodnicy_data:
                    if z["nr_startowy"] == nr_startowy:
                        zawodnik = z
                        break
                
                if not zawodnik:
                    results.append({
                        "nr_startowy": nr_startowy,
                        "success": False,
                        "error": "Zawodnik nie istnieje"
                    })
                    continue
                
                # Wygeneruj QR kod
                qr_data = f"SKATECROSS_QR_{nr_startowy}"
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(qr_data)
                qr.make(fit=True)
                
                # Zapisz QR kod w pamięci
                zawodnik["qr_code"] = qr_data
                
                # Wygeneruj obraz QR kodu jako base64
                img = qr.make_image(fill_color="black", back_color="white")
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                results.append({
                    "nr_startowy": nr_startowy,
                    "success": True,
                    "qr_code": qr_data,
                    "qr_image": f"data:image/png;base64,{img_str}",
                    "zawodnik": zawodnik
                })
                
            except Exception as e:
                results.append({
                    "nr_startowy": nr_startowy,
                    "success": False,
                    "error": str(e)
                })
        
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        return jsonify({
            "success": True,
            "generated": len(successful),
            "failed": len(failed),
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd masowego generowania QR: {str(e)}"
        }), 500

@app.route("/api/qr/stats")
def qr_stats():
    """Statystyki QR kodów"""
    try:
        total_zawodnikow = len(zawodnicy_data)
        z_qr_kodami = len([z for z in zawodnicy_data if z.get("qr_code")])
        bez_qr_kodow = total_zawodnikow - z_qr_kodami
        
        return jsonify({
            "total_zawodnikow": total_zawodnikow,
            "z_qr_kodami": z_qr_kodami,
            "bez_qr_kodow": bez_qr_kodow
        })
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania statystyk QR: {str(e)}"}), 500

@app.route("/api/grupy-startowe")
def grupy_startowe():
    """Endpoint zwracający grupy startowe"""
    try:
        result = []
        for grupa in grupy_startowe_data:
            # Znajdź zawodników w tej grupie
            zawodnicy_w_grupie = [z for z in zawodnicy_data 
                                  if z["kategoria"] == grupa["kategoria"] and z["plec"] == grupa["plec"]]
            
            grupa_info = grupa.copy()
            grupa_info["liczba_zawodnikow"] = len(zawodnicy_w_grupie)
            grupa_info["numery_startowe"] = ", ".join([str(z["nr_startowy"]) for z in zawodnicy_w_grupie])
            grupa_info["lista_zawodnikow"] = ", ".join([f"{z['imie']} {z['nazwisko']}" for z in zawodnicy_w_grupie])
            grupa_info["estimated_time"] = None
            
            result.append(grupa_info)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Błąd w grupy-startowe: {str(e)}")
        return jsonify({"error": f"Błąd pobierania grup startowych: {str(e)}"}), 500

@app.route("/api/grupa-aktywna", methods=['GET'])
def get_grupa_aktywna():
    """Pobieranie aktywnej grupy"""
    try:
        aktywna_grupa = None
        for grupa in grupy_startowe_data:
            if grupa["status"] == "ACTIVE":
                aktywna_grupa = grupa
                break
        
        return jsonify({
            "success": True,
            "grupa": aktywna_grupa
        })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd pobierania aktywnej grupy: {str(e)}"
        }), 500

@app.route("/api/grupa-aktywna", methods=['POST'])
def set_grupa_aktywna():
    """Ustawianie/usuwanie aktywnej grupy"""
    try:
        data = request.json
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        nazwa = data.get('nazwa')
        
        # Znajdź grupę
        grupa = None
        for g in grupy_startowe_data:
            if g["kategoria"] == kategoria and g["plec"] == plec:
                grupa = g
                break
        
        if not grupa:
            return jsonify({
                "success": False,
                "error": "Grupa nie istnieje"
            }), 404
        
        # Sprawdź czy grupa już jest aktywna
        if grupa["status"] == "ACTIVE":
            # Deaktywuj grupę
            grupa["status"] = "WAITING"
            return jsonify({
                "success": True,
                "action": "removed",
                "message": f"Grupa {nazwa} została deaktywowana"
            })
        else:
            # Deaktywuj wszystkie inne grupy
            for g in grupy_startowe_data:
                g["status"] = "WAITING"
            
            # Aktywuj wybraną grupę
            grupa["status"] = "ACTIVE"
            return jsonify({
                "success": True,
                "action": "added",
                "message": f"Grupa {nazwa} została aktywowana"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd toggle grupy aktywnej: {str(e)}"
        }), 500

@app.route("/api/start-queue", methods=['GET'])
def get_start_queue():
    """Pobieranie kolejki startowej"""
    try:
        result = []
        
        # Dodaj zawodników z aktywnej grupy
        for grupa in grupy_startowe_data:
            if grupa["status"] == "ACTIVE":
                zawodnicy_w_grupie = [z for z in zawodnicy_data 
                                      if z["kategoria"] == grupa["kategoria"] and z["plec"] == grupa["plec"]]
                for z in zawodnicy_w_grupie:
                    zawodnik_info = z.copy()
                    zawodnik_info["source_type"] = "AKTYWNA_GRUPA"
                    zawodnik_info["ostatni_skan"] = None
                    result.append(zawodnik_info)
        
        # Dodaj skanowanych zawodników
        for z in zawodnicy_data:
            if z.get("checked_in"):
                zawodnik_info = z.copy()
                zawodnik_info["source_type"] = "SKANOWANY"
                zawodnik_info["ostatni_skan"] = datetime.now().isoformat()
                # Usuń duplikaty
                if not any(r["nr_startowy"] == z["nr_startowy"] for r in result):
                    result.append(zawodnik_info)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania kolejki startowej: {str(e)}"}), 500

@app.route("/api/qr/scan-result", methods=['POST'])
def qr_scan_result():
    """Endpoint dla skanowania QR kodów w centrum startu"""
    try:
        data = request.json
        qr_code = data.get('qr_code', '').strip()
        
        if not qr_code:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": "Pusty kod QR"
            }), 400
        
        # Spróbuj wyciągnąć numer startowy z QR kodu
        if qr_code.startswith('SKATECROSS_QR_'):
            nr_startowy_str = qr_code.replace('SKATECROSS_QR_', '')
        else:
            nr_startowy_str = qr_code
        
        try:
            nr_startowy = int(nr_startowy_str)
        except ValueError:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": f"Nieprawidłowy format kodu QR: {qr_code}"
            }), 400
        
        # Znajdź zawodnika
        zawodnik = None
        for z in zawodnicy_data:
            if z["nr_startowy"] == nr_startowy:
                zawodnik = z
                break
        
        if not zawodnik:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": f"Zawodnik z numerem {nr_startowy} nie istnieje"
            }), 404
        
        # Sprawdź czy już jest w kolejce
        if zawodnik.get('checked_in'):
            return jsonify({
                "success": True,
                "action": "OSTRZEZENIE",
                "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} jest już w kolejce",
                "zawodnik": zawodnik
            })
        
        # Dodaj zawodnika do kolejki
        zawodnik["checked_in"] = True
        zawodnik["check_in_time"] = datetime.now().isoformat()
        zawodnik["ostatni_skan"] = datetime.now().isoformat()
        
        return jsonify({
            "success": True,
            "action": "AKCEPTUJ",
            "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} dodany do kolejki",
            "zawodnik": zawodnik
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "action": "ODRZUC",
            "message": f"Błąd skanowania: {str(e)}"
        }), 500

@app.route("/api/version")
def get_version():
    """Endpoint zwracający wersję systemu"""
    try:
        return jsonify({
            "version": "1.0.0",
            "name": "SKATECROSS QR System (Demo Mode)",
            "features": ["QR Generation", "QR Printing", "Start Queue", "Scanner"],
            "status": "demo",
            "environment": "standalone",
            "database": "in-memory"
        })
    except Exception as e:
        return jsonify({"version": "unknown", "error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Uruchamiam SKATECROSS QR Backend (Demo Mode)")
    print("📊 Dane przechowywane w pamięci")
    print("🌐 Serwer dostępny na http://localhost:5001")
    app.run(debug=True, port=5001) 