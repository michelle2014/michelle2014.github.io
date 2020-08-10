import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Registered students
students = []

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


# Get info from user input, if not input, show a warning message, if info, open csv file and write into memory
@app.route("/form", methods=["POST"])
def post_form():
    # # Get info from user input
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    house = request.form.get("house")
    position = request.form.get("position")
    # if not input, show a warning message
    if not firstname:
        return render_template("error.html", message="You must provide your first name!")
    elif not lastname:
        return render_template("error.html", message="You must provide your last name!")
    elif not house:
        return render_template("error.html", message="You must specify your house!")
    elif not position:
        return render_template("error.html", message="You must specify your position!")
    # if info, open csv file and and write into memory and then redirect to sheet page
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("firstname"), request.form.get("lastname"),
                     request.form.get("house"), request.form.get("position")))
    file.close()
    return redirect("/sheet")


# Open csv file and read through
@app.route("/sheet", methods=["GET"])
def get_sheet():
    # # Open csv file and read through it
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    # Append each to list
    students = list(reader)
    # return to sheet page to see list
    return render_template("sheet.html", students=students)

