from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'amon_is_a_billionaire'

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Sample user class (replace with your own User model if you have one)
class User:
    def __init__(self, id, name, email, approved, password):
        self.id = id
        self.name = name
        self.email = email
        self.approved = approved
        self.password = password

# Sample function to get user from database (replace with your own logic)
def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['name'], user['email'], user['approved'], user['password'])
    return None

# Sample function to get user from database by ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['name'], user['email'], user['approved'], user['password'])
    return None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Format the current date and time to show only two digits for microseconds
        registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (name, country, email, password, approved, registration_date) VALUES (?, ?, ?, ?, ?, ?)',
                         (name, country, email, hashed_password, 0, registration_date))  # Not approved initially
            conn.commit()
            conn.close()
            flash('Signup successful! Please wait for approval.', 'success')
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.email == 'amon@coolifyapp.com'
            flash('Welcome! You are now logged in.', 'success')
            if user.approved:
                return redirect(url_for('user_dashboard'))  # Redirect approved users to user dashboard
            else:
                return redirect(url_for('dashboard'))  # Redirect unapproved users to dashboard
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('user_dashboard.html')


@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    pending_users = conn.execute('SELECT * FROM users WHERE approved = 0').fetchall()
    approved_users = conn.execute('SELECT * FROM users WHERE approved = 1').fetchall()
    conn.close()

    return render_template('admin.html', pending_users=pending_users, approved_users=approved_users)

@app.route('/approve_user/<int:user_id>')
def approve_user(user_id):
    conn = get_db_connection()
    # Format the current date and time to show only two digits for microseconds
    approved_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    conn.execute('UPDATE users SET approved = 1, approved_date = ? WHERE id = ?', (approved_date, user_id))
    conn.commit()
    conn.close()
    flash('User approved successfully.', 'success')
    return redirect(url_for('admin'))

@app.route('/remove_user/<int:user_id>')
def remove_user(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE users SET approved = 0 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User removed from approved list.', 'success')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
