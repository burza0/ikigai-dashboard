#!/usr/bin/env python3
"""
🐘 Local PostgreSQL Setup for IKIGAI Development
Inicjalizuje lokalną bazę PostgreSQL z pełnymi danymi
"""

import os

# Local PostgreSQL Configuration
LOCAL_DATABASE_URL = "postgresql://ikigai_user:ikigai_pass@localhost:5432/ikigai_dev"

print("🐘 Setting up local PostgreSQL for IKIGAI development...")
print(f"📍 Database URL: {LOCAL_DATABASE_URL}")

# Set environment variable
os.environ['DATABASE_URL'] = LOCAL_DATABASE_URL

try:
    import psycopg2
    
    conn = psycopg2.connect(LOCAL_DATABASE_URL)
    cursor = conn.cursor()
    
    print("✅ Connected to local PostgreSQL")
    
    # Import the full init script
    from init_postgres_full import *
    
    # The init_postgres_full script will use the DATABASE_URL we just set
    print("🎉 Local PostgreSQL setup complete!")
    print("📋 Instrukcje:")
    print("   1. Dodaj do ~/.bashrc: export DATABASE_URL='postgresql://ikigai_user:ikigai_pass@localhost:5432/ikigai_dev'")
    print("   2. Przeładuj terminal: source ~/.bashrc")
    print("   3. Uruchom: ./start_ikigai.sh")
    
except ImportError:
    print("❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
except Exception as e:
    print(f"❌ Error: {e}")
    print("📋 Upewnij się że:")
    print("   - PostgreSQL jest zainstalowany")
    print("   - Serwis jest uruchomiony: sudo systemctl start postgresql")
    print("   - Baza ikigai_dev istnieje")
    print("   - User ikigai_user ma uprawnienia") 