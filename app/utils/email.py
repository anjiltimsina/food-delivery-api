from fastapi_mail import FastMail , MessageSchema , ConnectionConfig, MessageType
from app.core.config import settings
from app.core.security import create_access_token
from datetime import timedelta

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_TLS,
    MAIL_SSL_TLS=settings.MAIL_SSL,
    USE_CREDENTIALS=True
)

def create_verification_token(email:str)->str:
    return create_access_token(
        data ={"sub" : email , "type": "verification"},
        expires_delta = timedelta(hours= 24)
    )

def create_password_reset_token(email : str)->str:
    return create_access_token(
        data={"sub" : email , "type": "password_reset"},
        expires_delta = timedelta(hours=1)
    )

async def send_verification_email(email : str , full_name : str , token : str):
    verification_url = f"http://localhost:8001/auth/verify-email?token={token}"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #FF6B35; padding: 20px; border-radius: 10px; text-align: center;">
                <h1 style="color: white;">🍔 FoodDeliveryAPI</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hi {full_name}!</h2>
                <p>Thanks for registering! Please verify your email by clicking below:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}"
                       style="background-color: #FF6B35; color: white; padding: 15px 30px;
                              text-decoration: none; border-radius: 5px; font-size: 16px;">
                        Verify Email
                    </a>
                </div>
                <p style="color: #666;">This link expires in <strong>24 hours</strong>.</p>
                <p style="color: #666;">If you didn't create an account, ignore this email.</p>
            </div>
        </body>
    </html>
    """
    message = MessageSchema(
        subject="Verify your FoodDeliveryAPI email ✅",
        recipients=[email],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
async def send_password_reset_email(email: str, full_name: str, token: str):
    # We just show the token — user copies it and uses in Swagger
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #FF6B35; padding: 20px; border-radius: 10px; text-align: center;">
                <h1 style="color: white;">🍔 FoodDeliveryAPI</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hi {full_name}!</h2>
                <p>We received a request to reset your password.</p>
                <p>Your reset token is:</p>
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; word-break: break-all;">
                    <strong>{token}</strong>
                </div>
                <p style="color: #666; margin-top: 20px;">
                    Use this token in <strong>POST /auth/reset-password</strong>
                </p>
                <p style="color: #666;">This token expires in <strong>1 hour</strong>.</p>
                <p style="color: #666;">If you didn't request this, ignore this email.</p>
            </div>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Reset your FoodDeliveryAPI password 🔐",
        recipients=[email],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)