# Deployment and Troubleshooting Guide

## Issues & Solutions

### Issue 1: No Push Notifications Being Sent

#### Possible Causes:
1. **Bot not running** - The Telegram bot must be running to send notifications
2. **No subscribers** - Users must subscribe via `/subscribe` command
3. **Wrong environment** - Bot token not configured

#### Solutions:

**A. Check if bot is running:**
```bash
# On Render (check worker service logs)
# Locally:
py bot.py
```

**B. Verify subscribers:**
```bash
py -c "from database import SecurityDatabase; db = SecurityDatabase('security_reports.db'); print('Subscribers:', len(db.get_all_subscribers()))"
```

**C. Subscribe to notifications:**
1. Open your Telegram bot
2. Send `/subscribe`
3. You'll receive a test notification

**D. Check environment variables:**
```bash
# Make sure BOT_TOKEN is set
echo $env:BOT_TOKEN  # Windows PowerShell
```

### Issue 2: Render Deployment Stuck on "Building"

#### Common Causes:
1. Missing dependencies
2. Wrong start command
3. Port configuration issues
4. Missing environment variables

#### Solutions:

**A. Updated render.yaml Configuration**

The render.yaml now includes:
- ✅ Proper gunicorn configuration
- ✅ Separate worker service for the bot
- ✅ Correct port binding (10000)
- ✅ Environment variables for BOT_TOKEN and ADMIN_USER_IDS

**B. Required Steps in Render Dashboard:**

1. **Add BOT_TOKEN as Secret:**
   - Go to your service in Render dashboard
   - Navigate to "Environment" tab
   - Add `BOT_TOKEN` with your actual bot token
   - Mark it as "Secret" (won't be visible in logs)

2. **Verify Services:**
   - You should see 2 services:
     - `security-status-miniapp` (Web Service) - for the Flask API
     - `security-status-bot` (Worker Service) - for the Telegram bot

3. **Check Build Logs:**
   - Click on each service
   - View "Logs" tab
   - Look for any error messages

**C. Common Render Build Issues:**

**Issue:** Build times out
```yaml
# Solution: Increase timeout
startCommand: gunicorn --bind 0.0.0.0:10000 --workers 2 --timeout 120 webapp.app:app
```

**Issue:** Port binding error
```yaml
# Solution: Use PORT environment variable
startCommand: gunicorn --bind 0.0.0.0:$PORT webapp.app:app
```

**Issue:** Module not found
```bash
# Solution: Check requirements.txt includes all dependencies
pip freeze > requirements.txt
```

## Local Testing

### Test Notifications Locally:

1. **Start the bot:**
```bash
py bot.py
```

2. **Subscribe to notifications:**
   - Open Telegram
   - Send `/subscribe` to your bot
   - Confirm you receive test notification

3. **Test report submission:**
```bash
# Via bot:
# Send /report in Telegram and follow prompts

# Via Python script:
py -c "
from database import SecurityDatabase
db = SecurityDatabase('security_reports.db')
db.add_security_report(
    location='Test Area',
    status='Testing',
    recommended_action='Test notification',
    reporter_id=994550828,
    reporter_name='Test User'
)
print('Report added! Check for notifications...')
"
```

### Test Web App Locally:

```bash
# Start Flask app
py webapp/app.py

# Test API endpoint
curl http://localhost:5000/health
```

## Render Deployment Checklist

Before deploying:
- [ ] BOT_TOKEN added as secret in Render dashboard
- [ ] ADMIN_USER_IDS configured
- [ ] requirements.txt includes all dependencies
- [ ] render.yaml has both web and worker services
- [ ] Database path configured correctly
- [ ] Port 10000 used for web service

After deployment:
- [ ] Web service is "Live"
- [ ] Worker service is "Running"
- [ ] Health check endpoint works: `https://your-app.onrender.com/health`
- [ ] Bot responds to commands in Telegram
- [ ] Notifications are being sent

## Debugging Commands

### Check Database:
```bash
py -c "
from database import SecurityDatabase
db = SecurityDatabase('security_reports.db')
print('Subscribers:', db.get_all_subscribers())
print('Admins:', db.get_all_admins())
print('Reports:', len(db.get_latest_reports(100)))
"
```

### Test Notification Service:
```bash
py -c "
import asyncio
import os
from notifications import NotificationService
from database import SecurityDatabase

# Load .env
from dotenv import load_dotenv
load_dotenv()

db = SecurityDatabase('security_reports.db')
notif = NotificationService(os.getenv('BOT_TOKEN'), db)

async def test():
    result = await notif.send_test_notification(994550828)
    print('Test notification sent:', result)

asyncio.run(test())
"
```

### Check Environment:
```bash
py -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('BOT_TOKEN set:', 'Yes' if os.getenv('BOT_TOKEN') else 'No')
print('ADMIN_USER_IDS:', os.getenv('ADMIN_USER_IDS'))
print('DATABASE_PATH:', os.getenv('DATABASE_PATH', 'security_reports.db'))
"
```

## Common Error Messages

### "Event loop is closed"
**Cause:** Async issues in Flask
**Solution:** Already fixed in webapp/app.py with threading approach

### "No subscribers to notify"
**Cause:** No users subscribed
**Solution:** Run `/subscribe` command in Telegram bot

### "Failed to send admin alert"
**Cause:** Bot token invalid or user blocked bot
**Solution:** 
- Verify BOT_TOKEN is correct
- Make sure you haven't blocked the bot in Telegram
- Check bot is running

### "Port already in use"
**Cause:** Another process using the port
**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
# Kill the process using the port
```

## Support

If issues persist:
1. Check Render logs for specific error messages
2. Verify all environment variables are set
3. Test locally first before deploying
4. Ensure bot is subscribed to notifications
5. Check that both web and worker services are running on Render

## Quick Fix Commands

```bash
# Restart everything locally
py bot.py

# Subscribe yourself
py subscribe_user.py

# Test a notification
py -c "from database import SecurityDatabase; db = SecurityDatabase('security_reports.db'); db.add_security_report('Test', 'Alert', 'Test action', 994550828, 'Admin')"

# Check logs
py bot.py > bot_logs.txt 2>&1
```

