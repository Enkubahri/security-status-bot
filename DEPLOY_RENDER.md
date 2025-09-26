# 🚀 Deploy to Render

This guide walks you through deploying your Telegram Security Status Bot Mini App to Render.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code must be on GitHub (already done!)
3. **Telegram Bot Token**: From BotFather
4. **Admin User ID**: Your Telegram user ID

## 🛠️ Deployment Steps

### 1. Create a New Web Service

1. **Log into Render**: Go to https://dashboard.render.com
2. **New Web Service**: Click "New" → "Web Service"
3. **Connect Repository**: 
   - Choose "Connect a repository"
   - Select your GitHub account
   - Choose: `Enkubahri/security-status-bot`
   - Click "Connect"

### 2. Configure the Service

**Basic Settings:**
- **Name**: `security-status-miniapp` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `master`
- **Runtime**: `Python 3`

**Build & Deploy Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python webapp/app.py`

### 3. Set Environment Variables

In the "Environment Variables" section, add these variables:

```env
BOT_TOKEN=your_actual_bot_token_here
ADMIN_USER_IDS=your_telegram_user_id_here
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=10000
FLASK_DEBUG=false
DATABASE_PATH=/tmp/security_reports.db
```

**Important**: Replace the placeholder values with your actual data:
- `BOT_TOKEN`: Get this from @BotFather in Telegram
- `ADMIN_USER_IDS`: Your Telegram User ID (get from @userinfobot)

### 4. Deploy

1. **Review Settings**: Double-check all configurations
2. **Create Web Service**: Click "Create Web Service"
3. **Wait for Deployment**: This will take a few minutes
4. **Check Logs**: Monitor the deployment progress in the logs

### 5. Configure Telegram Mini App

Once deployed, you'll get a URL like: `https://your-app-name.onrender.com`

1. **Go to @BotFather** in Telegram
2. **Send**: `/mybots`
3. **Select your bot**
4. **Choose**: "Bot Settings" → "Menu Button"
5. **Set Web App URL**: `https://your-app-name.onrender.com`
6. **Set Button Text**: `🛡️ Security Reports`

## ✅ Verify Deployment

### Test the Mini App
1. **Open your bot** in Telegram
2. **Click the menu button** at the bottom
3. **Verify the Mini App loads** correctly
4. **Test all functionality**:
   - View reports
   - Submit reports (if you're a focal person)
   - Admin panel (if you're an admin)

### Test API Endpoints
You can test the API directly:
- `https://your-app-name.onrender.com/health` - Should return health status
- `https://your-app-name.onrender.com/api/reports` - Should return recent reports

## 🔧 Troubleshooting

### Common Issues

1. **"Application Error"**
   - Check the logs in Render dashboard
   - Verify all environment variables are set correctly
   - Ensure BOT_TOKEN is valid

2. **Mini App doesn't load**
   - Verify the URL in BotFather is correct
   - Check if the service is running (not sleeping)
   - Ensure HTTPS is working

3. **Database errors**
   - The app creates the database automatically
   - If persistent data is needed, consider upgrading to a paid plan

4. **Bot commands still work but Mini App doesn't**
   - The bot and Mini App are separate components
   - Ensure both have the same BOT_TOKEN
   - Check admin permissions

### Render-Specific Considerations

- **Free Plan Limitations**:
  - Apps go to sleep after 15 minutes of inactivity
  - Limited to 750 hours per month
  - Temporary file system (data doesn't persist across restarts)

- **Database Persistence**:
  - For production use, consider using Render's PostgreSQL add-on
  - Or upgrade to a paid plan for persistent disk storage

## 🎯 Next Steps

### Production Recommendations

1. **Enable Telegram Authentication**:
   - Uncomment validation in `webapp/app.py`
   - This secures your API endpoints

2. **Database Upgrade**:
   - Consider PostgreSQL for production
   - Add database backups

3. **Monitoring**:
   - Set up health check monitoring
   - Add error tracking (like Sentry)

4. **Custom Domain** (Paid plans):
   - Use your own domain instead of `.onrender.com`

### Updating Your App

1. **Make changes** to your code locally
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update Mini App"
   git push origin master
   ```
3. **Render auto-deploys** from your GitHub repository

## 📞 Support

If you encounter issues:
1. Check Render's logs for errors
2. Verify your environment variables
3. Test API endpoints directly
4. Check Telegram's webhook settings

Your Mini App should now be live and accessible through Telegram! 🎉
