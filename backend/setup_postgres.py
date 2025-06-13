#!/usr/bin/env python3
"""
Setup PostgreSQL database for IKIGAI on Heroku
"""
import os

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("❌ DATABASE_URL not found. Run this on Heroku or set the variable locally.")
    exit(1)

# Fix postgres:// to postgresql:// for psycopg2
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print("🐘 Setting up PostgreSQL for IKIGAI...")

try:
    import psycopg2
    
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("✅ Connected to PostgreSQL")
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(50),
            loyalty_level INTEGER DEFAULT 1,
            loyalty_points INTEGER DEFAULT 0,
            total_orders INTEGER DEFAULT 0,
            total_spent DECIMAL(10,2) DEFAULT 0.00,
            password_hash VARCHAR(255),
            role VARCHAR(50) DEFAULT 'user',
            is_active BOOLEAN DEFAULT TRUE,
            member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            favorite_recipe_id VARCHAR(50)
        );
    """)
    
    print("✅ Users table created")
    
    # Insert demo user with loyalty points
    cursor.execute("""
        INSERT INTO users (id, name, email, loyalty_points, total_orders, total_spent, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            loyalty_points = EXCLUDED.loyalty_points,
            total_orders = EXCLUDED.total_orders,
            total_spent = EXCLUDED.total_spent
    """, ('web_user', 'Demo User IKIGAI', 'demo@ikigai.com', 2847, 15, 247.50, 'user'))
    
    # Insert admin user
    cursor.execute("""
        INSERT INTO users (id, name, email, loyalty_points, role)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, ('admin', 'Administrator IKIGAI', 'admin@ikigai.com', 10000, 'admin'))
    
    conn.commit()
    print("✅ Sample users inserted")
    
    # Test the setup
    cursor.execute("SELECT id, name, loyalty_points FROM users")
    users = cursor.fetchall()
    print("\n👥 Users in database:")
    for user in users:
        print(f"  - {user[1]} ({user[0]}): {user[2]} points")
    
    conn.close()
    print("\n🎉 PostgreSQL setup complete!")
    
except ImportError:
    print("❌ psycopg2 not installed. Add 'psycopg2-binary' to requirements.txt")
except Exception as e:
    print(f"❌ Error setting up PostgreSQL: {e}") 