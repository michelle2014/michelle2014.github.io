import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

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
    """Show portfolio of stocks"""

    # Get symbol, name, price and sum shares and sum of each stock
    stocks = db.execute("SELECT symbol, name, price, SUM(shares) AS shares, sum(sum) AS sum FROM transactions WHERE id=:id GROUP BY symbol",
                        id=session['user_id'])

    for stock in stocks:

        symbol = stock["symbol"]
        name = stock["name"]
        price = stock["price"]

    # Get cash from users table
    cashRow = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])

    cashTotal = cashRow[0]["cash"]

    # Get sum of all stock purchased
    amounts = db.execute("SELECT sum, SUM(sum) AS quantity FROM transactions WHERE id=:id", id=session['user_id'])

    sum = amounts[0]["quantity"]

    sum = float(0 if sum is None else sum)

    # Cash left after all purhcase
    cash = cashTotal - sum

    return render_template("index.html", stocks=stocks, cash=cash, cashTotal=cashTotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # If no symbol input
        if not symbol:
            return apology("missing symbol", 400)

        # If no shares input
        if not shares:
            return apology("missing shares", 400)

        # If shares input is fractional or non-numeric
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Shares must be a posative integer", 400)

        # If shares input is negative
        if int(request.form.get("shares")) < 0:
            return apology("Shares must be a posative integer", 400)

        # If symbol not found
        stock = lookup(symbol)

        if stock == None:
            return apology("Invalid symbol", 400)

        # Check if enough cash to buy
        id = db.execute("SELECT * FROM users WHERE id=:id", id=session['user_id'])

        cash = id[0]["cash"]

        price = stock["price"]

        shareNumber = int(shares)

        amount = price * shareNumber

        remain = cash - amount

        if remain < 0:
            return apology("Can't afford")

        # Current date and time
        now = datetime.now()

        # Insert purchase details into transactions table
        db.execute("INSERT INTO transactions (id, symbol, name, shares, price, sum, time) VALUES(:id, :symbol, :name, :shares, :price, :sum, :time);",
                   id=session['user_id'], symbol=request.form.get("symbol"), name=stock["name"], shares=request.form.get("shares"),
                   price=stock["price"], sum=amount, time=now.strftime("%Y-%m-%d, %H:%M:%S"))

        # Flash message of bought
        flash('Bought!')

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    if request.method == "GET":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.args.get("username"))
        username = request.args.get("username")

        # Ensure username exists and password is correct
        if len(rows) == 0 and len(username) >= 1:
            return jsonify(True)

        else:
            return jsonify(False)

    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    stocks = db.execute("SELECT * FROM transactions WHERE id=:id", id=session['user_id'])

    # Ff have purchased, then display purchase info
    if stocks is not None:

        for stock in stocks:

            symbol = stock["symbol"]

            shares = stock["shares"]

            price = stock["price"]

            transacted = stock["time"]

        return render_template("history.html", stocks=stocks, symbol=symbol, shares=shares, price=price, transacted=transacted)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get symbol input
        symbol = request.form.get("symbol")

        # If no symbol input
        if not symbol:
            return apology("missing symbol", 400)

        quoted = lookup(symbol)

        # If symbol not found
        if quoted == None:
            return apology("Invalid symbol", 400)

        return render_template("quoted.html", quoted=quoted)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("missing username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("missing password", 400)

        # Ensure password was confirmed and correct
        elif not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # If username is already in users table
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 0:

            return apology("username taken", 400)

        # If username not in users table, then register succeeds and insert new user info into users table
        else:

            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash);",
                       username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        flash('Registered!')

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get symbol and shares input
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # If no symbol input
        if not symbol:
            return apology("missing symbol", 400)

        # If no shares input
        if not shares:
            return apology("missing shares", 400)

        stocks = db.execute("SELECT shares, sum FROM transactions WHERE id=:id AND symbol=:symbol",
                            id=session['user_id'], symbol=request.form.get("symbol"))

        # Initize shares available and sum in total
        sharesAvailable = 0
        sumTotal = 0

        # Loop through stocks and get sums
        for stock in stocks:

            sharesAvailable += stock["shares"]
            sumTotal += stock["sum"]

        # If not enough shares to sell
        if int(shares) > sharesAvailable:
            return apology("Too many shares", 400)

        # Update shares available
        sharesUpdate = sharesAvailable - int(shares)

        quote = lookup(symbol)

        # Get latest price
        price = quote["price"]

        # Get cash sum from selling
        sumSold = int(shares) * price

        # Get cash left
        sumAvailable = sumTotal - sumSold

        # Update transactions after selling
        db.execute("UPDATE transactions SET shares = :sharesUpdate, sum = :sumAvailable WHERE id=:id AND symbol=:symbol",
                   id=session['user_id'], symbol=request.form.get("symbol"), sharesUpdate=sharesUpdate, sumAvailable=sumAvailable)

        # If all shares of stock is sold out, delete the stock row
        db.execute("DELETE FROM transactions WHERE shares = '0'")

        flash('Sold!')

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        stocks = db.execute("SELECT * FROM transactions WHERE id=:id GROUP BY symbol", id=session['user_id'])

        for stock in stocks:

            symbol = stock["symbol"]

        return render_template("sell.html", stocks=stocks, symbol=symbol)


@app.route("/addCash", methods=["GET", "POST"])
@login_required
def addCash():
    """Add cash."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get cash amount requested to add
        amount = request.form.get("amount")

        # Check if amount input
        if not amount:
            return apology("missing amount", 400)

        # If amount input is fractional or non-numeric
        try:
            amount = int(request.form.get("amount"))
        except ValueError:
            return apology("Amount must be a posative integer", 400)

        # If amount input is negative
        if int(request.form.get("amount")) < 0:
            return apology("Amount must be a posative integer", 400)

        # Get cash in total from users table
        cashRow = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])

        cashTotal = cashRow[0]["cash"]

        # Add new cash
        cashNew = cashTotal + int(amount)

        # Update cash in total
        db.execute("UPDATE users SET cash = :cashNew WHERE id=:id", id=session['user_id'], cashNew=cashNew)

        return redirect("/")

    else:
        return render_template("addCash.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
