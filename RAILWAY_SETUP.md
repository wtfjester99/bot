# 🚀 Railway.app Deployment Guide

## Complete Step-by-Step Instructions

### Prerequisites
- GitHub account
- Telegram bot token from @BotFather

---

## Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New repository"**
3. **Repository name**: `telegram-drop-bot` (or any name you like)
4. **Make it Public** (required for Railway free tier)
5. **Check "Add README file"**
6. **Click "Create repository"**

---

## Step 2: Upload Bot Files

Upload these 7 files to your GitHub repository:

### Required Files:
1. `telegram_drop_bot.py` - Main bot code
2. `requirements.txt` - Python dependencies  
3. `railway.toml` - Railway configuration
4. `Procfile` - Process definition
5. `.gitignore` - Security (prevents token leaks)
6. `README.md` - Documentation
7. `RAILWAY_SETUP.md` - This file

### How to Upload:
1. In your GitHub repo, click **"Add file" → "Upload files"**
2. Drag and drop all 7 files
3. Add commit message: "Initial bot deployment"
4. Click **"Commit changes"**

⚠️ **IMPORTANT**: Never upload files containing your actual bot token!

---

## Step 3: Get Bot Token

1. **Open Telegram** and message [@BotFather](https://t.me/BotFather)
2. **Send**: `/newbot`
3. **Choose bot name**: "My Drop Bot" (display name)
4. **Choose username**: "mydropbot123_bot" (must end with 'bot')
5. **Copy the token**: `123456789:ABCDEFghijklmnopqrstuvwxyz123456789`

---

## Step 4: Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Click "Login"** and sign in with GitHub
3. **Click "Start New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your bot repository**
6. **Railway automatically starts deployment** (takes 1-2 minutes)

---

## Step 5: Add Environment Variables

1. **In Railway dashboard**, click on your project
2. **Go to "Variables" tab**
3. **Click "New Variable"**
4. **Add**:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `your_bot_token_from_step_3`
5. **Click "Add"**
6. **Railway automatically redeploys** your bot

---

## Step 6: Test Your Bot

1. **Find your bot on Telegram** using the username from Step 3
2. **Send**: `/start`
3. **You should see**: "Available drops:" with account list
4. **Without verification**: You'll get verification instructions
5. **To test verification**:
   - Add `tornettlogs.cc uhq logs` to your Telegram name
   - Send `/start` again
   - You should receive an account drop!

---

## Monitoring Your Bot

### Railway Dashboard Features:
- **📊 Metrics**: CPU/RAM usage
- **📝 Logs**: Real-time bot activity  
- **⚙️ Variables**: Environment settings
- **🚀 Deployments**: Deployment history

### Useful Commands:
```bash
# View logs in real-time
railway logs --tail

# Check deployment status  
railway status

# Redeploy manually
railway up
```

---

## Troubleshooting

### ❌ Bot Not Starting
**Solution**:
1. Check Railway logs for error messages
2. Verify `TELEGRAM_BOT_TOKEN` is set correctly
3. Test token: `https://api.telegram.org/bot<TOKEN>/getMe`

### ❌ Bot Not Responding  
**Solution**:
1. Verify bot username is correct
2. Check if bot is blocked or restricted
3. Send `/start` command (don't just type messages)

### ❌ Database Errors
**Solution**:
1. Railway provides automatic persistent storage
2. Database file is created on first run
3. Check logs for SQLite permission errors

### ❌ Verification Not Working
**Solution**:
1. Ensure exact text: `tornettlogs.cc uhq logs`
2. Add to Telegram "Last Name" field
3. Check capitalization matches exactly

---

## Railway Free Tier Limits

- **💰 Cost**: $5 usage credit (free)
- **⏱️ Duration**: 2-3 months for small bots
- **💾 Storage**: 1GB persistent disk
- **🔥 CPU**: 0.5 vCPU
- **💭 RAM**: 512MB  
- **📊 Usage**: Perfect for 100-500 daily users

### After Free Credit:
- **$5/month** usage-based pricing
- **Scale automatically** with your bot growth
- **No surprises** - clear pricing dashboard

---

## Success Checklist

- [ ] ✅ GitHub repository created with all 7 files
- [ ] ✅ Bot token obtained from @BotFather  
- [ ] ✅ Railway project deployed successfully
- [ ] ✅ `TELEGRAM_BOT_TOKEN` environment variable set
- [ ] ✅ Bot responds to `/start` command
- [ ] ✅ Verification system working
- [ ] ✅ Account drops functioning  
- [ ] ✅ No errors in Railway logs

---

## Next Steps

### For Production Use:
1. **Monitor usage** to stay within free credit
2. **Add real accounts** to replace sample data
3. **Set up monitoring** alerts for errors
4. **Scale up** when you get more users

### To Add More Accounts:
1. **Access Railway database** via dashboard
2. **Use database tools** to insert new accounts
3. **Format**: JSON with account credentials
4. **Test drops** to verify new accounts work

---

## Security Best Practices

- ✅ **Never commit bot tokens** to GitHub
- ✅ **Use environment variables** for all secrets
- ✅ **Enable 2FA** on GitHub and Railway accounts  
- ✅ **Monitor logs** for suspicious activity
- ✅ **Rotate tokens** if compromised
- ✅ **Use sample data** for testing only

---

**🎉 Congratulations! Your bot is now live 24/7 on Railway!**

Your bot will:
- ✅ **Run continuously** without interruption
- ✅ **Auto-restart** if it crashes  
- ✅ **Scale automatically** as users grow
- ✅ **Stay online** even during Railway maintenance
- ✅ **Handle hundreds of users** on free tier

**Test it now by messaging your bot on Telegram!** 🚀
