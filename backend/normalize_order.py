def normalize_order_data(raw_data):
    """Normalizuje dane z różnych formatów frontendu do formatu backendu"""
    data = {}
    
    # user_id
    data["user_id"] = raw_data.get("user_id", "web_user")
    
    # machine_id (frontend używa vending_machine_id)
    data["machine_id"] = raw_data.get("machine_id") or raw_data.get("vending_machine_id", "VM001")
    
    # payment_method (domyślnie card)  
    data["payment_method"] = raw_data.get("payment_method", "card")
    
    # recipe_id - różne formaty
    if raw_data.get("recipe_id"):
        data["recipe_id"] = raw_data["recipe_id"]
    elif raw_data.get("mixture_name") or raw_data.get("items"):
        data["recipe_id"] = "detox_green"  # Domyślny dla custom mieszanek
    else:
        data["recipe_id"] = "detox_green"
    
    # notes - dodatkowe informacje z frontu
    notes_parts = []
    if raw_data.get("mixture_name"):
        notes_parts.append(f"Nazwa: {raw_data['mixture_name']}")
    if raw_data.get("items"):
        notes_parts.append(f"Składniki: {len(raw_data['items'])}")
    if raw_data.get("quick_order"):
        notes_parts.append("Szybkie zamówienie")
    
    data["notes"] = "; ".join(notes_parts) + (f"; {raw_data.get('notes', '')}" if raw_data.get("notes") else "")
    
    return data 