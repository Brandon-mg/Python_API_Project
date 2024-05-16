# Simple async send email function using fastapi-mail 

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

enable_email = False
async def send_email_async(subject: str, attorney_email: str, prospect_email: str, body: dict):
    if enable_email:
        fm = FastMail(ConnectionConfig(MAIL_USERNAME = "username", MAIL_PASSWORD = "**********", MAIL_PORT = 587, MAIL_SERVER = "mail server", MAIL_SSL_TLS = False, TEMPLATE_FOLDER="./templates/"))
        await fm.send_message(MessageSchema(subject=subject, recipients=[attorney_email, prospect_email], body=body,subtype='html'), template_name="email.html")
    print(f"debug: sending email to {attorney_email} and {prospect_email}")
