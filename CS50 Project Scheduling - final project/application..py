import os

from cs50 import SQL
from flask import Flask, flash, jsonify, json, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        select = request.form.get("options")

        if (select == 'statistics'):

            return render_template("index.html")

        elif (select == 'myProjects'):

            return redirect("/myprojects")

        elif (select == 'allProjects'):

            return redirect("/allprojects")

        elif (select == 'minutes'):

            return redirect("/minutes")

        elif (select == 'mymeetings'):

            return redirect("/mymeetings")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":

        users=db.execute("SELECT username FROM users WHERE id = :id", id=session['user_id'])

        projects = db.execute("SELECT * FROM projects WHERE id = :id", id=session['user_id'])

        numberProjects = 0

        for i in range(len(projects)):
            numberProjects += 1

        projects = db.execute("SELECT * FROM projects WHERE id = :id AND status = :status", id=session['user_id'], status="notstarted")

        numberNotStarted = 0

        for i in range(len(projects)):
            numberNotStarted += 1

        projects = db.execute("SELECT * FROM projects WHERE id = :id AND status = :status", id=session['user_id'], status="inprogress")

        numberInProgress = 0

        for i in range(len(projects)):
            numberInProgress += 1

        projects = db.execute("SELECT * FROM projects WHERE id = :id AND status = :status", id=session['user_id'], status="onhold")

        numberOnHold = 0

        for i in range(len(projects)):
            numberOnHold += 1

        projects = db.execute("SELECT * FROM projects WHERE id = :id AND status = :status", id=session['user_id'], status="cancelled")

        numberCancelled = 0

        for i in range(len(projects)):
            numberCancelled += 1


        projects = db.execute("SELECT * FROM projects WHERE id = :id AND status = :status", id=session['user_id'], status="completed")

        numberCompleted = 0

        for i in range(len(projects)):
            numberCompleted += 1

        projects = db.execute("SELECT * FROM projects")

        totalProjects = 0

        for i in range(len(projects)):
            totalProjects += 1

        projects = db.execute("SELECT * FROM projects WHERE status = :status", status="notstarted")

        totalNotStarted = 0

        for i in range(len(projects)):
            totalNotStarted += 1

        projects = db.execute("SELECT * FROM projects WHERE status = :status", status="inprogress")

        totalInProgress = 0

        for i in range(len(projects)):
            totalInProgress += 1

        projects = db.execute("SELECT * FROM projects WHERE status = :status", status="onhold")

        totalOnHold = 0

        for i in range(len(projects)):
            totalOnHold += 1

        projects = db.execute("SELECT * FROM projects WHERE status = :status", status="cancelled")

        totalCancelled = 0

        for i in range(len(projects)):
            totalCancelled += 1


        projects = db.execute("SELECT * FROM projects WHERE status = :status", status="completed")

        totalCompleted = 0

        for i in range(len(projects)):
            totalCompleted += 1

        projects = db.execute("SELECT * FROM projects WHERE status = :status", status="overdue")

        totalOverdue = 0

        for i in range(len(projects)):
            totalOverdue += 1

        # Get Python data to JavaScript google pie chart https://www.roytuts.com/google-pie-chart-using-python-flask/
        data = { 'Task' : 'Hours per Day', "Not Started": totalNotStarted, "In Progress": totalInProgress, "On Hold": totalOnHold,
                 "Cancelled": totalCancelled, "Completed": totalCompleted, "Overdue": totalOverdue }

        return render_template("index.html", users=users, numberProjects=numberProjects, numberNotStarted=numberNotStarted,
                               numberInProgress=numberInProgress, numberOnHold=numberOnHold, numberCancelled=numberCancelled,
                               numberCompleted=numberCompleted, totalProjects=totalProjects, totalNotStarted=totalNotStarted,
                               totalInProgress=totalInProgress, totalOnHold=totalOnHold, totalCancelled=totalCancelled,
                               totalCompleted=totalCompleted, totalOverdue=totalOverdue, data=data)


@app.route("/myprojects")
@login_required
def myprojects():
    """Show portoflio of my projects"""

    projects = db.execute("SELECT * FROM projects WHERE id = :id", id=session['user_id'])

    return render_template("myprojects.html", projects=projects)


