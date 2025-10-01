# Push Notifications Feature

## Overview

The Security Status Bot now includes a comprehensive push notification system that sends instant alerts to subscribers whenever a new security report is submitted. This ensures that community members can stay informed about security conditions in real-time.

## Features

### 🔔 Automatic Notifications
- **Instant Alerts**: All subscribers receive push notifications immediately when a security report is submitted
- **Admin Notifications**: Administrators receive special notifications with additional report details
- **Multi-Channel Support**: Notifications work for reports submitted via both the Telegram bot and the web app

### 📱 User Subscription Management
Users can easily manage their notification preferences:
- `/subscribe` - Subscribe to security alert notifications
- `/unsubscribe` - Unsubscribe from notifications
- Automatic test notification sent upon subscription to verify delivery

### 🔐 Security
- Only authorized focal people can submit reports (which trigger notifications)
- Admins receive additional context about who submitted each report
- Graceful error handling if users have blocked the bot

## How It Works

### For Users

1. **Subscribe to Notifications**
   ```
   /subscribe
   ```
   - You'll receive a test notification to confirm your subscription
   - You'll get instant alerts whenever new security reports are submitted

2. **Unsubscribe from Notifications**
   ```
   /unsubscribe
   ```
   - You'll stop receiving security alert notifications
   - You can re-subscribe at any time

### For Focal People (Report Submitters)

When you submit a security report:
1. The report is saved to the database
2. Push notifications are automatically sent to:
   - All subscribed users (with report details)
   - All administrators (with additional reporter information)

### Notification Content

**Subscriber Alert:**
```
🚨 SECURITY ALERT

📍 Location: [Location Name]
⚠️ Status: [Security Status]
💡 Recommended Action: [Action to Take]
👤 Reported by: [Reporter Name]
🕐 Time: [Timestamp]

⚡ This is an automated security notification. Stay safe and follow recommended actions.

Use /status to view all recent reports
Use /location [Location Name] for updates on this location
```

**Admin Alert:**
```
🔔 ADMIN NOTIFICATION: New Security Report

📍 Location: [Location Name]
⚠️ Status: [Security Status]
💡 Recommended Action: [Action to Take]
👤 Reported by: [Reporter Name] (ID: [Reporter ID])
🕐 Time: [Timestamp]

This report has been automatically distributed to all subscribers.
```

## Technical Implementation

### Architecture

The push notification system consists of:

1. **NotificationService** (`notifications.py`)
   - Manages sending notifications via Telegram Bot API
   - Handles subscriber list retrieval
   - Logs delivery success/failure

2. **Database Support** (`database.py`)
   - New `subscribers` table for managing notification subscriptions
   - Methods: `add_subscriber()`, `remove_subscriber()`, `get_all_subscribers()`
   - Methods: `is_subscriber()`, `get_all_admins()`

3. **Bot Integration** (`bot.py`)
   - Integrated into the report submission flow
   - New `/subscribe` and `/unsubscribe` commands
   - Async notification sending after report submission

4. **Web App Integration** (`webapp/app.py`)
   - Notifications sent when reports are submitted via API
   - Uses asyncio for non-blocking notification delivery

### Database Schema

New table added to support subscriptions:

```sql
CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_user_id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    subscribed_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
)
```

### API Methods

#### NotificationService Methods

- `send_security_alert(location, status, recommended_action, reporter_name, report_id=None)`
  - Sends alerts to all subscribed users
  - Returns dict with success/failure counts

- `send_admin_alert(location, status, recommended_action, reporter_name, reporter_id)`
  - Sends alerts to all administrators
  - Includes additional context for admins

- `send_test_notification(user_id)`
  - Sends a test notification to verify delivery
  - Used when users subscribe

## Usage Examples

### Example: User Subscribing
```
User: /subscribe
Bot: 🔔 Successfully subscribed to security alerts!

     You will now receive push notifications whenever a new security report is submitted.
     
     ✅ A test notification was sent to confirm your subscription.
     
     Use /unsubscribe anytime to stop receiving notifications.
```

### Example: Security Report Notification
When a focal person submits a report about "Downtown Area" with status "High alert", all subscribers instantly receive:

```
🚨 SECURITY ALERT

📍 Location: Downtown Area
⚠️ Status: High alert
💡 Recommended Action: Avoid the area until further notice
👤 Reported by: John Doe
🕐 Time: 2025-10-01 14:30

⚡ This is an automated security notification. Stay safe and follow recommended actions.

Use /status to view all recent reports
Use /location Downtown Area for updates on this location
```

## Benefits

✅ **Real-time Awareness**: Community members receive instant notifications
✅ **Opt-in System**: Users choose whether to receive notifications
✅ **Comprehensive Coverage**: Works across bot and web app
✅ **Admin Oversight**: Administrators receive additional context
✅ **Error Handling**: Gracefully handles delivery failures
✅ **Testing**: Built-in test notification on subscription

## Error Handling

The system includes robust error handling:
- Failed deliveries are logged but don't block report submission
- Users who have blocked the bot are identified in logs
- The system continues even if notification service is unavailable
- Each notification attempt is independent (one failure doesn't affect others)

## Future Enhancements

Potential improvements for future versions:
- Location-based subscriptions (subscribe to specific areas)
- Notification preferences (customize alert types)
- Digest mode (daily/weekly summaries instead of instant alerts)
- Mobile push notifications via Firebase/APNs
- SMS notifications for critical alerts
- Email notifications as backup channel

## Support

If you experience issues with notifications:
1. Ensure you haven't blocked the bot
2. Check your Telegram notification settings
3. Try unsubscribing and resubscribing
4. Contact an administrator if problems persist

## Commands Summary

| Command | Description | Who Can Use |
|---------|-------------|-------------|
| `/subscribe` | Subscribe to security alerts | All users |
| `/unsubscribe` | Unsubscribe from alerts | All users |
| `/report` | Submit security report (triggers notifications) | Focal people only |

---

**Note**: Push notifications are automatically triggered when security reports are submitted. There is no need to manually send notifications - the system handles this automatically.

