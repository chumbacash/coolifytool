import threading
import sqlite3
import time
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from email_utils import generate_otp, send_otp_email, send_payment_email, send_approval_email
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_is _not_secret'

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# User class
class User:
    def __init__(self, id, name, email, approved, password):
        self.id = id
        self.name = name
        self.email = email
        self.approved = approved
        self.password = password

# Function to get user by email
def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['name'], user['email'], user['approved'], user['password'])
    return None

# Function to get user by ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['name'], user['email'], user['approved'], user['password'])
    return None

# Function to revert approved users after 1 month
def revert_approved_users():
    conn = get_db_connection()
    conn.execute("UPDATE users SET approved = 0 WHERE approved = 1 AND approved_date <= date('now', '-30 day')")
    conn.commit()
    conn.close()

# Function to send the payment email after a 5-minute delay
def schedule_payment_email(user_email, first_name):
    time.sleep(300)  # 5-minute delay
    send_payment_email(user_email, first_name)

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
                         (name, country, email, hashed_password, 0, registration_date))  # Unapproved initially
            conn.commit()
            conn.close()

            otp = generate_otp()
            session['otp'] = otp
            session['email'] = email  # Store user's email for later use

            send_otp_email(email, name, otp)

            # Schedule the payment email 5 minutes after registration
            threading.Thread(target=schedule_payment_email, args=(email, name)).start()

            flash('Signup successful! An OTP has been sent to your email. Please verify.', 'success')
            return redirect(url_for('verify_otp'))
        except sqlite3.Error as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form.get('otp')

        if 'otp' in session and str(session['otp']) == user_otp:
            email = session.get('email')

            conn = get_db_connection()
            conn.execute('UPDATE users SET approved = 0 WHERE email = ?', (email,))
            conn.commit()
            conn.close()

            session.pop('otp')
            session.pop('email')

            flash('Your account has been verified successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect(url_for('verify_otp'))

    return render_template('verify_otp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_status'] = user.approved

            if user.approved == 2:  # Admin
                session['is_admin'] = True
                return redirect(url_for('admin'))
            elif user.approved == 1:  # Approved user
                return redirect(url_for('user_dashboard'))
            else:  # Unapproved user
                return redirect(url_for('dashboard'))

        flash('Invalid email or password.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Allow both unapproved users (0) and admin (2) to access
    if session.get('user_status') == 0 or session.get('user_status') == 2:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Allow both approved users (1) and admin (2) to access
    if session.get('user_status') == 1 or session.get('user_status') == 2:
        return render_template('user_dashboard.html')
    else:
        return redirect(url_for('login'))


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
    approved_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
    conn.execute('UPDATE users SET approved = 1, approved_date = ? WHERE id = ?', (approved_date, user_id))
    conn.commit()
    user = get_user_by_id(user_id)
    send_approval_email(user.email, user.name)  # Send approval email
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
