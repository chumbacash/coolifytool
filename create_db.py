import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')

# Drop the users table if it exists (optional)
conn.execute('DROP TABLE IF EXISTS users')

# Create the users table with the correct schema
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    approved INTEGER DEFAULT 0,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_date DATETIME  -- Field to store when a user was approved
);
''')

conn.close()
