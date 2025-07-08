# 🎟️ Event Booking System with QR Code Check-In

A Flask-powered web application that allows users to book events and check in using QR codes. Admins can verify attendees via webcam scan or image upload, and manage booking history with ease.

---

## 🚀 Features

- 👤 User registration and login
- 📅 Event creation and listing (admin only)
- 🧾 Event booking with unique QR code generation
- 📲 QR code check-in via:
  - Live webcam scan
  - Image upload verification
- ✅ Admin dashboard for booking history and check-in status
- 🔐 CSRF-protected forms and role-based access control
- 🎨 Responsive UI with Bootstrap 5 and dark mode support

---

## 🛠️ Tech Stack

| Layer        | Tools Used                          |
|--------------|-------------------------------------|
| Backend      | Flask, Flask-WTF, SQLAlchemy        |
| Frontend     | HTML, CSS, Bootstrap 5, Jinja2      |
| Database     | SQLite                              |
| QR Handling  | qrcode, pyzbar / OpenCV, Pillow     |
| Auth & Forms | Flask-Login, Flask-WTF              |

---

## 🧪 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/event-booking-qr.git
   cd event-booking-qr
   ```

2. **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**
   ```bash
   python run.py
   ```

---

## 🔐 Admin Access

To access admin features like event creation and QR verification, log in with an admin account.  
You can manually set `is_admin=True` in the database for a user.

---

## 📈 Future Improvements

- 📧 Email confirmation with QR attachment
- 📤 Export booking data to CSV
- 🔍 Filter bookings by event or date
- 🌐 Deploy on Render or Heroku

---

## 🙌 Acknowledgements

Built with ❤️ using Flask and open-source libraries.

---

## 📬 Contact

Feel free to connect with me on LinkedIn or contribute to the project!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/tanishqsakhare)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=for-the-badge&logo=github)](https://github.com/tanishqsakhare)
[![Gmail](https://img.shields.io/badge/Gmail-red?style=for-the-badge&logo=gmail)](mailto:tanishqsakhare@gmail.com)

---   
