from app import create_app

app = create_app()

from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

user = User.query.filter_by(email="someone@example.com").first()

if user:
    user.is_admin = True
    db.session.commit()
    print("✅ User promoted to admin.")
else:
    print("⚠️ No user found with that email.")


if __name__ == "__main__":
    app.run(debug=True)
