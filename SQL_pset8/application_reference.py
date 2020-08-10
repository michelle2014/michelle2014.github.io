from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
 
from helpers import *
from datetime import datetime, date, time
 
# configure application
app = Flask(__name__)
 
# ensure responses aren't cached
if app.config["DEBUG"]:
@app.after_request
def after_request(response):
response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
response.headers["Expires"] = 0
response.headers["Pragma"] = "no-cache"
return response
 
# custom filter
app.jinja_env.filters["usd"] = usd
 
# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
 
@app.route("/")
@login_required
def index():
id=session["user_id"]
symbols=db.execute("SELECT symbol FROM indexes WHERE id=:sessioni", sessioni=id)
#return render_template("tmp.html", debug = symbols)
 
stock_list=[]
for sym in symbols:
symbol = sym['symbol']
share=db.execute("SELECT shares FROM indexes WHERE id=:sessioni AND symbol=:symbol", sessioni=id, symbol=symbol)[0]["shares"]
#share=db.execute("SELECT shares FROM indexes WHERE id=:sessioni AND symbol=:symbol", sessioni=id, symbol=symbol)
 
stock_info=lookup(symbol)
stock_data={}
stock_data['price']=stock_info["price"]
stock_data['name']=stock_info["name"]
stock_data['shares']=share
stock_data['total']=share*stock_data['price']
stock_data['symbol'] = symbol
 
stock_list.append(stock_data)
 
cash=db.execute("SELECT cash FROM users WHERE id=:sessioni", sessioni=id)[0]["cash"]
total= cash
for stock in stock_list:
total=stock['total']+total
 
return render_template("index.html", stocks=stock_list, cash=cash, total=total )
#table = ("INSERT INTO ")
#useri = db.execute("SELECT username FROM users")
#stockp = lookup("SELECT stock FROM progress")["price"]
#stockn = db.execute("SELECT stock FROM progress")
#valuet = int(db.execute("SELECT shares FROM progress"))*stockp
# return apology("TODO")
 
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
if request.method == "GET":
return render_template("buy.html")
 
if not request.form.get("Symbol"):
return apology("must provide stock symbol")
elif not request.form.get("shares"):
return apology("how many shares?")
if int(request.form.get("shares")) <= 0:
return apology("shares must be positive integers")
 
id=session["user_id"]
symbol = request.form.get("Symbol")
share = int(request.form.get("shares"))
 
if (lookup(symbol) == None):
return apology("must provide valid stock symbol")
moneyc = db.execute("SELECT cash FROM users WHERE id = :sessioni", sessioni = id)
moneyc =moneyc[0]["cash"]
 
stock = lookup(symbol)
 
purchase = stock["price"]*share
#check if the user has enough money left
if moneyc < purchase:
return apology("you have no money left")
 
#insert the progress information into the progress table
stockv=stock["name"]
db.execute("INSERT INTO progress (id, symbol, shares, price, type) Values(:id, :symbol, :shares, :price, :type)", id = id, symbol = symbol, shares = share, price = int(stock["price"]), type = "buy")
 
symbol_check = db.execute("SELECT * FROM indexes WHERE id=:sessioni AND symbol=:symbol", sessioni=id, symbol= symbol)
stock_index = db.execute("SELECT symbol FROM indexes WHERE id=:sessioni AND symbol=:symbol", sessioni=id, symbol= symbol)
share_user = db.execute("SELECT shares FROM indexes WHERE id=:sessioni AND symbol=:symbol", sessioni=id, symbol= symbol)
 
if not symbol_check:
db.execute("INSERT INTO indexes (id, symbol, shares) Values(:id, :symbol, :shares)", id = id, symbol = symbol, shares = share)
else:
shares_update = int(share_user[0]["shares"])+share
db.execute("UPDATE indexes SET shares=:shares WHERE id=:sessioni AND symbol=:symbol", shares = shares_update, symbol = symbol, sessioni=id)
 
moneyc = moneyc - purchase
db.execute("UPDATE users SET cash = :cash WHERE id = :sessioni", sessioni = id, cash = moneyc)
 
return render_template("buy.html")
 
@app.route("/history")
@login_required
def history():
id=session["user_id"]
 
stock_list=db.execute("SELECT symbol, shares, price, type FROM progress WHERE id=:sessioni", sessioni=id)
for stock in stock_list:
stock["price"] = usd(stock["price"])
return render_template("history.html", stocks=stock_list)
return apology("TODO")
 
