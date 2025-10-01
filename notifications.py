import logging
from typing import List, Optional
from telegram import Bot
from telegram.constants import ParseMode
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for sending push notifications about security updates"""
    
    def __init__(self, bot_token: str, database):
        """
        Initialize the notification service
        
        Args:
            bot_token: Telegram bot token for sending messages
            database: SecurityDatabase instance
        """
        self.bot = Bot(token=bot_token)
        self.db = database
    
    async def send_security_alert(
        self, 
        location: str, 
        status: str, 
        recommended_action: str,
        reporter_name: str,
        report_id: Optional[int] = None
    ) -> dict:
        """
        Send push notification to all subscribers about a new security report
        
        Args:
            location: Location of the security incident
            status: Current security status
            recommended_action: Recommended action to take
            reporter_name: Name of the person who reported
            report_id: Database ID of the report (optional)
        
        Returns:
            dict with success count and failed deliveries
        """
        # Get all subscribers
        subscribers = self.db.get_all_subscribers()
        
        if not subscribers:
            logger.info("No subscribers to notify")
            return {"success": 0, "failed": 0}
        
        # Format the alert message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        alert_message = f"""
🚨 **SECURITY ALERT**

📍 **Location:** {location}
⚠️ **Status:** {status}
💡 **Recommended Action:** {recommended_action}
👤 **Reported by:** {reporter_name}
🕐 **Time:** {timestamp}

⚡ This is an automated security notification. Stay safe and follow recommended actions.

Use /status to view all recent reports
Use /location {location} for updates on this location
        """
        
        success_count = 0
        failed_count = 0
        failed_users = []
        
        # Send notification to each subscriber
        for subscriber_id, subscriber_name in subscribers:
            try:
                await self.bot.send_message(
                    chat_id=subscriber_id,
                    text=alert_message,
                    parse_mode=ParseMode.MARKDOWN
                )
                success_count += 1
                logger.info(f"Security alert sent to {subscriber_name} (ID: {subscriber_id})")
            except Exception as e:
                failed_count += 1
                failed_users.append((subscriber_id, subscriber_name))
                logger.error(f"Failed to send alert to {subscriber_name} (ID: {subscriber_id}): {e}")
        
        # Log summary
        logger.info(
            f"Security alert delivery complete: "
            f"{success_count} successful, {failed_count} failed"
        )
        
        # Optionally deactivate subscribers who have blocked the bot
        if failed_users:
            for user_id, user_name in failed_users:
                logger.warning(f"User {user_name} (ID: {user_id}) may have blocked the bot")
        
        return {
            "success": success_count,
            "failed": failed_count,
            "failed_users": failed_users
        }
    
    async def send_admin_alert(
        self,
        location: str,
        status: str,
        recommended_action: str,
        reporter_name: str,
        reporter_id: int
    ) -> dict:
        """
        Send push notification specifically to admins about a new security report
        
        Args:
            location: Location of the security incident
            status: Current security status
            recommended_action: Recommended action to take
            reporter_name: Name of the person who reported
            reporter_id: Telegram ID of the reporter
        
        Returns:
            dict with success count and failed deliveries
        """
        # Get all admins
        admins = self.db.get_all_admins()
        
        if not admins:
            logger.info("No admins to notify")
            return {"success": 0, "failed": 0}
        
        # Format the admin alert message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        admin_message = f"""
🔔 **ADMIN NOTIFICATION: New Security Report**

📍 **Location:** {location}
⚠️ **Status:** {status}
💡 **Recommended Action:** {recommended_action}
👤 **Reported by:** {reporter_name} (ID: {reporter_id})
🕐 **Time:** {timestamp}

This report has been automatically distributed to all subscribers.
        """
        
        success_count = 0
        failed_count = 0
        
        # Send notification to each admin
        for admin_id in admins:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=admin_message,
                    parse_mode=ParseMode.MARKDOWN
                )
                success_count += 1
                logger.info(f"Admin alert sent to admin ID: {admin_id}")
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to send admin alert to ID {admin_id}: {e}")
        
        return {
            "success": success_count,
            "failed": failed_count
        }
    
    async def send_test_notification(self, user_id: int) -> bool:
        """
        Send a test notification to verify the user can receive messages
        
        Args:
            user_id: Telegram user ID to send test message to
        
        Returns:
            True if successful, False otherwise
        """
        try:
            test_message = """
✅ **Test Notification**

You will now receive security alerts for new reports.

This is a test message to confirm your subscription is active.
            """
            
            await self.bot.send_message(
                chat_id=user_id,
                text=test_message,
                parse_mode=ParseMode.MARKDOWN
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send test notification to {user_id}: {e}")
            return False

