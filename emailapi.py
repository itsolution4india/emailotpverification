from fastapi import FastAPI, HTTPException
import uvicorn
import random
import smtplib
import re
from email.message import EmailMessage

app = FastAPI()

OTP = {}

def generate_otp():
    """Generate a random 6-digit OTP."""
    otp = random.randint(100000, 999999)
    OTP[otp] = None
    return otp

def otp_verify(otp):
    """Verify if the OTP is correct."""
    if otp in OTP and OTP[otp] is None:
        OTP[otp] = "verified"
        return True
    return False

def is_valid_email(email):
    """Verify if the email is valid using regex pattern."""
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.search(regex, email) is not None

def setup_server():
    """Set up the SMTP server."""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    return server

def send_email(name, email, subject, body, server):
    """Send the email with the OTP."""
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@itsolution4india.com"
    msg["To"] = email

    server.send_message(msg)

def send_otp(name, email, server):
    """Send the OTP to the user's email."""
    otp = generate_otp()

    body = f"Dear {name},\n\nYour OTP is {otp}."
    subject = "OTP verification"
    send_email(name, email, subject, body, server)

    print("OTP has been sent to", email)

@app.post("/otp/")
async def send_otp_api(name: str, email: str):
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email ID")

    server = setup_server()
    password = "ioqd pldc jjlx dkmm"
    server.login("noreply@itsolution4india.com", password)

    try:
        send_otp(name, email, server)
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Error sending email")

    server.quit()
    return {"message": "OTP sent to your email"}

@app.post("/verify_otp/")
async def verify_otp_api(otp: int):
    if not otp_verify(otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"Account created successfully": "OTP verified"}

if __name__ == "__main__":
    uvicorn.run(app,host="192.168.29.200", port=5000, log_level="info")