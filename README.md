# 🛡️ Telegram Security Status Bot with Mini App

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-21.6-blue.svg)](https://core.telegram.org/bots/api)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern Telegram bot with a beautiful Mini App interface for community security reporting. This bot helps communities stay informed about security conditions in different areas through both traditional bot commands and a modern web interface.

## 🌟 Key Features

### 📱 **Modern Mini App Interface**
- Beautiful, responsive web design that adapts to Telegram's theme
- Real-time search and filtering of security reports
- Interactive forms for easy report submission
- Mobile-optimized touch-friendly interface
- Status color coding (Safe=Green, Warning=Yellow, Danger=Red)
- Native Telegram haptic feedback

### 🤖 **Traditional Bot Commands**
- Full command-line interface for all bot functions
- Multi-step conversations for report submission
- Admin commands for user management
- Location-based report filtering

### 👥 **Role-Based Access Control**
- **Admins**: Manage focal people, full system access
- **Focal People**: Submit security reports
- **Regular Users**: View reports and search by location

## Features

### For All Group Members
- **View Recent Reports**: Get the latest 10 security reports
- **Location-Based Search**: Search for security reports by location
- **Real-time Updates**: Stay informed about security conditions in your area

### For Focal People (Authorized Reporters)
- **Submit Security Reports**: Input location, status, and recommended actions
- **Guided Input Process**: Step-by-step report submission with validation
- **Automatic Timestamps**: All reports are automatically timestamped

### For Administrators
- **Manage Focal People**: Add and remove authorized reporters
- **User Management**: View all active focal people
- **Access Control**: Only admins can manage focal people permissions

## Available Commands

### General Commands
- `/start` or `/help` - Show welcome message and command list
- `/status` - View the 10 most recent security reports
- `/location <area>` - Search for security reports by location name

### Focal People Commands
- `/report` - Start the security report submission process (guided conversation)
- `/cancel` - Cancel an ongoing report submission

### Admin Commands
- `/addfocal` - Add a new focal person (requires User ID and name)
- `/listfocal` - List all authorized focal people
- `/removefocal` - Remove a focal person's authorization
- `/cancel` - Cancel an ongoing admin action

## Bot Setup Instructions

### Prerequisites
1. **Python 3.7+** installed on your system
2. A **Telegram account**
3. Basic command line knowledge

### Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "Community Security Bot")
4. Choose a username for your bot (must end with 'bot', e.g., "community_security_bot")
5. Copy the bot token provided by BotFather

### Step 2: Get Your Telegram User ID

1. Send `/start` to your newly created bot
2. Use a bot like `@userinfobot` to get your Telegram User ID
3. Save this number - you'll need it for admin access

### Step 3: Install Dependencies

```bash
# Navigate to the bot directory
cd security-status-bot

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file with your information:
   ```env
   # Your bot token from BotFather
   BOT_TOKEN=1234567890:ABCdefGHijKLmnOPqrSTuvWXyz

   # Your Telegram User ID(s) - comma separated for multiple admins
   ADMIN_USER_IDS=123456789,987654321

   # Database file location
   DATABASE_PATH=security_reports.db
   ```

### Step 5: Run the Bot

```bash
python bot.py
```

The bot will start and display a message like:
```
INFO - Starting Security Status Bot...
INFO - Application started
```

### Step 6: Add the Bot to Your Group

1. Add your bot to your Telegram group
2. Make sure the bot has permission to send messages
3. Test the bot by sending `/start` in the group

## Usage Guide

### For Group Administrators

#### Adding Focal People
1. Send `/addfocal` command
2. Provide the Telegram User ID of the person
3. Provide their full name (alphabets and spaces only)
4. The person can now submit security reports

#### Managing Focal People
- Use `/listfocal` to see all authorized focal people
- Use `/removefocal` to remove someone's authorization
- Users can get their ID by sending `/start` to the bot privately

### For Focal People

#### Submitting Security Reports
1. Send `/report` command
2. Follow the guided process:
   - **Location**: Enter the area/location name (alphabets and spaces only)
   - **Status**: Describe the current security situation
   - **Recommended Action**: Suggest what community members should do

#### Example Report Flow
```
User: /report
Bot: Please provide the location/area name:

User: Downtown Market Area
Bot: Location: Downtown Market Area
     Now, please describe the security status:

User: Heavy police presence due to ongoing protests
Bot: Status: Heavy police presence due to ongoing protests
     Finally, please provide the recommended action:

User: Avoid the area until further notice
Bot: ✅ Security Report Submitted Successfully!
     [Report details displayed]
```

### For All Group Members

#### Viewing Recent Reports
Send `/status` to see the latest 10 security reports with:
- Location
- Security status
- Recommended action
- Reporter name
- Timestamp

#### Searching by Location
Send `/location <area name>` to find reports for specific locations:
```
/location downtown
/location market area
/location central district
```

## Database Schema

The bot uses SQLite database with the following tables:

### security_reports
- `id`: Unique report identifier
- `location`: Area/location name
- `status`: Security status description
- `recommended_action`: Suggested actions
- `reporter_id`: Telegram User ID of reporter
- `reporter_name`: Name of reporter
- `timestamp`: When report was created
- `is_active`: Whether report is active

### focal_people
- `id`: Unique identifier
- `telegram_user_id`: Telegram User ID
- `name`: Full name
- `added_by`: Admin who added them
- `added_date`: When they were added
- `is_active`: Whether they're active

### admins
- `id`: Unique identifier
- `telegram_user_id`: Admin's Telegram User ID
- `added_date`: When admin was added

## Security Features

- **Input Validation**: Location and name fields only accept alphabets and spaces
- **Role-based Access**: Only focal people can submit reports
- **Admin Controls**: Only admins can manage focal people
- **Automatic Logging**: All actions are logged with timestamps
- **Database Integrity**: SQLite with proper constraints and data types

## Troubleshooting

### Common Issues

1. **"BOT_TOKEN not found" error**
   - Check your `.env` file exists and contains the correct bot token
   - Make sure there are no extra spaces around the token

2. **"Only authorized focal people can submit reports"**
   - The user needs to be added as a focal person by an admin
   - Use `/addfocal` command to add them

3. **Admin commands not working**
   - Verify your User ID is in the `ADMIN_USER_IDS` list
   - Make sure the User ID is correct (no extra characters)

4. **Bot not responding in group**
   - Check if bot has permission to send messages in the group
   - Try sending commands privately to the bot first

### Getting Help

1. Check the logs for error messages when running `python bot.py`
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Verify your `.env` file configuration
4. Test commands in a private chat with the bot first

## File Structure

```
security-status-bot/
├── bot.py              # Main bot application
├── database.py         # Database operations and schema
├── admin_handlers.py   # Admin functionality handlers
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env              # Your environment configuration (create this)
├── security_reports.db # SQLite database (created automatically)
└── README.md         # This documentation file
```

## Customization

You can customize the bot by modifying:

- **Message templates** in `bot.py` (welcome messages, help text, etc.)
- **Database schema** in `database.py` (add new fields or tables)
- **Admin permissions** by modifying the admin checking logic
- **Validation rules** for locations and names (currently alphabets only)

## Deployment Options

### Local Deployment
Run the bot on your local machine or server using the instructions above.

### Cloud Deployment
For 24/7 operation, consider deploying to:
- **Heroku**: Simple deployment with buildpack
- **DigitalOcean**: Virtual private server
- **AWS EC2**: Scalable cloud hosting
- **Google Cloud**: Reliable cloud platform

Remember to keep your `.env` file secure and never commit it to version control!

## 🌐 Telegram Mini App Setup

### Mini App Features

The bot includes a modern web interface that runs inside Telegram as a Mini App:

- **Interactive Dashboard**: View all security reports in a beautiful, scrollable interface
- **Smart Search**: Real-time filtering by location with instant results
- **One-Click Reporting**: Submit reports through intuitive forms with validation
- **Admin Panel**: Manage focal people with an easy-to-use interface
- **Responsive Design**: Works perfectly on mobile and desktop
- **Native Integration**: Seamlessly integrates with Telegram's theming and haptic feedback

### Setting Up the Mini App

1. **Configure the Mini App in BotFather**:
   ```
   1. Go to @BotFather in Telegram
   2. Send /mybots
   3. Select your bot
   4. Choose "Bot Settings" → "Menu Button"
   5. Set the Web App URL to: https://yourdomain.com/webapp
   6. Set button text: "🛡️ Security Reports"
   ```

2. **Deploy the Web Application**:
   ```bash
   # Install additional dependencies for the web app
   pip install flask flask-cors
   
   # Run the web application
   python webapp/app.py
   ```

3. **Configure Environment for Mini App**:
   Add these variables to your `.env` file:
   ```env
   # Web application settings
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   FLASK_DEBUG=False
   
   # Domain where your Mini App is hosted
   WEBAPP_URL=https://yourdomain.com
   ```

### Mini App File Structure

```
webapp/
├── app.py              # Flask web application
├── templates/
│   └── index.html      # Main Mini App interface
├── static/
│   ├── css/
│   │   └── style.css   # Styling for Mini App
│   └── js/
│       └── app.js      # Mini App functionality
└── api/
    └── routes.py       # API endpoints for Mini App
```

### API Endpoints

The Mini App communicates with the bot through REST API endpoints:

- `GET /api/reports` - Get recent security reports
- `GET /api/reports/location/<location>` - Get reports by location
- `POST /api/reports` - Submit new security report (focal people only)
- `GET /api/focal-people` - List focal people (admin only)
- `POST /api/focal-people` - Add new focal person (admin only)
- `DELETE /api/focal-people/<id>` - Remove focal person (admin only)

## 🚀 Advanced Deployment

### Using Docker

1. **Create Dockerfile** (example provided in repository)
2. **Build the image**:
   ```bash
   docker build -t security-status-bot .
   ```
3. **Run the container**:
   ```bash
   docker run -d --env-file .env security-status-bot
   ```

### Using Heroku

1. **Create Heroku app**:
   ```bash
   heroku create your-security-bot
   ```

2. **Set environment variables**:
   ```bash
   heroku config:set BOT_TOKEN=your_bot_token
   heroku config:set ADMIN_USER_IDS=your_user_id
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

### Production Considerations

- **Database**: Consider using PostgreSQL for production instead of SQLite
- **SSL/HTTPS**: Required for Telegram Mini Apps
- **Rate Limiting**: Implement rate limiting for API endpoints
- **Logging**: Set up proper logging and monitoring
- **Backups**: Regular database backups for report data
- **Security**: Use secrets management for sensitive environment variables

## 📱 Using the Mini App

### For Regular Users
1. Open the bot in Telegram
2. Click the "🛡️ Security Reports" button at the bottom
3. Browse recent reports or search by location
4. View detailed information for each report

### For Focal People
1. Access the Mini App as above
2. Switch to the "Submit Report" tab
3. Fill in the location, status, and recommended action
4. Submit the report with one click

### For Administrators
1. Access the Mini App
2. Switch to the "Admin Panel" tab
3. View all focal people
4. Add or remove focal people as needed
5. All changes sync with the bot database

## 🔧 Development

### Running in Development Mode

1. **Start the bot**:
   ```bash
   python bot.py
   ```

2. **Start the web app** (in another terminal):
   ```bash
   cd webapp
   python app.py
   ```

3. **Access locally**: Open `http://localhost:5000/webapp`

### Testing the Mini App

1. Use ngrok for local testing:
   ```bash
   ngrok http 5000
   ```

2. Configure the ngrok URL in BotFather as your Mini App URL

3. Test the Mini App directly in Telegram

## 📊 Monitoring and Analytics

- **Bot Logs**: All bot activities are logged with timestamps
- **Report Statistics**: Track report submissions and user engagement
- **Error Handling**: Comprehensive error logging for debugging
- **Usage Metrics**: Monitor which features are used most frequently

## 🤝 Contributing

We welcome contributions! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure all contributions follow the existing code style and include appropriate documentation.

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the GitHub issues for similar problems
3. Create a new issue with detailed information about your problem

## License

This project is open source and available under the MIT License.

---

**Made with ❤️ for community safety**
