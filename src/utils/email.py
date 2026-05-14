import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_USER     = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
BASE_URL       = os.getenv("BASE_URL", "http://127.0.0.1:5500/front-end/pages/signIn/index.html")


def send_activation_email(student_name: str, student_email: str, token: str):
    activation_link = f"{BASE_URL}/students/activate/{token}"

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
        <div style="max-width: 500px; margin: auto; background: white; border-radius: 8px; padding: 30px;">
          <h2 style="color: #333;">Bem-vindo ao GymFlow, {student_name}!</h2>
          <p style="color: #555;">A tua conta foi criada com sucesso. Clica no botão abaixo para activar a tua conta.</p>
          <a href="{activation_link}"
             style="display: inline-block; margin-top: 20px; padding: 12px 24px;
                    background-color: #4CAF50; color: white; text-decoration: none;
                    border-radius: 5px; font-size: 16px;">
            Activar Conta
          </a>
          <p style="margin-top: 20px; color: #999; font-size: 12px;">
            Se não criaste esta conta, podes ignorar este email.
          </p>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "GymFlow — Activa a tua conta"
    msg["From"]    = GMAIL_USER
    msg["To"]      = student_email

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, student_email, msg.as_string())