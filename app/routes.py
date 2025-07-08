from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db, login_manager
from .forms import BookingForm
from .models import User, Event, Booking
from .forms import RegisterForm, LoginForm, EventForm
from .utils import generate_qr_code, send_confirmation_email, decode_qr_code
from .forms import QRUploadForm
import os
from flask import jsonify
from PIL import Image

main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page with event list and admin event creation
@main.route("/", methods=["GET", "POST"])
def index():
    events = Event.query.order_by(Event.date.asc()).all()
    form = EventForm()

    if current_user.is_authenticated and current_user.is_admin and form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for("main.index"))

    return render_template("index.html", events=events, form=form)

# User registration
@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        is_first_user = User.query.count() == 0
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw, is_admin=is_first_user)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

# User login
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.index"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

# Logout
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

# Event detail page
@main.route("/event/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()
    return render_template("event_detail.html", event=event, form=form)

# Book an event
@main.route("/book/<int:event_id>", methods=["POST"])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    existing = Booking.query.filter_by(user_id=current_user.id, event_id=event.id).first()
    if existing:
        flash("You've already booked this event.", "warning")
        return redirect(url_for("main.event_detail", event_id=event.id))

    # Use pipe | as a safe separator
    qr_data = f"{current_user.email}|{event.title}|{event.date.strftime('%Y-%m-%d')}"
    filename = f"{current_user.id}_{event.id}.png"
    qr_path = generate_qr_code(qr_data, filename)

    booking = Booking(user_id=current_user.id, event_id=event.id, qr_code_path=qr_path)
    db.session.add(booking)
    db.session.commit()

    send_confirmation_email(current_user.email, event.title, qr_path)
    flash("Booking successful! QR code sent to your email.", "success")
    return redirect(url_for("main.index"))

# Admin-only QR verification panel
@main.route("/verify", methods=["GET", "POST"])
@login_required
def verify_qr():
    if not current_user.is_admin:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))

    form = QRUploadForm()

    if form.validate_on_submit():
        file = form.qr_image.data
        filename = secure_filename(file.filename)
        path = os.path.join("app/static/uploads", filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file.save(path)

        qr_data = decode_qr_code(path)
        if qr_data:
            try:
                email, title, date = qr_data.split("|")
                booking = Booking.query.join(User).join(Event).filter(
                    User.email == email.strip(),
                    Event.title == title.strip()
                ).first()
                if booking:
                    booking.checked_in = True
                    db.session.commit()
                    flash(f"✅ Verified: {email} for {title}", "success")
                else:
                    flash("❌ Booking not found", "danger")
            except Exception:
                flash(f"⚠️ Invalid QR format: {qr_data}", "warning")
        else:
            flash("⚠️ Could not decode QR", "warning")

    return render_template("verify_qr.html", form=form)

# User's booking history
@main.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).join(Event).all()
    return render_template("my_bookings.html", bookings=bookings)

# Admin-only event editing
@main.route("/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for("main.index"))

    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash("Event updated!", "success")
        return redirect(url_for("main.index"))

    return render_template("edit_event.html", form=form)

# Admin-only event deletion
@main.route("/delete/<int:event_id>")
@login_required
def delete_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for("main.index"))

    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted.", "info")
    return redirect(url_for("main.index"))

#  Scan QR
@main.route("/scan")
@login_required
def scan_qr_page():
    if not current_user.is_admin:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))
    return render_template("scan_qr.html")

@main.route("/scan", methods=["POST"])
@login_required
def scan_qr_api():
    if not current_user.is_admin:
        return jsonify({"status": "danger", "message": "Access denied"})

    data = request.get_json()
    qr_data = data.get("qr_data")

    if qr_data:
        try:
            email, title, date = qr_data.split("|")
            booking = Booking.query.join(User).join(Event).filter(
                User.email == email.strip(),
                Event.title == title.strip()
            ).first()
            if booking:
                booking.checked_in = True
                db.session.commit()
                return jsonify({"status": "success", "message": f"✅ Verified: {email} for {title}"})
            else:
                return jsonify({"status": "danger", "message": "❌ Booking not found"})
        except Exception:
            return jsonify({"status": "warning", "message": f"⚠️ Invalid QR format: {qr_data}"})
    return jsonify({"status": "warning", "message": "⚠️ No QR data received"})

@main.route("/admin/bookings")
@login_required
def booking_history():
    if not current_user.is_admin:
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))

    bookings = Booking.query.order_by(Booking.timestamp.desc()).all()
    return render_template("admin_bookings.html", bookings=bookings)