@app.route("/login", methods=["GET", "POST"])
def login():
"""Log user in."""
 
# forget any user_id
session.clear()
 
# if user reached route via POST (as by submitting a form via POST)
if request.method == "POST":
 
# ensure username was submitted
if not request.form.get("username"):
return apology("must provide username")
 
# ensure password was submitted
elif not request.form.get("password"):
return apology("must provide password")
 
# query database for username
rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
 
# ensure username exists and password is correct
if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
return apology("invalid username and/or password")
 
# remember which user has logged in
session["user_id"] = rows[0]["id"]
 
# redirect user to home page
return redirect(url_for("index"))
 
# else if user reached route via GET (as by clicking a link or via redirect)
else:
return render_template("login.html")
 
@app.route("/logout")
def logout():
"""Log user out."""
 
# forget any user_id
session.clear()
 
# redirect user to login form
return redirect(url_for("login"))
 
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
if request.method == "POST":
if not request.form.get("Symbol"):
return render_template("quote.html")
else:
Symbol = lookup(request.form.get("Symbol"))
return render_template("quoted.html", Symbol=request.form.get("Symbol"), result=usd(lookup(request.form.get("Symbol"))["price"]), resultn=lookup(request.form.get("Symbol"))["name"])
elif request.method == "GET":
return render_template("quote.html")
return apology("TODO")
 
@app.route("/register", methods=["GET", "POST"])
def register():
"""Register user."""
if request.method == "POST":
if not request.form.get("username"):
return apology("must provide username")
elif not request.form.get("password"):
return apology("must provide password")
if not request.form.get("checkp") == request.form.get("password"):
return apology("passwords do not match")
 
hashp = pwd_context.encrypt(request.form.get("password"))
db.execute("INSERT INTO users (hash, username) Values(:hashp, :username)",
hashp=pwd_context.encrypt(request.form.get("password")), username = request.form.get("username"))
return render_template("login.html")
return render_template("register.html")
 
"""return apology("TODO")"""
 
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
if request.method == "GET":
return render_template("sell.html")
 
if not request.form.get("Symbol"):
return apology("must provide stock symbol")
elif not request.form.get("shares"):
return apology("how many shares?")
if int(request.form.get("shares")) <= 0:
return apology("shares must be positive integers")
 
id=session["user_id"]
 
symbol = request.form.get("Symbol")
share = int(request.form.get("shares"))
stock = lookup(symbol)
share_user = db.execute("SELECT shares FROM indexes WHERE id=:sessioni AND symbol =:symbol", sessioni=id, symbol=symbol )
 
if stock == None:
return apology("must provide valid stock")
if not share_user:
return apology("you do not own those stocks")
if share is None:
return apology("must provide positive integer")
if (lookup(symbol) == None):
return apology("must provide valid stock symbol")
if int(share_user[0]["shares"]) < share:
return apology("you don't have enough shares")
 
moneyc = db.execute("SELECT cash FROM users WHERE id = :sessioni", sessioni = id)
moneyc = moneyc[0]["cash"]
 
stock = lookup(symbol)
symbol_check = db.execute("SELECT symbol FROM indexes WHERE id=:sessioni AND symbol=:symbol", sessioni=id, symbol= symbol)
stock_index = db.execute("SELECT symbol FROM indexes WHERE id=:sessioni AND symbol=:symbol", sessioni=id, symbol= symbol)
shares_update = int(share_user[0]["shares"])-share
 
purchase = stock["price"]*share
#check if the user has enough money left
 
#insert the progress information into the progress table
stockv=stock["name"]
db.execute("INSERT INTO progress (id, symbol, shares, price, type) Values(:id, :symbol, :shares, :price, :type)", id = id, symbol = symbol, shares = share, price = int(stock["price"]), type = "sell")
 
shares_update = int(share_user[0]["shares"])-share
db.execute("UPDATE indexes SET shares=:shares WHERE id=:sessioni AND symbol=:symbol", shares = shares_update, symbol = symbol, sessioni=id)
 
if shares_update == 0:
db.execute("DELETE FROM indexes WHERE id=:sessioni AND symbol=:symbol AND shares=:shares", sessioni= id, symbol=symbol, shares=shares_update)
 
moneyc = moneyc + purchase
db.execute("UPDATE users SET cash = :cash WHERE id = :sessioni", sessioni = id, cash = moneyc)
 
return render_template("sell.html")