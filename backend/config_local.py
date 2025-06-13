#!/usr/bin/env python3
"""
Local PostgreSQL Configuration for IKIGAI
"""

import os

# PostgreSQL Development Configuration
LOCAL_DATABASE_URL = "postgresql://ikigai_user:ikigai_pass@localhost:5432/ikigai_dev"

def setup_local_postgres():
    """Setup environment variables for local PostgreSQL"""
    os.environ['DATABASE_URL'] = LOCAL_DATABASE_URL
    os.environ['DB_TYPE'] = 'postgresql'
    print("🐘 Ustawiono lokalny PostgreSQL")
    print(f"📍 Database: {LOCAL_DATABASE_URL}")

if __name__ == "__main__":
    setup_local_postgres() 