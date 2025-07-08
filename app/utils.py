import qrcode
import os
from flask_mail import Message
from . import mail
from flask import current_app
from PIL import Image
import cv2

def generate_qr_code(data, filename):
    qr = qrcode.make(data)
    qr_path = os.path.join("app", "static", "qrcodes", filename)
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    qr.save(qr_path)
    return qr_path

def send_confirmation_email(user_email, event_title, qr_path):
    msg = Message(
        subject=f"🎟️ Your Ticket for {event_title}",
        recipients=[user_email],
        body=f"Thanks for booking {event_title}!\nYour QR code is attached below.",
    )
    with open(qr_path, "rb") as qr_file:
        msg.attach("ticket.png", "image/png", qr_file.read())
    mail.send(msg)

def decode_qr_code(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return data if data else None
