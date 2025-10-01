import os
import logging
import re
from datetime import datetime
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)
from telegram.constants import ParseMode
from dotenv import load_dotenv

from database import SecurityDatabase
from admin_handlers import AdminHandlers, ADD_FOCAL_ID, ADD_FOCAL_NAME, REMOVE_FOCAL_ID
from notifications import NotificationService

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
REPORT_LOCATION, REPORT_STATUS, REPORT_ACTION = range(3)
ADD_FOCAL_LOCATION, ADD_FOCAL_NAME = range(2)

class SecurityBot:
    def __init__(self):
        self.db = SecurityDatabase(os.getenv('DATABASE_PATH', 'security_reports.db'))
        self.token = os.getenv('BOT_TOKEN')
        
        # Initialize admin users from environment
        admin_ids = os.getenv('ADMIN_USER_IDS', '').split(',')
        for admin_id in admin_ids:
            if admin_id.strip().isdigit():
                self.db.add_admin(int(admin_id.strip()))
        
        # Initialize notification service
        self.notification_service = NotificationService(self.token, self.db)
        
        self.application = None
        self.user_data: Dict[int, Dict[str, Any]] = {}
        self.admin_handlers = AdminHandlers(self.db, self.user_data)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        welcome_msg = """
🛡️ **Security Status Bot**

Welcome! This bot helps community members stay informed about security conditions in different areas.

**🚀 NEW: Mini App Available!**
Use /app to open the modern web interface with better features!

**Available Commands:**
🌐 /app - Open Security Status Mini App (Recommended)
📊 /status - View recent security reports
🔍 /location <area> - Get security status for specific location
📝 /report - Submit a security report (focal people only)
🔔 /subscribe - Subscribe to security alert notifications
🔕 /unsubscribe - Unsubscribe from notifications
👥 /addfocal - Add focal person (admins only)
📋 /listfocal - List all focal people (admins only)
❌ /removefocal - Remove focal person (admins only)
ℹ️ /help - Show this help message

**For Best Experience:**
Use the Mini App (/app) for enhanced interface, real-time updates, and better mobile experience.
        """
        
        # Create inline keyboard with Mini App button
        keyboard = [
            [
                InlineKeyboardButton(
                    "🌐 Open Security Status App",
                    web_app=WebAppInfo(url="https://your-domain.com")  # You'll need to replace this
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_msg,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def app_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Launch the Mini App."""
        keyboard = [
            [
                InlineKeyboardButton(
                    "🌐 Open Security Status App",
                    web_app=WebAppInfo(url="https://your-domain.com")  # Replace with your domain
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🚀 **Launch Security Status Mini App**\n\n"
            "Click the button below to open the modern web interface with:\n"
            "• Interactive forms\n"
            "• Real-time search and filtering\n"
            "• Better mobile experience\n"
            "• Admin panel for authorized users\n\n"
            "The Mini App provides all the same functionality as the bot commands, but with a much better user experience!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send help message."""
        await self.start(update, context)

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show recent security reports."""
        reports = self.db.get_latest_reports(10)
        
        if not reports:
            await update.message.reply_text(
                "📋 No security reports available at the moment."
            )
            return

        message = "🛡️ **Latest Security Reports:**\n\n"
        
        for i, (location, status, action, reporter, timestamp) in enumerate(reports, 1):
            # Parse timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%Y-%m-%d %H:%M')
            except:
                time_str = timestamp
            
            message += f"**{i}. {location}**\n"
            message += f"🚨 Status: {status}\n"
            message += f"💡 Action: {action}\n"
            message += f"👤 Reported by: {reporter}\n"
            message += f"🕐 Time: {time_str}\n\n"
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN
        )

    async def location_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show security reports for a specific location."""
        if not context.args:
            await update.message.reply_text(
                "Please specify a location. Usage: /location <area name>"
            )
            return
        
        location = ' '.join(context.args)
        reports = self.db.get_reports_by_location(location, 5)
        
        if not reports:
            await update.message.reply_text(
                f"📍 No security reports found for '{location}'"
            )
            return

        message = f"🛡️ **Security Reports for '{location}':**\n\n"
        
        for i, (loc, status, action, reporter, timestamp) in enumerate(reports, 1):
            # Parse timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%Y-%m-%d %H:%M')
            except:
                time_str = timestamp
            
            message += f"**{i}. {loc}**\n"
            message += f"🚨 Status: {status}\n"
            message += f"💡 Action: {action}\n"
            message += f"👤 Reported by: {reporter}\n"
            message += f"🕐 Time: {time_str}\n\n"
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN
        )

    # Security Report Conversation Handlers
    async def start_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the security report conversation."""
        user_id = update.effective_user.id
        
        # Check if user is a focal person
        if not self.db.is_focal_person(user_id):
            await update.message.reply_text(
                "🚫 Sorry, only authorized focal people can submit security reports. "
                "Please contact an administrator to get focal person access."
            )
            return ConversationHandler.END
        
        # Initialize user data
        self.user_data[user_id] = {}
        
        await update.message.reply_text(
            "📝 **Submit Security Report**\n\n"
            "Please provide the location/area name:"
        )
        
        return REPORT_LOCATION

    async def report_location(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle location input for security report."""
        user_id = update.effective_user.id
        location = update.message.text.strip()
        
        # Validate location (alphabets only as per rule)
        if not re.match(r'^[a-zA-Z\s]+$', location):
            await update.message.reply_text(
                "❌ Location must contain only alphabets and spaces. Please try again:"
            )
            return REPORT_LOCATION
        
        self.user_data[user_id]['location'] = location
        
        await update.message.reply_text(
            f"📍 Location: {location}\n\n"
            "Now, please describe the security status:"
        )
        
        return REPORT_STATUS

    async def report_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle status input for security report."""
        user_id = update.effective_user.id
        status = update.message.text.strip()
        
        self.user_data[user_id]['status'] = status
        
        await update.message.reply_text(
            f"🚨 Status: {status}\n\n"
            "Finally, please provide the recommended action:"
        )
        
        return REPORT_ACTION

    async def report_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle recommended action input and save the report."""
        user_id = update.effective_user.id
        action = update.message.text.strip()
        
        # Get user info
        user = update.effective_user
        reporter_name = user.full_name or user.username or f"User{user_id}"
        
        # Save the report
        location = self.user_data[user_id]['location']
        status = self.user_data[user_id]['status']
        
        success = self.db.add_security_report(
            location=location,
            status=status,
            recommended_action=action,
            reporter_id=user_id,
            reporter_name=reporter_name
        )
        
        if success:
            # Send confirmation
            confirmation = f"""
✅ **Security Report Submitted Successfully!**

📍 **Location:** {location}
🚨 **Status:** {status}
💡 **Recommended Action:** {action}
👤 **Reporter:** {reporter_name}
🕐 **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

The report has been added to the database and is now visible to all group members.
            """
            
            await update.message.reply_text(
                confirmation,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Send push notifications to subscribers and admins
            try:
                # Send to all subscribers
                notification_result = await self.notification_service.send_security_alert(
                    location=location,
                    status=status,
                    recommended_action=action,
                    reporter_name=reporter_name
                )
                
                # Send to admins
                admin_result = await self.notification_service.send_admin_alert(
                    location=location,
                    status=status,
                    recommended_action=action,
                    reporter_name=reporter_name,
                    reporter_id=user_id
                )
                
                logger.info(
                    f"Notifications sent: {notification_result['success']} subscribers, "
                    f"{admin_result['success']} admins"
                )
            except Exception as e:
                logger.error(f"Error sending notifications: {e}")
        else:
            await update.message.reply_text(
                "❌ There was an error saving your report. Please try again later."
            )
        
        # Clear user data
        if user_id in self.user_data:
            del self.user_data[user_id]
        
        return ConversationHandler.END

    async def cancel_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel the security report conversation."""
        user_id = update.effective_user.id
        
        # Clear user data
        if user_id in self.user_data:
            del self.user_data[user_id]
        
        await update.message.reply_text(
            "❌ Security report submission cancelled."
        )
        
        return ConversationHandler.END
    
    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Subscribe to security alert notifications."""
        user_id = update.effective_user.id
        user = update.effective_user
        user_name = user.full_name or user.username or f"User{user_id}"
        
        # Check if already subscribed
        if self.db.is_subscriber(user_id):
            await update.message.reply_text(
                "✅ You are already subscribed to security alerts!\n\n"
                "You will receive push notifications whenever a new security report is submitted.\n\n"
                "Use /unsubscribe to stop receiving notifications."
            )
            return
        
        # Add subscriber to database
        success = self.db.add_subscriber(user_id, user_name)
        
        if success:
            # Send test notification
            test_sent = await self.notification_service.send_test_notification(user_id)
            
            if test_sent:
                await update.message.reply_text(
                    "🔔 **Successfully subscribed to security alerts!**\n\n"
                    "You will now receive push notifications whenever a new security report is submitted.\n\n"
                    "✅ A test notification was sent to confirm your subscription.\n\n"
                    "Use /unsubscribe anytime to stop receiving notifications."
                )
            else:
                await update.message.reply_text(
                    "🔔 **Successfully subscribed to security alerts!**\n\n"
                    "You will now receive push notifications whenever a new security report is submitted.\n\n"
                    "⚠️ Note: Please make sure you haven't blocked this bot.\n\n"
                    "Use /unsubscribe anytime to stop receiving notifications."
                )
        else:
            await update.message.reply_text(
                "❌ There was an error processing your subscription. Please try again later."
            )
    
    async def unsubscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Unsubscribe from security alert notifications."""
        user_id = update.effective_user.id
        
        # Check if subscribed
        if not self.db.is_subscriber(user_id):
            await update.message.reply_text(
                "❌ You are not currently subscribed to security alerts.\n\n"
                "Use /subscribe to start receiving notifications."
            )
            return
        
        # Remove subscriber from database
        success = self.db.remove_subscriber(user_id)
        
        if success:
            await update.message.reply_text(
                "🔕 **Successfully unsubscribed from security alerts.**\n\n"
                "You will no longer receive push notifications for new security reports.\n\n"
                "Use /subscribe anytime to start receiving notifications again."
            )
        else:
            await update.message.reply_text(
                "❌ There was an error processing your unsubscription. Please try again later."
            )

    def setup_handlers(self):
        """Set up all command and message handlers."""
        # Basic commands
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("app", self.app_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("location", self.location_command))
        
        # Subscription commands
        self.application.add_handler(CommandHandler("subscribe", self.subscribe_command))
        self.application.add_handler(CommandHandler("unsubscribe", self.unsubscribe_command))
        
        # Security report conversation
        report_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("report", self.start_report)],
            states={
                REPORT_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.report_location)],
                REPORT_STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.report_status)],
                REPORT_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.report_action)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel_report)],
        )
        
        self.application.add_handler(report_conv_handler)
        
        # Admin commands
        self.application.add_handler(CommandHandler("listfocal", self.admin_handlers.list_focal))
        
        # Add focal person conversation
        add_focal_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("addfocal", self.admin_handlers.add_focal_start)],
            states={
                ADD_FOCAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.admin_handlers.add_focal_id)],
                ADD_FOCAL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.admin_handlers.add_focal_name)],
            },
            fallbacks=[CommandHandler("cancel", self.admin_handlers.cancel_admin_action)],
        )
        
        self.application.add_handler(add_focal_conv_handler)
        
        # Remove focal person conversation
        remove_focal_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("removefocal", self.admin_handlers.remove_focal_start)],
            states={
                REMOVE_FOCAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.admin_handlers.remove_focal_id)],
            },
            fallbacks=[CommandHandler("cancel", self.admin_handlers.cancel_admin_action)],
        )
        
        self.application.add_handler(remove_focal_conv_handler)

    def run(self):
        """Start the bot."""
        if not self.token:
            logger.error("BOT_TOKEN not found in environment variables!")
            return
        
        # Create the Application
        self.application = Application.builder().token(self.token).build()
        
        # Set up handlers
        self.setup_handlers()
        
        logger.info("Starting Security Status Bot...")
        
        # Run the bot
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    bot = SecurityBot()
    bot.run()
