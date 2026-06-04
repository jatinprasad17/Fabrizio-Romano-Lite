import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def send_transfer_email(to_email,team,analysis):
    gmail = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    date_str = datetime.now().strftime("%B %d %Y")

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
        <h2 style="color: #1a1a2e;">⚽ {team} Transfer News</h2>
        <p style="color: #666;">Daily Update — {date_str}</p>
        <hr>
        <div style="white-space: pre-line; line-height: 1.8;">
            {analysis}
        </div>
        <hr>
        <p style="color: #999; font-size: 12px;">Powered by Fabrizio Romano Lite 🤖</p>
    </body>
    </html>
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"⚽ {team} Transfer News — {date_str}"
    msg["From"] = gmail
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail, password)
        server.sendmail(gmail, to_email, msg.as_string())
    
    print(f"Email sent to {to_email}!")