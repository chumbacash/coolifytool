# Coolify App

It is a Flask application for user signup, login, and admin management with real-time data analysis using WebSockets for Deriv trading.

## Features

- User signup and login
- Admin panel for user approval and management
- Real-time data analysis (WebSockets)
- Flash messages for user feedback

## Project Structure
```
Coolify/
│
├── .venv                   # Virtual environment for project dependencies
│
├── static/                 # Static files (CSS, JavaScript, images)
│   ├── css/
│   │   ├── style.css       # Main CSS file for styling
│   │   └── index.css       # Additional CSS file for specific styles
│   ├── js/
│   │   └── script.js       # JavaScript file for interactive features
│   └── favicon.ico         # Favicon for the website
│
├── templates/              # HTML templates for rendering views
│   ├── login.html          # Login page template
│   ├── admin.html          # Admin management template
│   ├── signup.html         # Signup page template
│   ├── user_dashboard.html # User dashboard template
│   └── dashboard.html      # General dashboard template or additional dashboard view
│
├── requirements.txt        # List of project dependencies
├── database.db             # SQLite database file
├── setup_database.py       # Script to initialize or set up the database
├── forms.py                # File containing form classes and logic
├── app.py                  # Flask application entry point and configuration
└── models.py               # Database models and schema definitions
```
## Modifications
- we went ahead and added a cool UI to the user_dashboard
- Added some security features towards the data
- Added the verification for email, this will basically lead to better marketing 
  we will get emails, which we will use for marketing.
- Since the database is (mysql) typo. It will be better if we improve or take this to mongodb
- cd/cI implementation through/ using github actions.

## Marketing
- We improved the way we will be doing some marketing here.
- The approach of keeping data safe for the purpose of sending notification emails.
- Payments will be emphasied to the users since we are improving the card/ emails to be sent to the user.
