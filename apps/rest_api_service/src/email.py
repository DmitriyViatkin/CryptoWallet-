import aiosmtplib
from email.message import EmailMessage

from config.infra.config.base_settings import get_infra_settings

async def _send(msg: EmailMessage) -> None:
    settings = get_infra_settings()
    smtp = settings.smtp
    await aiosmtplib.send(
        msg,
        hostname=smtp.HOST,
        port=smtp.PORT,
        username=smtp.USER,
        password=smtp.PASSWORD,
        use_tls=smtp.USE_TLS,
        start_tls=not smtp.USE_TLS,
    )


async def send_reset_email_smtp(to_email: str, reset_token: str) -> None:
    settings = get_infra_settings()
    smtp = settings.smtp

    reset_token= f" token={reset_token}"

    msg = EmailMessage()
    msg["From"] = smtp.FROM_EMAIL or smtp.USER or "noreply@example.com"
    msg["To"] = to_email
    msg["Subject"] = "Password reset"
    msg.set_content(
        f"Reset your password here:\n{reset_token}\n\nLink expires in 30 minutes."
    )
    msg.add_alternative(
        f"<p>Click to reset your password:</p>"
        f'token={reset_token}'
        f"<p>token  expires in 30 minutes.</p>",
        subtype="html",
    )

    await _send(msg)

async def send_email(to_email:str, subject:str, body:str):

    settings = get_infra_settings()
    smtp = settings.smtp
    text= body

    msg = EmailMessage()
    msg["From"] = smtp.FROM_EMAIL or smtp.USER or "noreply@example.com"
    msg["To"] = to_email
    msg["Subject"] = "Password reset"
    msg.set_content(
        f"Reset your password here:\n{text}\n\nLink expires in 30 minutes."
    )
    msg.add_alternative(
        f"<p>Click to reset your password:</p>"
        f'{text}',

        subtype="html",
    )

    await _send(msg)

