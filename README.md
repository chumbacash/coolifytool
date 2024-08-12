# Coolify App

It is a Flask application for user signup, login, and admin management with real-time data analysis using WebSockets for Deriv trading.

## Features

- User signup and login
- Admin panel for user approval and management
- Real-time data analysis (WebSockets)
- Flash messages for user feedback

## Project Structure

```plaintext
Coolifyapp/
│
├── .venv                   # Virtual environment
│
├── static/
│   ├── css/
│   │   └── style.css      # CSS file
│   ├── js/
│   │   └── script.js      # JavaScript file
│
├── templates/
│   ├── login.html
│   ├── admin_panel.html
│   ├── admin.html
│   ├── signup.html
│   ├── user_dashboard.html
│   └── dashboard.html
│
├── requirements.txt        # Project dependencies
├── database.db             # SQLite database file
├── setup_database.py       # Database setup script
├── forms.py                # Form classes
├── app.py                  # Flask application entry point
├── main.py                 # WebSocket server script
└── models.py               # Database models
