from flask import Flask, render_template, url_for, flash, redirect
from Felder import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "59ee2f42ea064f2e8c9629eae97c080a"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#__________________________________ Database interaction __________________________________

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

#__________________________________ CONTENT 1 __________________________________

# Figure aus plt in flask
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
plt.style.use("seaborn")


#__________________________________ CONTENT 2 __________________________________

arr = np.random.randint(1,1000,1000)
arr = arr.reshape(4,250)
df = pd.DataFrame(arr)
graf = df.plot()

#__________________________________ HOME __________________________________

@app.route ("/")
@app.route ("/home")
def home():
	return render_template("home.html")

#__________________________________ KONTAKT __________________________________


@app.route ("/kontakt")
def about():
	return render_template("kontakt.html", title="about")

#__________________________________ REGISTRIEREN __________________________________

@app.route ("/registrieren", methods=["GET","POST"])
def registrieren():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f"Account erzeugt für {form.username.data}", "success")
		return redirect(url_for("home"))
	return render_template("registrieren.html", title="Registrieren", form=form)

#__________________________________ NEUIGKEITEN __________________________________

@app.route ("/neuigkeiten")
def neuigkeiten():
	return render_template("neuigkeiten.html", title="Neuigkeiten", news="News")

#__________________________________ PREISE __________________________________

@app.route ("/preise")
def preise():
	return render_template("preise.html", title="Preise")

#__________________________________ BILANZ __________________________________

@app.route ("/bilanz")
def bilanz():
	return render_template("bilanz_dashboard.html", title="Bilanz")


#__________________________________ LOGIN __________________________________

@app.route ("/login", methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == "alex@gmx.de" and form.password.data == "passwort":
			flash(f"Erfolgreich eingeloggt, willkommen zurück, {form.email.data}", "success")
			return redirect(url_for("home"))
		else:
			flash(f"Email oder Passwort ist falsch", "danger")
			return redirect(url_for("login"))
	return render_template("login.html", title="Login", form=form)

#__________________________________ JOBS __________________________________

@app.route ("/jobs")
def jobs():
	return render_template("jobs.html", title="Jobs")


if __name__ == '__main__':
	app.run(debug=True)


#HTML Kommentar
#<!-- _________________________________________________________-->

