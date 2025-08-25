# Telegram Drop Bot for Railway.app

A Telegram bot that drops accounts to verified users. Users must add specific text to their Telegram name to claim drops.

## 🚀 Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## Features

- **Name Verification**: Users must add "tornettlogs.cc uhq logs" to their Telegram name
- **Daily Limits**: One drop per user per day
- **Account Types**: Gmail, Instagram, Twitter, Netflix, Spotify, Discord, Facebook, Amazon
- **Database**: SQLite with automatic setup
- **Auto-restart**: Handles crashes gracefully

## Setup Instructions

### 1. Deploy to Railway

1. Fork this repository to your GitHub account
2. Go to [railway.app](https://railway.app) and sign up
3. Click "Start New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Railway will automatically detect Python and deploy

### 2. Get Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create new bot: `/newbot`
3. Choose name and username for your bot
4. Copy the bot token that BotFather gives you

### 3. Configure Railway

1. In Railway dashboard, go to your deployed project
2. Click on "Variables" tab
3. Add new variable:
   - **Name:** `TELEGRAM_BOT_TOKEN`
   - **Value:** paste your bot token here
4. Your bot will automatically redeploy and start working

### 4. Test Your Bot

1. Find your bot on Telegram using the username you chose
2. Send `/start` command
3. Bot should show available account drops
4. Try adding "tornettlogs.cc uhq logs" to your Telegram name and send `/start` again

## How It Works

1. User sends `/start` to your bot
2. Bot displays list of available account drops
3. Bot checks if user's Telegram name contains "tornettlogs.cc uhq logs"
4. **If verified**: User receives a random account from the drop pool
5. **If not verified**: User gets instructions on how to verify their name

## Commands

- `/start` - View available drops and claim one (if verified)
- `/help` - Show help information and verification instructions

## Verification Process

Users must add the exact text `tornettlogs.cc uhq logs` to their Telegram display name:
- Go to Telegram Settings → Edit Profile
- Add the text to their "Last Name" field
- Name should look like: "John Smith tornettlogs.cc uhq logs"
- Then use `/start` command to claim drops

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | Yes |

## File Structure

```
telegram-drop-bot/
├── telegram_drop_bot.py    # Main bot code
├── requirements.txt        # Python dependencies
├── railway.toml           # Railway configuration
├── Procfile              # Process definition
├── .gitignore            # Git ignore rules (keeps tokens safe)
└── README.md            # This documentation
```

## Account Types Included

The bot comes with sample accounts for:
- 📧 Gmail Accounts
- 📸 Instagram Accounts  
- 🐦 Twitter Accounts
- 🎬 Netflix Accounts
- 🎵 Spotify Accounts
- 💬 Discord Accounts
- 👥 Facebook Accounts
- 📦 Amazon Accounts

⚠️ **Note**: These are demo/sample accounts for educational purposes only.

## Security Features

- 🔒 Bot token stored as secure environment variable (not in code)
- 🛡️ Gitignore prevents accidentally committing sensitive data
- 📝 All account data stored in encrypted database
- ⏰ Daily limits prevent abuse
- 📊 Activity logging for monitoring

## Troubleshooting

### Bot Not Responding
1. Check Railway logs for errors
2. Verify `TELEGRAM_BOT_TOKEN` environment variable is set correctly
3. Test bot token validity: `https://api.telegram.org/bot<TOKEN>/getMe`

### Database Issues
1. Railway provides persistent storage automatically
2. Database is created on first startup
3. Check Railway logs for SQLite errors

### Out of Memory/CPU
1. Railway free tier: 512MB RAM, 0.5 vCPU
2. Monitor usage in Railway dashboard
3. Upgrade to paid plan if needed ($5/month)

## Cost

- **Free tier**: $5 usage credit (lasts 2-3 months for small bots)
- **After credit**: $5/month usage-based pricing
- **Perfect for**: Up to 500-1000 daily active users

## Adding Your Own Accounts

To add real accounts to your drop pool:

1. Access Railway database or use database management tools
2. Insert into `accounts` table:
```sql
INSERT INTO accounts (account_type, account_data) 
VALUES ('Service Name', '{"username": "account_user", "password": "account_pass"}');
```
3. Bot will automatically include them in drops

## Support

- 📚 Check Railway documentation for deployment issues
- 🔍 Use Railway logs for debugging bot errors
- 📱 Test bot commands directly in Telegram
- ⚙️ Verify environment variables in Railway dashboard

## License

This project is for educational and demonstration purposes only. Use responsibly and in accordance with all applicable laws and platform terms of service.

---

**🎉 Your bot is now live 24/7 on Railway.app!**

Test it by sending `/start` to your bot on Telegram.
