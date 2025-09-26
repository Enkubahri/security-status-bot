#!/usr/bin/env python3
"""
Test script to verify admin functionality
"""

import os
from dotenv import load_dotenv
from database import SecurityDatabase

def test_admin_setup():
    # Load environment variables
    load_dotenv()
    
    # Get admin IDs from environment
    admin_ids_str = os.getenv('ADMIN_USER_IDS', '')
    bot_token = os.getenv('BOT_TOKEN', '')
    
    print("🔍 Admin Configuration Test")
    print("=" * 40)
    
    # Check bot token
    if bot_token:
        print(f"✅ Bot token configured: {bot_token[:20]}...")
    else:
        print("❌ Bot token NOT configured!")
        return
    
    # Check admin IDs
    if admin_ids_str:
        print(f"✅ Admin IDs configured: {admin_ids_str}")
        admin_ids = admin_ids_str.split(',')
        admin_ids = [int(aid.strip()) for aid in admin_ids if aid.strip().isdigit()]
        print(f"✅ Parsed admin IDs: {admin_ids}")
    else:
        print("❌ Admin IDs NOT configured!")
        return
    
    # Test database
    try:
        db = SecurityDatabase()
        print("✅ Database connection successful")
        
        # Add admin users
        for admin_id in admin_ids:
            db.add_admin(admin_id)
            print(f"✅ Added admin ID: {admin_id}")
        
        # Test admin check
        for admin_id in admin_ids:
            is_admin = db.is_admin(admin_id)
            print(f"✅ Admin check for {admin_id}: {is_admin}")
        
        # Test with a non-admin ID
        test_id = 999999999
        is_admin = db.is_admin(test_id)
        print(f"✅ Non-admin check for {test_id}: {is_admin}")
        
        # List current focal people
        focal_people = db.get_all_focal_people()
        print(f"📋 Current focal people: {len(focal_people)}")
        for fp in focal_people:
            print(f"  - ID: {fp[0]}, Name: {fp[1]}")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return
    
    print("\n🎯 Test Complete! If you see all ✅ marks, the admin system should work.")
    print(f"Your admin User ID is: {admin_ids[0]} (use this to test /addfocal)")

if __name__ == "__main__":
    test_admin_setup()
