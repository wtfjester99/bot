import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import json
from datetime import datetime
import asyncio

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramDropBot:
    def __init__(self, db_path='drop_bot.db'):
        self.db_path = db_path
        self.required_text = "tornettlogs.cc uhq logs"
        self.init_database()

    def init_database(self):
        """Initialize the database with tables and sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                telegram_username TEXT,
                full_name TEXT,
                verified BOOLEAN DEFAULT 0,
                drops_received INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_type TEXT NOT NULL,
                account_data TEXT NOT NULL,
                is_dropped BOOLEAN DEFAULT 0,
                dropped_to_user_id INTEGER,
                dropped_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dropped_to_user_id) REFERENCES users (telegram_id)
            )
        """)

        # Drop logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drop_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                account_id INTEGER,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (telegram_id),
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        """)

        # Check if sample data exists
        cursor.execute('SELECT COUNT(*) FROM accounts')
        count = cursor.fetchone()[0]

        if count == 0:
            # Insert sample accounts
            sample_accounts = [
                ('Gmail Account', '{"email": "sample1@gmail.com", "password": "demo123", "recovery": "backup@gmail.com"}'),
                ('Instagram Account', '{"username": "demo_insta", "password": "demo456", "followers": "1.2K"}'),
                ('Twitter Account', '{"username": "@demo_tweet", "password": "demo789", "followers": "856"}'),
                ('Netflix Account', '{"email": "netflix@demo.com", "password": "demo321", "plan": "Premium"}'),
                ('Spotify Account', '{"email": "spotify@demo.com", "password": "demo654", "plan": "Premium"}'),
                ('Discord Account', '{"username": "demo_user#1234", "password": "demo987", "servers": "12"}'),
                ('Facebook Account', '{"email": "facebook@demo.com", "password": "demo111", "verified": true}'),
                ('Amazon Account', '{"email": "amazon@demo.com", "password": "demo222", "prime": true}'),
            ]

            for account_type, account_data in sample_accounts:
                cursor.execute("""
                    INSERT INTO accounts (account_type, account_data)
                    VALUES (?, ?)
                """, (account_type, account_data))

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def is_user_verified(self, user_full_name):
        """Check if user's name contains the required verification text"""
        if not user_full_name:
            return False
        return self.required_text.lower() in user_full_name.lower()

    def get_available_drops(self):
        """Get list of available drops"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT account_type, COUNT(*) as count 
            FROM accounts 
            WHERE is_dropped = 0 
            GROUP BY account_type
            ORDER BY account_type
        """)

        drops = cursor.fetchall()
        conn.close()

        return [{"type": row["account_type"], "count": row["count"]} for row in drops]

    def get_total_available_drops(self):
        """Get total number of available drops"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as total FROM accounts WHERE is_dropped = 0')
        result = cursor.fetchone()
        conn.close()

        return result["total"] if result else 0

    def has_user_received_drop_today(self, user_id):
        """Check if user already received a drop today"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM drop_logs 
            WHERE user_id = ? 
            AND action = 'drop_given' 
            AND DATE(timestamp) = ?
        """, (user_id, today))

        result = cursor.fetchone()
        conn.close()

        return result["count"] > 0 if result else False

    def give_drop_to_user(self, user_id, username, full_name):
        """Give a random available drop to the user"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            # Get a random available account
            cursor.execute("""
                SELECT id, account_type, account_data 
                FROM accounts 
                WHERE is_dropped = 0 
                ORDER BY RANDOM() 
                LIMIT 1
            """)

            account = cursor.fetchone()

            if not account:
                conn.close()
                return {"success": False, "message": "No drops available at the moment."}

            # Mark account as dropped
            cursor.execute("""
                UPDATE accounts 
                SET is_dropped = 1, dropped_to_user_id = ?, dropped_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (user_id, account["id"]))

            # Insert/update user record
            cursor.execute("""
                INSERT OR REPLACE INTO users 
                (telegram_id, telegram_username, full_name, verified, drops_received, last_activity)
                VALUES (?, ?, ?, 1, 
                    COALESCE((SELECT drops_received FROM users WHERE telegram_id = ?), 0) + 1,
                    CURRENT_TIMESTAMP)
            """, (user_id, username, full_name, user_id))

            # Log the drop
            cursor.execute("""
                INSERT INTO drop_logs (user_id, account_id, action)
                VALUES (?, ?, 'drop_given')
            """, (user_id, account["id"]))

            conn.commit()

            # Format account data for display
            account_data = json.loads(account["account_data"])
            formatted_data = f"**{account['account_type']}**\n\n"

            for key, value in account_data.items():
                formatted_data += f"**{key.capitalize()}:** `{value}`\n"

            conn.close()
            return {"success": True, "message": formatted_data}

        except Exception as e:
            conn.rollback()
            conn.close()
            logger.error(f"Error giving drop to user {user_id}: {str(e)}")
            return {"success": False, "message": f"Error processing drop: {str(e)}"}

# Initialize bot instance
bot_instance = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command"""
    user = update.effective_user
    user_id = user.id
    username = user.username or ""

    # Get user's full name (first_name + last_name)
    full_name = ""
    if user.first_name:
        full_name += user.first_name
    if user.last_name:
        full_name += f" {user.last_name}"

    logger.info(f"User {user_id} ({username}) started bot. Full name: '{full_name}'")

    # Get available drops first
    available_drops = bot_instance.get_available_drops()
    total_available = bot_instance.get_total_available_drops()

    # Create drops list message
    drops_message = "**Available drops:**\n\n"
    if available_drops:
        for drop in available_drops:
            drops_message += f"• {drop['type']}: {drop['count']} available\n"
        drops_message += f"\n**Total available:** {total_available}\n\n"
    else:
        drops_message = "**No drops currently available.**\n\n"

    # Check if user is verified
    if not bot_instance.is_user_verified(full_name):
        verification_message = f"""**To claim drops, please add**

`{bot_instance.required_text}`

You will need to add the entire line above to receive your drop to your Telegram display name (last name) and try again.

If your name was `{full_name or 'bob'}` it should now be `{full_name or 'bob'} {bot_instance.required_text}`

This means that you have to change your telegram name to be able to claim any drops."""

        await update.message.reply_text(
            drops_message + verification_message,
            parse_mode='Markdown'
        )
        return

    # User is verified - check if already received drop today
    if bot_instance.has_user_received_drop_today(user_id):
        await update.message.reply_text(
            drops_message + "**You have already claimed your drop for today. Come back tomorrow!** 🕒",
            parse_mode='Markdown'
        )
        return

    # Give user a drop
    drop_result = bot_instance.give_drop_to_user(user_id, username, full_name)

    if drop_result["success"]:
        message = drops_message + f"🎉 **Congratulations! You received:**\n\n{drop_result['message']}"
    else:
        message = drops_message + drop_result["message"]

    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command"""
    help_text = f"""
**🤖 Telegram Drop Bot Help**

This bot provides free account drops to verified users.

**📋 Commands:**
• `/start` - Get available drops and claim your daily drop
• `/help` - Show this help message

**✅ How to get verified:**
1. Add `{bot_instance.required_text}` to your Telegram display name (last name)
2. Use the `/start` command to claim your drop

**📖 Rules:**
• One drop per user per day
• Must be verified to claim drops
• Available drops change regularly

**Enjoy! 🎉**
    """

    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle non-command messages"""
    await update.message.reply_text(
        "👋 Hi! Use `/start` to get your drop or `/help` for more information.",
        parse_mode='Markdown'
    )

def main() -> None:
    """Run the bot"""
    global bot_instance

    # Get bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN environment variable not set!")
        logger.error("Please set your bot token in Railway environment variables")
        return

    # Initialize bot instance
    bot_instance = TelegramDropBot()
    logger.info("✅ Bot instance initialized")

    # Create application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Get port from environment (Railway provides this)
    port = int(os.environ.get('PORT', 8080))

    # Run the bot
    logger.info("🚀 Starting bot...")
    logger.info(f"📡 Bot will run on port {port}")

    # Run with polling (Railway supports this)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
