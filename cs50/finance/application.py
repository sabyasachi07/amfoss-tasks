import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT symbol, name, shares FROM stocks WHERE user_id = ? order by symbol", session["user_id"])

    stock_total = 0
    for row in rows:
        current_price = lookup(row["symbol"])["price"]
        total = current_price*int(row["shares"])
        row["current_price"] = usd(current_price)
        row["total"] = usd(total)
        stock_total += total

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    total = cash + stock_total

    return render_template("index.html", rows = rows, cash = usd(cash), total = usd(total))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":


        quote = lookup(request.form.get("symbol"))

        if not request.form.get("symbol"):
            return apology("missing symbol")

        elif not quote:
            return apology("invalid symbol")

        elif not request.form.get("shares"):
            return apology("missing shares")

        elif not str.isdigit(request.form.get("shares")):
            return apology("invalid shares")

        elif int(request.form.get("shares")) <= 0:
            return apology("invalid shares")

        name = quote["name"]

        rows = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"] )

        price_per_share = quote["price"]

        total_price = float(price_per_share)*int(request.form.get("shares"))

        available_cash = float(db.execute("SELECT cash FROM users WHERE id = ?",  session["user_id"])[0]["cash"])

        if available_cash < total_price:
            return apology("not enought cash! can't afford")

        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?",  available_cash - total_price,  session["user_id"] )


            flash("Congratulations! Transaction is successful!")

            db.execute("INSERT INTO transactions ( user_id, name, shares, price_per_share, total_price, transacted, symbol) VALUES(?, ?, ?, ?, ?, ?, ?)",
                         session["user_id"], name,  int(request.form.get("shares")), price_per_share, total_price, datetime.date.today(), str.upper(request.form.get("symbol")))

            instock = db.execute("SELECT symbol FROM stocks WHERE user_id = ? and symbol = ?",  session["user_id"],  str.upper(request.form.get("symbol")))


            if  not instock:
                db.execute("INSERT INTO stocks (user_id, symbol, name, shares) VALUES(?, ?, ?, ?)", session["user_id"], str.upper(request.form.get("symbol")), name, int(request.form.get("shares")))
            else:
                rows = db.execute("SELECT shares FROM stocks WHERE user_id = ? and symbol = ?",  session["user_id"], str.upper(request.form.get("symbol")))

                db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? and symbol = ?", int(rows[0]["shares"]) + int(request.form.get("shares")), session["user_id"], str.upper(request.form.get("symbol")))


        return redirect("/")

    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, name, shares, price_per_share, total_price, transacted FROM transactions WHERE user_id= ?", session["user_id"])

    if not rows:
        return apology("sorry you have no transactions on record")

    for row in rows:
        row["price_per_share"] = usd(row["price_per_share"])
        row["total_price"] = usd(row["total_price"])


    return render_template("history.html", rows= rows)


@app.route("/login", methods=["GET", "POST"])
def login():


    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        session["user_id"] = rows[0]['id']

        return redirect("/")

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
    if request.method == "POST":


        if not request.form.get("quote"):
            return apology("Missing symbol")
        else:
            quote=lookup(request.form.get("quote"))

            if not quote:
                return apology("Invalid symbol")
            else:
                return render_template("quoted.html", quote = quote, price = usd(quote["price"]) )
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and password confirmation must match")

        username = request.form.get("username")
        password = request.form.get("password")
        hashedpassword = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)


        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if  len(rows) == 1:
            return apology("username is already registered")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashedpassword)

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
        if request.method == "POST":

            quote = lookup(request.form.get("symbol"))

            if not request.form.get("symbol"):
                return apology("missing symbol")

            elif not quote:
                return apology("invalid symbol")

            elif not request.form.get("shares"):
                return apology("missing shares")

            elif not str.isdigit(request.form.get("shares")):
                return apology("invalid shares")

            elif int(request.form.get("shares")) <= 0:
                return apology("invalid shares")

            name = quote["name"]

            rows = db.execute("SELECT shares FROM stocks WHERE user_id = ? and symbol = ?", session["user_id"], str.upper(request.form.get("symbol")))

            if not rows or int(request.form.get("shares")) > int(rows[0]["shares"]):
                return apology("don't have enough shares to sell")

            else:
                if int(rows[0]["shares"]) == int(request.form.get("shares")):
                    db.execute("DELETE FROM stocks WHERE user_id = ? and symbol = ?", session["user_id"], str.upper(request.form.get("symbol")))

                db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? and symbol = ?", int(rows[0]["shares"]) - int(request.form.get("shares")), session["user_id"], str.upper(request.form.get("symbol")))

                flash("Sold! Transaction is succesful!")

                price_per_share = float(quote["price"])
                total_value = price_per_share*int(request.form.get("shares"))


                db.execute("INSERT INTO transactions (user_id, name, shares, price_per_share, total_price, transacted, symbol) VALUES(?, ?, ?, ?, ?, ?, ?)", \
                            session["user_id"],name, "-" + request.form.get("shares"),  price_per_share, total_value, datetime.date.today(), str.upper(request.form.get("symbol")))

                rows = db.execute("SELECT cash FROM users WHERE id = ?",  session["user_id"])
                db.execute("UPDATE users SET cash = ? WHERE id = ?", rows[0]["cash"] + total_value, session["user_id"])


                return redirect("/")

        else:
            return render_template("sell.html")

@app.route("/add_cash", methods = ["GET", "POST"])
@login_required
def add_cash():
    """Add cash to the account."""

    # ensure request methon is POST
    if request.method == "POST":

        # ensure cash amout was submitted
        if not request.form.get("add_cash"):
            return apology("missing amount of cash")

        # ensure amount of cash is numeric and greater then $0.01 and lesser then $100,000
        elif not str.isdigit(request.form.get("add_cash")) or float(request.form.get("add_cash")) < 0.01 \
             or float(request.form.get("add_cash")) > 100000:
             return apology("invalid amount of cash")

        # query database for username current cash
        rows = db.execute("SELECT cash FROM users WHERE id = ?",  session["user_id"])

        # update cash in users table for the user
        db.execute("UPDATE users SET cash = ? WHERE id = ?",  rows[0]["cash"] + float(request.form.get("add_cash")), session["user_id"])

        return redirect("/")


    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add_cash.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
