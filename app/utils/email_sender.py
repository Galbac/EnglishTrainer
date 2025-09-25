# app/utils/email_sender.py

import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


async def send_daily_reminder_email(to_email: str, username: str, words: str, base_url: str):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = f"Привет, {username}! У вас слова на повторение 📚"

    body = f"""
Привет, {username}!

У вас {len(words.split(','))} слов на повторение: {words}. 

Не забудьте их повторить — это поможет запомнить навсегда!

👉 Пройти тест: {base_url}/test?category=pending

Спасибо, что используете English Trainer 💪

— Ваш персональный тренер по английскому
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        client = aiosmtplib.SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True)
        await client.connect()
        await client.login(SMTP_USER, SMTP_PASS)
        await client.send_message(msg)
        await client.quit()
        print(f"✅ Письмо отправлено на {to_email}")
    except Exception as e:
        print(f"❌ Ошибка отправки письма: {e}")
