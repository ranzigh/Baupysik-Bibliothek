from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	username = StringField("Benutzername", validators=[DataRequired(), Length(min=2,max=20)])

	email = StringField ("Email", validators=[DataRequired(), Email()])

	password = PasswordField ("Passwort", validators=[DataRequired()])

	confirm_password = PasswordField ("Passwort bestätigen", validators=[DataRequired(), EqualTo("password")])

	submit = SubmitField("Registrieren")

class LoginForm(FlaskForm):

	email = StringField ("Email", validators=[DataRequired(), Email()])

	password = PasswordField ("Passwort", validators=[DataRequired()])

	remember = BooleanField("Eingeloggt bleiben")

	submit = SubmitField("Einloggen")
