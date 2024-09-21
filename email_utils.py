import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp():
    return random.randint(100000, 999999)

# Send OTP email
def send_otp_email(user_email, first_name, otp):
    sender_email = "noreply@coolifyapp.com"
    receiver_email = user_email
    password = "JurnAmoo&24"  # Use your actual email password or app password

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify Your Coolify Account"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""
    <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
                body {{
                    font-family: 'Poppins', Arial, sans-serif;
                    background-color: #f0f4f8;
                    margin: 0;
                    padding: 40px 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .otp {{
                    background: linear-gradient(135deg, #7209b7, #3a0ca3);
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    margin: 30px 0;
                    color: #ffffff;
                    font-size: 32px;
                    letter-spacing: 8px;
                    font-weight: 600;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    color: #4a4a4a;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="color: #3a0ca3; font-size: 36px; letter-spacing: 2px;">Coolify</h1>
                </div>
                <p>Hey <strong style="color: #3a0ca3;">{first_name}</strong>,</p>
                <p>Welcome to Coolify! Please verify your email address using this code:</p>
                <div class="otp">{otp}</div>
                <p>If you didn't sign up for Coolify, you can ignore this email.</p>
                <div class="footer">
                    <p>&copy; 2021 - 2024 Coolify. All Rights Reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.zoho.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("OTP email sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")

# Send Payment Email
def send_payment_email(user_email, first_name):
    sender_email = "support@coolifyapp.com"
    receiver_email = user_email
    password = "AmonChumba2018"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Complete Your Coolify Payment"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""
    <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
                body {{
                    font-family: 'Poppins', Arial, sans-serif;
                    background-color: #f0f4f8;
                    margin: 0;
                    padding: 40px 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .btn {{
                    padding: 10px 20px;
                    background-color: #f04a4a;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 8px;
                    font-size: 16px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    color: #4a4a4a;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="color: #3a0ca3; font-size: 36px; letter-spacing: 2px;">Coolify</h1>
                </div>
                <p>Hey <strong style="color: #3a0ca3;">{first_name}</strong>,</p>
                <p>We’re almost there! 🚀 To unlock all the awesome features Coolify has to offer, please complete your payment of <strong>$30</strong>.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://coolifyapp.com/" class="btn">Pay Now</a>
                </div>
                <p>If you need any assistance, contact us at <a href="mailto:support@coolifyapp.com" style="color: #3a0ca3;">support@coolifyapp.com</a>.</p>
                <div class="footer">
                    <p>&copy; 2021 - 2024 Coolify. All Rights Reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.zoho.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Payment email sent successfully!")
    except Exception as e:
        print(f"Failed to send payment email: {e}")

# Send Approval Email
def send_approval_email(user_email, first_name):
    sender_email = "support@coolifyapp.com"
    receiver_email = user_email
    password = "AmonChumba2018"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Welcome to Coolify - You're Approved!"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""
    <html>
        <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
                body {{
                    font-family: 'Poppins', Arial, sans-serif;
                    background-color: #f0f4f8;
                    margin: 0;
                    padding: 40px 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .btn {{
                    padding: 10px 20px;
                    background-color: #3a0ca3;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 8px;
                    font-size: 16px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    color: #4a4a4a;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="color: #3a0ca3; font-size: 36px; letter-spacing: 2px;">Coolify</h1>
                </div>
                <p>Hey <strong style="color: #3a0ca3;">{first_name}</strong>,</p>
                <p>Congratulations! 🎉 You’ve officially been approved to access the full Coolify experience.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://app.coolifyapp.com" class="btn">Log in to Coolify</a>
                </div>
                <p>If you have any questions, contact us at <a href="mailto:support@coolifyapp.com" style="color: #3a0ca3;">support@coolifyapp.com</a>.</p>
                <div class="footer">
                    <p>&copy; 2021 - 2024 Coolify. All Rights Reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.zoho.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Approval email sent successfully!")
    except Exception as e:
        print(f"Failed to send approval email: {e}")
