#!/usr/bin/env python3
"""
Simple setup script for Security Status Bot
"""

import os
import shutil

def main():
    print("🛡️  Security Status Bot Setup")
    print("=" * 40)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return
    
    # Copy .env.example to .env
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("\n📝 Next steps:")
        print("1. Edit the .env file with your bot token and admin user ID")
        print("2. Get bot token from @BotFather on Telegram")
        print("3. Get your user ID from @userinfobot on Telegram")
        print("4. Run: python bot.py")
    else:
        print("❌ .env.example file not found")
        return
    
    print("\n🚀 Setup complete! Edit .env file and run 'python bot.py'")

if __name__ == "__main__":
    main()
