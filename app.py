import os
from datetime import datetime
from urllib.parse import urljoin, urlparse

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-insecure-key-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.instance_path, "pingsense.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "info"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()


# Curated YouTube channels, served via the /learn/recommendation API and
# rendered client-side on the /learn page.
CHANNELS = [
    {
        "id": "globalttstudio",
        "color": "c1",
        "initials": "GT",
        "avatar": (
            "https://yt3.googleusercontent.com/L62yqLvNhMSnbuqhaOtZaBvE2NUOZLCOp8x5_Mrcu4O4E74cSFRrkbNEr3cdGHJ-2kT6Xb0IoIk=s176-c-k-c0x00ffffff-no-rj"
        ),
        "name": "Global TT Studio",
        "handle": "@globalttstudio",
        "description": (
            "Dedicated to helping beginner and amateur table tennis enthusiasts "
            "build a solid foundation. Structured lessons, technique breakdowns, "
            "and training drills for all levels."
        ),
        "tags": ["Tutorials", "Beginner"],
        "url": "https://youtube.com/@globalttstudio?si=HIthb8KxZmJTIKfW",
    },
    {
        "id": "tabletennisreview",
        "color": "c2",
        "initials": "TTR",
        "avatar": (
            "https://yt3.googleusercontent.com/F2elGEmSHojZ31n9YCfO5STc28qQs4P76strwVocTylPoO7fAiGdu5R14qd-O60A8cZ5gd5P=s176-c-k-c0x00ffffff-no-rj"
        ),
        "name": "Table Tennis Review",
        "handle": "@tabletennisreview",
        "description": (
            "In-depth equipment reviews covering rubbers, blades, and accessories. "
            "Real on-table testing with honest assessments to help you choose the "
            "perfect gear for your game."
        ),
        "tags": ["Equipment", "Reviews"],
        "url": "https://youtube.com/@tabletennisreview?si=Mh5JlawOoaDwSxnj",
    },
    {
        "id": "hoangchopbongban",
        "color": "c3",
        "initials": "HC",
        "avatar": (
            "https://yt3.googleusercontent.com/f2xpF8muWiup88Bxrll4CXesbaNknpMaEWlSC0eApcmwUEapB6uQg0xlclQKzsHbUeoIphli=s176-c-k-c0x00ffffff-no-rj"
        ),
        "name": "Hoàng Chop Bóng Bàn",
        "handle": "@hoangchopbongban1776",
        "description": (
            "A vibrant Vietnamese table tennis channel featuring match highlights, "
            "training footage, and local tournament coverage. A great window into "
            "Southeast Asian ping pong culture."
        ),
        "tags": ["Vietnamese", "Matches"],
        "url": "https://youtube.com/@hoangchopbongban1776?si=BNjS-BZowYMbCg4n",
    },
    {
        "id": "pingsunday",
        "color": "c4",
        "initials": "PS",
        "avatar": (
            "https://yt3.googleusercontent.com/nd71dkAU7MEAh2JQJlJ7fw_ueDPGO_ZQt1DfvjXUEvaDgKAwqHI26g2g-NGqZJXtldm742SW=s176-c-k-c0x00ffffff-no-rj"
        ),
        "name": "PingSunday",
        "handle": "@pingsunday",
        "description": (
            "Coach EmRatThich's acclaimed channel teaching Chinese training methods "
            "and table tennis science. New lessons every Sunday, covering technique, "
            "strategy, and professional match analysis."
        ),
        "tags": ["Coaching", "Chinese Method"],
        "url": "https://youtube.com/@pingsunday?si=ZH3TKQ-S6XTMZZ7H",
    },
]


def is_safe_redirect(target):
    """Reject open-redirect targets that don't point back at this host."""
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/learn/recommendation")
def learn_recommendation():
    return jsonify(channels=CHANNELS)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        error = None
        if len(username) < 3:
            error = "Username must be at least 3 characters."
        elif "@" not in email or "." not in email:
            error = "Enter a valid email address."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif User.query.filter_by(username=username).first():
            error = "That username is already taken."
        elif User.query.filter_by(email=email).first():
            error = "An account with that email already exists."

        if error:
            flash(error, "error")
            return render_template("register.html", username=username, email=email)

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome to PingSense, {user.username}!", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            next_page = request.args.get("next")
            if is_safe_redirect(next_page):
                return redirect(next_page)
            return redirect(url_for("index"))

        flash("Invalid username/email or password.", "error")
        return render_template("login.html", identifier=identifier)

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