@app.route("/allprojects", methods=["GET", "POST"])
@login_required
def allprojects():
    """Show portoflio of all projects"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        status = request.form.get("options")

        projects = db.execute("SELECT * FROM projects WHERE status = :status", status = request.form.get("options"))

        return render_template("allprojects.html", projects=projects)

    else:

        projects = db.execute("SELECT * FROM projects WHERE id = :id", id=session['user_id'])

        return render_template("allprojects.html", projects=projects)


@app.route("/mymeetings", methods=["GET", "POST"])
@login_required
def mymeetings():
    """Show portoflio of my meetings"""

    meetings = db.execute("SELECT * FROM meetings")

    return render_template("mymeetings.html", meetings=meetings)


@app.route("/createmeetings", methods=["GET", "POST"])
@login_required
def createmeetings():

    """Create new meetings"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get meeting title input
        title = request.form.get("title")
        organizer = request.form.get("organizer")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        status = request.form.get("status")

        # If no title input
        if not title:
            return apology("missing meeting title", 400)

        # If no organizer input
        if not organizer:
            return apology("missing organizer", 400)

        # If no date input
        if not date:
            return apology("missing datee", 400)

        # If no time input
        if not time:
            return apology("missing time", 400)

        # If no location input
        if not location:
            return apology("missing location", 400)

        # If no status input
        if not status:
            return apology("missing status", 400)

        # If meeting is already in users table
        rows = db.execute("SELECT * FROM meetings WHERE title = :title", title=request.form.get("title"))

        if len(rows) != 0:

            return apology("meeting title taken", 400)

        else:

            db.execute("INSERT INTO meetings (id, title, organizer, date, time, location, status) VALUES(:id, :title, :organizer, :date, :time, :location, :status);",
                       id=session['user_id'], title=request.form.get("title"), organizer = request.form.get("organizer"),
                       date = request.form.get("date"), time = request.form.get("time"),
                       location = request.form.get("location"), status = request.form.get("status"))

        flash('A Meeting Created!')

        meetings = db.execute("SELECT * FROM meetings")

        return render_template("mymeetings.html", meetings=meetings)

    else:

        return render_template("createmeetings.html", meetings=meetings)


@app.route("/titlecheck", methods=["GET"])
def titlecheck():
    """Return true if meeting title available, else false, in JSON format"""

    if request.method == "GET":

        # Query database for project name
        meetings = db.execute("SELECT * FROM meetings WHERE title = :title", title=request.args.get("title"))
        title = request.args.get("title")

        # Ensure username exists and password is correct
        if len(meetings) == 0 and len(title) >= 1:
            return jsonify(True)

        else:
            return jsonify(False)

    else:
        return jsonify(False)


@app.route("/minutes")
@login_required
def minutes():
    """Show portoflio of minutes"""

    return render_template("minutes.html")


@app.route("/invite", methods=["GET", "POST"])
@login_required
def invite():
    """Invite user into teams"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        db.execute("INSERT INTO teammates (id, team, architect, frontend, backend, tester, database, devops, mobile) VALUES(:id, :team, :architect, :frontend, :backend, :tester, :database, :devops, :mobile);",
                    id=session['user_id'], team=request.form.get("team"), architect=request.form.get("architect"), frontend= request.form.get("frontend"),
                    backend = request.form.get("backend"), tester = request.form.get("tester"), database = request.form.get("database"),
                    devops = request.form.get("devops"), mobile = request.form.get("mobile"))

        flash('Invited!')

        return render_template("invite.html")

    else:
        return render_template("invite.html")


@app.route("/teams", methods=["GET", "POST"])
@login_required
def teams():
    """Show info about teams"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        db.execute("INSERT INTO teams (id, teamname) VALUES(:id, :teamname);",
                    id=session['user_id'], teamname=request.form.get("teamname"))

        flash('A Team Created!')

        return render_template("teams.html")

    else:
        teammates = db.execute("SELECT * FROM teammates")

        return render_template("teams.html", teammates=teammates)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a project."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get project name input
        name = request.form.get("name")
        team = request.form.get("team")
        technology = request.form.get("technology")
        status = request.form.get("status")
        start = request.form.get("datepicker1")
        due = request.form.get("datepicker2")

        # If no name input
        if not name:
            return apology("missing project name", 400)

        # If no technology input
        if not technology:
            return apology("missing technology", 400)

        # If no start input
        if not start:
            return apology("missing start time", 400)

        # If no due input
        if not due:
            return apology("missing due time", 400)

        # If no team input
        if not team:
            return apology("missing team name", 400)

        # If no status input
        if not status:
            return apology("missing status", 400)

        # If project is already in users table
        rows = db.execute("SELECT * FROM projects WHERE name = :name", name=request.form.get("name"))

        if len(rows) != 0:

            return apology("project name taken", 400)

        else:

            db.execute("INSERT INTO projects (id, name, technology, start, due, team, status) VALUES(:id, :name, :technology, :start, :due, :team, :status);",
                       id=session['user_id'], name=request.form.get("name"), technology = request.form.get("technology"),
                       start = request.form.get("datepicker1"), due = request.form.get("datepicker2"),
                       team = request.form.get("team"), status = request.form.get("status"))

        flash('A Project Created!')

        teams = db.execute("SELECT * FROM teams")

        return render_template("create.html", teams=teams)

    else:

        teams = db.execute("SELECT * FROM teams")

        return render_template("create.html", teams=teams)


@app.route("/projectcheck", methods=["GET"])
def projectcheck():
    """Return true if project name available, else false, in JSON format"""

    if request.method == "GET":

        # Query database for project name
        projects = db.execute("SELECT * FROM projects WHERE name = :name", name=request.args.get("name"))
        name = request.args.get("name")

        # Ensure username exists and password is correct
        if len(projects) == 0 and len(name) >= 1:
            return jsonify(True)

        else:
            return jsonify(False)

    else:
        return jsonify(False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # user reached route via POST (as by submitting a form via POST)
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

    # user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # user reached route via POST (as by submitting a form via POST)
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

    # user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
