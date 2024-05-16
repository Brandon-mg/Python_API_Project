from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

enable_email = False
async def send_email_async(subject: str, attorney_email: str, prospect_email: str, body: dict):
    if not enable_email:
        return
    message = MessageSchema(
        subject=subject,
        recipients=[attorney_email, prospect_email],
        body=body,
        subtype='html'
    )
    fm = FastMail(ConnectionConfig(MAIL_USERNAME = "username", MAIL_PASSWORD = "**********", MAIL_PORT = 587, MAIL_SERVER = "mail server", MAIL_SSL_TLS = False))
    await fm.send_message(message, template_name="email.html")

