import re
from datetime import datetime
from typing import Dict, Any

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode

# Conversation states for admin functions
ADD_FOCAL_ID, ADD_FOCAL_NAME = range(2)
REMOVE_FOCAL_ID = 0

class AdminHandlers:
    def __init__(self, db, user_data: Dict[int, Dict[str, Any]]):
        self.db = db
        self.user_data = user_data

    async def add_focal_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the add focal person conversation."""
        user_id = update.effective_user.id
        print(f"DEBUG: add_focal_start called by user {user_id}")
        
        # Check if user is admin
        is_admin = self.db.is_admin(user_id)
        print(f"DEBUG: User {user_id} admin check: {is_admin}")
        
        if not is_admin:
            await update.message.reply_text(
                "🚫 Sorry, only administrators can add focal people."
            )
            return ConversationHandler.END
        
        # Initialize user data
        self.user_data[user_id] = {}
        
        await update.message.reply_text(
            "👥 **Add Focal Person**\n\n"
            "Please provide the Telegram User ID of the person to add as focal person.\n"
            "You can get this by forwarding a message from them or asking them to send /start to this bot."
        )
        
        return ADD_FOCAL_ID

    async def add_focal_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle user ID input for adding focal person."""
        user_id = update.effective_user.id
        focal_id_text = update.message.text.strip()
        
        # Validate user ID is numeric
        if not focal_id_text.isdigit():
            await update.message.reply_text(
                "❌ Please provide a valid numeric Telegram User ID."
            )
            return ADD_FOCAL_ID
        
        focal_id = int(focal_id_text)
        self.user_data[user_id]['focal_id'] = focal_id
        
        await update.message.reply_text(
            f"👤 User ID: {focal_id}\n\n"
            "Now, please provide the full name for this focal person:"
        )
        
        return ADD_FOCAL_NAME

    async def add_focal_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle name input and complete focal person addition."""
        user_id = update.effective_user.id
        name = update.message.text.strip()
        
        # Validate name (alphabets only as per rule)
        if not re.match(r'^[a-zA-Z\s]+$', name):
            await update.message.reply_text(
                "❌ Name must contain only alphabets and spaces. Please try again:"
            )
            return ADD_FOCAL_NAME
        
        focal_id = self.user_data[user_id]['focal_id']
        
        # Add focal person to database
        success = self.db.add_focal_person(focal_id, name, user_id)
        
        if success:
            await update.message.reply_text(
                f"✅ **Focal Person Added Successfully!**\n\n"
                f"👤 **Name:** {name}\n"
                f"🆔 **User ID:** {focal_id}\n"
                f"📅 **Added:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                f"This person can now submit security reports using the /report command.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "❌ There was an error adding the focal person. They may already exist in the system."
            )
        
        # Clear user data
        if user_id in self.user_data:
            del self.user_data[user_id]
        
        return ConversationHandler.END

    async def list_focal(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """List all focal people."""
        user_id = update.effective_user.id
        
        # Check if user is admin
        if not self.db.is_admin(user_id):
            await update.message.reply_text(
                "🚫 Sorry, only administrators can view the focal people list."
            )
            return
        
        focal_people = self.db.get_all_focal_people()
        
        if not focal_people:
            await update.message.reply_text(
                "📋 No focal people are currently registered."
            )
            return
        
        message = "👥 **Authorized Focal People:**\n\n"
        
        for i, (focal_id, name, added_date) in enumerate(focal_people, 1):
            try:
                dt = datetime.fromisoformat(added_date.replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d')
            except:
                date_str = added_date
            
            message += f"**{i}. {name}**\n"
            message += f"🆔 User ID: `{focal_id}`\n"
            message += f"📅 Added: {date_str}\n\n"
        
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN
        )

    async def remove_focal_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the remove focal person conversation."""
        user_id = update.effective_user.id
        
        # Check if user is admin
        if not self.db.is_admin(user_id):
            await update.message.reply_text(
                "🚫 Sorry, only administrators can remove focal people."
            )
            return ConversationHandler.END
        
        await update.message.reply_text(
            "❌ **Remove Focal Person**\n\n"
            "Please provide the Telegram User ID of the focal person to remove:"
        )
        
        return REMOVE_FOCAL_ID

    async def remove_focal_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle user ID input for removing focal person."""
        focal_id_text = update.message.text.strip()
        
        # Validate user ID is numeric
        if not focal_id_text.isdigit():
            await update.message.reply_text(
                "❌ Please provide a valid numeric Telegram User ID."
            )
            return REMOVE_FOCAL_ID
        
        focal_id = int(focal_id_text)
        
        # Check if focal person exists
        if not self.db.is_focal_person(focal_id):
            await update.message.reply_text(
                f"❌ User ID {focal_id} is not currently a focal person."
            )
            return ConversationHandler.END
        
        # Remove focal person
        success = self.db.remove_focal_person(focal_id)
        
        if success:
            await update.message.reply_text(
                f"✅ **Focal Person Removed Successfully!**\n\n"
                f"🆔 **User ID:** {focal_id}\n"
                f"📅 **Removed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                f"This person can no longer submit security reports.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "❌ There was an error removing the focal person."
            )
        
        return ConversationHandler.END

    async def cancel_admin_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel any admin action conversation."""
        user_id = update.effective_user.id
        
        # Clear user data
        if user_id in self.user_data:
            del self.user_data[user_id]
        
        await update.message.reply_text(
            "❌ Admin action cancelled."
        )
        
        return ConversationHandler.END
