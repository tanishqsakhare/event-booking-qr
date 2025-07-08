from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, Length
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    # Set format to match HTML5 datetime-local input
    date = DateTimeField("Date & Time", format="%Y-%m-%dT%H:%M", default=datetime.utcnow, validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    submit = SubmitField("Create Event")

class BookingForm(FlaskForm):
    submit = SubmitField("Book Now")

class QRUploadForm(FlaskForm):
    qr_image = FileField("Upload QR Code", validators=[
        DataRequired(),
        FileAllowed(["png", "jpg", "jpeg"], "Images only!")
    ])
    submit = SubmitField("Verify")