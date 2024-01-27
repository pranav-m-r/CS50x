from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    sum = 0
    param = []
    for row in db.execute("SELECT * FROM current WHERE userid=?", session["user_id"]):
        param.append(row)
        price = lookup(row["symbol"])["price"]
        param[len(param) - 1]["price"] = price
        sum += price * row["shares"]
    balance = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    return render_template("index.html", rows=param, balance=balance, sum=sum)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to current balance"""

    if request.method == "POST":
        cash = float(request.form.get("amount"))
        if not cash or cash <= 0:
            return apology("must provide amount", 400)
        elif cash <= 0:
            return apology("invalid amount", 400)
        balance = float(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
        db.execute("UPDATE users SET cash=? WHERE id=?", balance + cash, session["user_id"])
        return redirect("/")

    else:
        return render_template("addcash.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        try:
            shares = float(request.form.get("shares"))
        except ValueError:
            return apology("invalid entry for shares", 400)
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not quote:
            return apology("invalid symbol", 400)
        elif shares <= 0 or shares % 1 != 0:
            return apology("invalid number of shares", 400)
        cost = quote["price"] * shares
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if cost > balance:
            return apology("insufficient balance", 400)
        if db.execute("SELECT * FROM current WHERE userid=? AND symbol=?", session["user_id"], quote["symbol"]):
            db.execute("UPDATE current SET shares=((SELECT shares FROM current WHERE userid=?)+?) WHERE userid=? AND symbol=?",
                       session["user_id"], shares, session["user_id"], quote["symbol"])
        else:
            db.execute("INSERT INTO current VALUES (?, ?, ?)", session["user_id"], quote["symbol"], shares)
        db.execute("INSERT INTO history (userid, type, symbol, price, shares, time) VALUES (?, 'Bought', ?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], quote["price"], shares, datetime.now())
        db.execute("UPDATE users SET cash=? WHERE id=?", balance - cost, session["user_id"])
        # row = {"symbol": quote["symbol"], "price": quote["price"], "shares": int(shares)}
        # return render_template("transaction.html", row = row)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT type, symbol, price, shares, time FROM history WHERE userid=? ORDER BY id DESC", session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        if request.form.get("symbol"):
            quote = lookup(request.form.get("symbol"))
            if quote:
                return render_template("quoted.html", quote=quote)
            else:
                return apology("invalid symbol", 400)
        else:
            return apology("must provide symbol", 400)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation do not match", 400)

        # Ensure username does not already exist
        elif len(rows) != 0:
            return apology("username already exists", 400)

        # Insert new user into database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password"))
        )

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        try:
            shares = float(request.form.get("shares"))
        except ValueError:
            return apology("invalid entry for shares", 400)
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not quote:
            return apology("invalid symbol", 400)
        elif shares <= 0 or shares % 1 != 0:
            return apology("invalid number of shares", 400)
        elif db.execute("SELECT shares FROM current WHERE userid=? AND symbol=?", session["user_id"], quote["symbol"])[0]["shares"] < shares:
            return apology("insufficient shares", 400)
        cost = quote["price"] * shares
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        db.execute("UPDATE current SET shares=((SELECT shares FROM current WHERE userid=?)-?) WHERE userid=? AND symbol=?",
                   session["user_id"], shares, session["user_id"], quote["symbol"])
        db.execute("INSERT INTO history (userid, type, symbol, price, shares, time) VALUES (?, 'Sold', ?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], quote["price"], shares, datetime.now())
        db.execute("UPDATE users SET cash=? WHERE id=?", balance + cost, session["user_id"])
        if db.execute("SELECT shares FROM current WHERE userid=? AND symbol=?", session["user_id"], quote["symbol"])[0]["shares"] == 0:
            db.execute("DELETE FROM current WHERE symbol=?", quote["symbol"])
        # row = {"symbol": quote["symbol"], "price": quote["price"], "shares": int(shares)}
        # return render_template("transaction.html", row = row)
        return redirect("/")

    else:
        symbols = db.execute("SELECT symbol FROM current WHERE userid=?", session["user_id"])
        return render_template("sell.html", rows=symbols)
