#!/usr/bin/env python3
"""
Script to add an admin user to the database.
This is useful for initial setup on deployed environments.
"""

import os
import sys
from database import SecurityDatabase
from dotenv import load_dotenv

load_dotenv()

def add_admin():
    """Add an admin user to the database"""
    
    # Get admin user ID from environment or prompt
    admin_user_ids = os.getenv('ADMIN_USER_IDS', '')
    if admin_user_ids:
        # Take the first admin ID from the environment
        admin_id = int(admin_user_ids.split(',')[0].strip())
        print(f"Using admin ID from environment: {admin_id}")
    else:
        # Prompt for admin ID
        try:
            admin_id = int(input("Enter your Telegram User ID: "))
        except ValueError:
            print("Error: Please enter a valid numeric User ID")
            return False
    
    # Initialize database
    db_path = os.getenv('DATABASE_PATH', 'security_reports.db')
    db = SecurityDatabase(db_path)
    
    try:
        # Initialize the database (create tables if they don't exist)
        db.init_database()
        print(f"Database initialized at: {db_path}")
        
        # Add admin
        success = db.add_admin(admin_id)
        
        if success:
            print(f"✅ Successfully added admin user: {admin_id}")
            print("You can now access the Admin panel in the Mini App!")
            return True
        else:
            print(f"ℹ️  Admin user {admin_id} already exists or there was an error")
            return False
            
    except Exception as e:
        print(f"❌ Error adding admin: {e}")
        return False

if __name__ == "__main__":
    print("🛡️ Security Status Bot - Add Admin User")
    print("=" * 50)
    
    success = add_admin()
    
    if success:
        print("\n🎉 Admin user added successfully!")
        print("Now you can:")
        print("1. Access the Admin panel in the Mini App")
        print("2. Add and remove focal people")
        print("3. Manage security reports")
    else:
        print("\n❌ Failed to add admin user")
        print("Please check your configuration and try again")
