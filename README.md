# Security Status Bot

A Telegram bot designed for community groups to track and share security status information for different locations. This bot allows authorized focal people to submit security reports that all group members can view and query.

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

## License

This project is open source and available under the MIT License.
