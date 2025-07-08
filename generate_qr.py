import qrcode

# for "Life Goals & Planning" this title
email = "tanishqsakhare@gmail.com"
event_title = "Life Goals & Planning"
event_date = "2025-07-09"

data = f"{email}|{event_title}|{event_date}"
img = qrcode.make(data)
img.save("test1_qr.png")

print("✅ QR code saved as test1_qr.png")


# for "AI & Future Careers" this title
email = "tanishqsakhare@gmail.com"
event_title = "AI & Future Careers"
event_date = "2025-07-21"

data = f"{email}|{event_title}|{event_date}"
img = qrcode.make(data)
img.save("test2_qr.png")

print("✅ QR code saved as test2_qr.png")

# for "How to Think Different?" this title
email = "tanishqsakhare@gmail.com"
event_title = "How to Think Different?"
event_date = "2025-07-31"

data = f"{email}|{event_title}|{event_date}"
img = qrcode.make(data)
img.save("test3_qr.png")

print("✅ QR code saved as test3_qr.png")