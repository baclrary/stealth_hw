import random
import smtplib
import time
from email.message import EmailMessage

from celery import Celery

from app.config import SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER

celery = Celery("tasks", broker="redis://127.0.0.1:6379/0")
celery.conf.broker_connection_retry_on_startup = True


def get_email_template_dashboard(email: str):
    message = EmailMessage()
    message["Subject"] = "Stealth Startup"
    message["From"] = SMTP_USER
    message["To"] = SMTP_USER

    message.set_content(
        "<div style='font-family: Arial, sans-serif; color: #333;'>"
        f"<h1 style='color: #4A90E2;'>Hello, {email}!</h1>"
        "<p>We are excited to share with you the latest report on all products listed on your website. \
            This comprehensive overview provides insights into product performance, customer preferences,\
                and market trends.</p>"
        "<h2 style='color: #4A90E2;'>Product Performance</h2>"
        "<img src='https://cdn-icons-png.flaticon.com/512/4129/4129571.png' width='500' style='display:\
             block; margin: 10px auto;'>"
        "<p>See detailed analytics on how each product is performing in terms of sales, customer reviews, and more.</p>"
        "<h2 style='color: #4A90E2;'>Customer Preferences</h2>"
        "<img src='https://cdn-icons-png.flaticon.com/512/10754/10754236.png' width='500' style='display:\
             block; margin: 10px auto;'>"
        "<p>Understand what your customers are looking for with our in-depth analysis of buying patterns \
            and preferences.</p>"
        "<h2 style='color: #4A90E2;'>Market Trends</h2>"
        "<img src='https://cdn-icons-png.flaticon.com/512/10103/10103208.png' width='500' style='display:\
             block; margin: 10px auto;'>"
        "<p>Stay ahead of the curve by exploring the latest trends shaping your industry.</p>"
        "<p>If you have any questions or need further assistance, please don't hesitate to reach out to\
            our team.</p>"
        "<p style='color: #888; font-size: 0.9em;'>Best regards,<br>Your Stealth Startup Team</p>"
        "</div>",
        subtype="html",
    )

    return message


@celery.task(name="send_report_task")
def send_report(recipient_email: str):
    time.sleep(random.uniform(3, 10))  # emulate generation
    email_message = get_email_template_dashboard(recipient_email)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email_message)
