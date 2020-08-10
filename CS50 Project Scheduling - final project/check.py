
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
		
 <link rel="stylesheet" href="/resources/demos/style.css">