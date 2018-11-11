from datetime import datetime

from flask import Flask, url_for, redirect, render_template, request

from trainers import *

app = Flask(__name__)

@app.route("/friend_codes", methods=['GET', 'POST'])
def friend_codes():
	if request.method == "POST":
		name = request.form["name"]
		code = request.form["code"]
		location = request.form["location"]

		errors = []

		if code == "":
			errors.append("Trainer code is required")
		elif not code.isnumeric() or not (len(code) == 12):
			errors.append("Enter valid trainer code")

		else:
			when = datetime.utcnow()
			create_trainer(code, name, when, location)
			return redirect(url_for("friend_codes"))


		return render_template("friend_codes.html", trainers=get_trainers(limit=20), errors=errors, initial={"name": name, "code": code, "location": location})

	elif request.method == "GET":
		return render_template("friend_codes.html", trainers=get_trainers(limit=20), errors=[], initial={"name": "", "code": "", "location": ""})

@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route("/get_trainers", methods=["GET", "POST"])
def load_trainers():
	"""used for AJAX loading of codes"""
	html = ""
	mongo_id = request.get_json().get("mongo_id")
	trainers = get_trainers_belowid(id=mongo_id, limit=25)
	return render_template("get_trainers.html", trainers=trainers)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80, debug=True)
