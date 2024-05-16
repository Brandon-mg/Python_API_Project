from config import Settings
from fastapi_mail import FastMail, MessageSchema

async def send_email_async(subject: str, attorney_email: str, prospect_email: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[attorney_email, prospect_email],
        body=body,
        subtype='html'
    )
    fm = FastMail(Settings.mail)
    await fm.send_message(message, template_name="email.html")

