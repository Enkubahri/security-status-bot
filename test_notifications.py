#!/usr/bin/env python
"""
Test script to verify push notification system
"""
import os
import sys
import asyncio
from database import SecurityDatabase
from notifications import NotificationService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("🧪 Testing Push Notification System\n")
    print("=" * 50)
    
    # Check environment
    print("\n1️⃣ Checking Environment Variables...")
    bot_token = os.getenv('BOT_TOKEN')
    if bot_token:
        print(f"   ✅ BOT_TOKEN is set (length: {len(bot_token)})")
    else:
        print("   ❌ BOT_TOKEN is NOT set!")
        print("   ➡️  Create a .env file with BOT_TOKEN=your_bot_token")
        return False
    
    admin_ids = os.getenv('ADMIN_USER_IDS', '')
    print(f"   ✅ ADMIN_USER_IDS: {admin_ids}")
    
    # Check database
    print("\n2️⃣ Checking Database...")
    db = SecurityDatabase('security_reports.db')
    
    subscribers = db.get_all_subscribers()
    admins = db.get_all_admins()
    reports = db.get_latest_reports(5)
    
    print(f"   📊 Subscribers: {len(subscribers)}")
    if subscribers:
        for user_id, name in subscribers:
            print(f"      - {name} (ID: {user_id})")
    else:
        print("      ⚠️  No subscribers! Run /subscribe in Telegram or run subscribe_user.py")
    
    print(f"   👑 Admins: {len(admins)}")
    for admin_id in admins:
        print(f"      - ID: {admin_id}")
    
    print(f"   📝 Recent Reports: {len(reports)}")
    
    if not subscribers and not admins:
        print("\n   ❌ No subscribers or admins! Notifications won't be sent.")
        print("   ➡️  Run: py subscribe_user.py")
        return False
    
    # Test notification service
    print("\n3️⃣ Testing Notification Service...")
    notif_service = NotificationService(bot_token, db)
    
    # Send test notification
    print("   📤 Sending test notification...")
    
    async def send_test():
        if subscribers:
            user_id = subscribers[0][0]  # First subscriber
            result = await notif_service.send_test_notification(user_id)
            return result
        elif admins:
            result = await notif_service.send_test_notification(admins[0])
            return result
        return False
    
    try:
        result = asyncio.run(send_test())
        if result:
            print("   ✅ Test notification sent successfully!")
            print("   📱 Check your Telegram for the message")
        else:
            print("   ❌ Failed to send test notification")
            print("   ➡️  Make sure:")
            print("      1. Bot is running (py bot.py)")
            print("      2. You haven't blocked the bot in Telegram")
            print("      3. BOT_TOKEN is correct")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test with a fake security report
    print("\n4️⃣ Testing Security Alert...")
    print("   📝 Creating test security report...")
    
    success = db.add_security_report(
        location="Test Location",
        status="Testing notifications",
        recommended_action="Check your Telegram for notification",
        reporter_id=994550828,
        reporter_name="Test System"
    )
    
    if success:
        print("   ✅ Test report created in database")
        print("   ⚠️  Note: Notifications are only sent when bot.py is running")
        print("   ➡️  Start the bot with: py bot.py")
    else:
        print("   ❌ Failed to create test report")
        return False
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"✅ Environment configured: Yes")
    print(f"✅ Database accessible: Yes")
    print(f"✅ Subscribers: {len(subscribers)}")
    print(f"✅ Admins: {len(admins)}")
    print(f"✅ Notification service: Working")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Make sure bot is running: py bot.py")
    print("2. Subscribe to notifications: /subscribe in Telegram")
    print("3. Test by submitting a report: /report in Telegram")
    print("4. You should receive 2 notifications (subscriber + admin)")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

