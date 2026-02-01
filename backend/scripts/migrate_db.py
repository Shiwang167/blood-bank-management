#!/usr/bin/env python3
"""
Database Migration Script
Runs SQL migration files against PostgreSQL RDS
"""

import psycopg2
import os
import sys
from pathlib import Path

def run_migrations(database_url):
    """Execute all migration files in order"""
    
    migrations_dir = Path(__file__).parent.parent / 'migrations'
    
    if not migrations_dir.exists():
        print(f"Error: Migrations directory not found at {migrations_dir}")
        sys.exit(1)
    
    # Get all SQL files sorted by name
    migration_files = sorted(migrations_dir.glob('*.sql'))
    
    if not migration_files:
        print("No migration files found")
        return
    
    print(f"Found {len(migration_files)} migration file(s)")
    
    # Connect to database
    try:
        conn = psycopg2.connect(database_url)
        conn.autocommit = False
        cursor = conn.cursor()
        
        print(f"Connected to database successfully")
        
        # Create migrations tracking table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        # Run each migration
        for migration_file in migration_files:
            filename = migration_file.name
            
            # Check if already applied
            cursor.execute(
                "SELECT filename FROM schema_migrations WHERE filename = %s",
                (filename,)
            )
            
            if cursor.fetchone():
                print(f"⏭️  Skipping {filename} (already applied)")
                continue
            
            print(f"🔄 Applying {filename}...")
            
            try:
                # Read and execute migration
                with open(migration_file, 'r') as f:
                    sql = f.read()
                
                cursor.execute(sql)
                
                # Record migration
                cursor.execute(
                    "INSERT INTO schema_migrations (filename) VALUES (%s)",
                    (filename,)
                )
                
                conn.commit()
                print(f"✅ Applied {filename}")
                
            except Exception as e:
                conn.rollback()
                print(f"❌ Error applying {filename}: {e}")
                sys.exit(1)
        
        cursor.close()
        conn.close()
        print("\n✅ All migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("Error: DATABASE_URL environment variable not set")
        print("Usage: DATABASE_URL='postgresql://user:pass@host:5432/dbname' python migrate_db.py")
        sys.exit(1)
    
    print("=" * 60)
    print("BloodBridge Database Migration")
    print("=" * 60)
    
    run_migrations(database_url)
