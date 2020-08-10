# once get configured, just skip the first and second line
export FLASK_APP=application.py
export FLASK_DEBUG=1
flask run

@app.route("/show/<number>")
def show(number):
	return "You passed in {}".format(number)

# flask has a number of functions within its module
url_for()
redirect()
session()
render_template()

http://flask.pocoo.org/docs/0.12/quickstart/

http://jinja.pocoo.org/

var xhttp = new XMLHttpRequest();

# then define your onreadystatechange()

readyState has 5: 0 (request not yet initialized),1,2,3,4(request finished, response ready)

http://api.jquery.com/jquery.ajax/

