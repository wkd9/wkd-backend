from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()  # تحميل المتغيرات من .env

app = FastAPI()

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN")],  # مثال: https://username.github.io
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

@app.get("/")
async def health_check():
    return {"status": "OK", "message": "WKD Backend is running"}

@app.post("/send-email")
async def send_email(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    city: str = Form(...),
    brand: str = Form(...),
    message: str = Form(...),
):
    # بناء محتوى الإيميل
    msg = EmailMessage()
    msg["Subject"] = f"طلب امتياز جديد من {name}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(f"""
اسم المُرسل: {name}
البريد الإلكتروني: {email}
رقم الجوال: {phone}
المدينة: {city}
العلامة المطلوبة: {brand}

تفاصيل إضافية:
{message}
""")
    try:
        # إرسال الإيميل عبر SMTP SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return {"message": "تم إرسال الطلب بنجاح ✅"}
    except Exception as e:
        return {"error": f"فشل في الإرسال: {e}"}
