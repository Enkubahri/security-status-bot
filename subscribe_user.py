#!/usr/bin/env python
"""
Quick script to manually subscribe a user to security alert notifications
"""
import sys
from database import SecurityDatabase

# Initialize database
db = SecurityDatabase('security_reports.db')

# Your user details
user_id = 994550828  # Your Telegram user ID
user_name = "Admin User"  # Your name

# Add subscriber
success = db.add_subscriber(user_id, user_name)

if success:
    print(f"✅ Successfully subscribed user {user_id} ({user_name}) to notifications!")
    
    # Verify subscription
    if db.is_subscriber(user_id):
        print("✅ Subscription verified!")
    else:
        print("❌ Verification failed!")
    
    # Show all subscribers
    subscribers = db.get_all_subscribers()
    print(f"\n📋 Total subscribers: {len(subscribers)}")
    for sub_id, sub_name in subscribers:
        print(f"  - {sub_name} (ID: {sub_id})")
else:
    print("❌ Failed to subscribe user!")
    sys.exit(1)

