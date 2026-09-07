import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, get_user_by_email, get_user_by_id, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev"

with app.app_context():
    init_db()
    seed_db()


@app.context_processor
def inject_current_user():
    user_id = session.get("user_id")
    return {"current_user": get_user_by_id(user_id) if user_id else None}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template(
            "register.html", error="All fields are required.", name=name, email=email
        ), 400

    if len(password) < 8:
        return render_template(
            "register.html",
            error="Password must be at least 8 characters.",
            name=name,
            email=email,
        ), 400

    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return render_template(
            "register.html",
            error="An account with this email already exists.",
            name=name,
            email=email,
        ), 400

    password_hash = generate_password_hash(password)
    try:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return render_template(
            "register.html",
            error="An account with this email already exists.",
            name=name,
            email=email,
        ), 400
    conn.close()

    return redirect(url_for("login", registered=1))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template(
            "login.html", error="Invalid email or password.", email=email
        ), 400

    session["user_id"] = user["id"]
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    stats = {
        "total_spent": 280.53,
        "transaction_count": 8,
        "top_category": "Bills",
    }

    transactions = [
        {"date": "2026-09-21", "description": "Restaurant dinner", "category": "Food", "amount": 22.30},
        {"date": "2026-09-18", "description": "Miscellaneous", "category": "Other", "amount": 9.99},
        {"date": "2026-09-14", "description": "New shoes", "category": "Shopping", "amount": 60.00},
        {"date": "2026-09-11", "description": "Movie tickets", "category": "Entertainment", "amount": 15.75},
        {"date": "2026-09-08", "description": "Pharmacy", "category": "Health", "amount": 25.00},
        {"date": "2026-09-05", "description": "Electricity bill", "category": "Bills", "amount": 89.99},
        {"date": "2026-09-03", "description": "Bus pass", "category": "Transport", "amount": 12.00},
        {"date": "2026-09-02", "description": "Groceries", "category": "Food", "amount": 45.50},
    ]

    category_breakdown = [
        {"category": "Bills", "total": 89.99, "percent": 32},
        {"category": "Food", "total": 67.80, "percent": 24},
        {"category": "Shopping", "total": 60.00, "percent": 21},
        {"category": "Health", "total": 25.00, "percent": 9},
        {"category": "Entertainment", "total": 15.75, "percent": 6},
        {"category": "Transport", "total": 12.00, "percent": 4},
        {"category": "Other", "total": 9.99, "percent": 4},
    ]

    return render_template(
        "profile.html",
        member_since="March 2026",
        stats=stats,
        transactions=transactions,
        category_breakdown=category_breakdown,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
