import os

SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
SQLALCHEMY_DATABASE_URI = "sqlite:///eventbooking.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Email config (use Mailtrap or Gmail SMTP)
MAIL_SERVER = "smtp.mailtrap.io"
MAIL_PORT = 2525
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_USE_TLS = True
MAIL_USE_SSL = False
