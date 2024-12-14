from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Ism', validators=[DataRequired()])
    email = EmailField("Pochta", validators=[DataRequired()])
    password = PasswordField("Parol", validators=[DataRequired()])
    submit = SubmitField("ro'yxatdan o'tish")


class LoginForm(FlaskForm):
    email = EmailField("Pochta", validators=[DataRequired()])
    password = PasswordField("Parol", validators=[DataRequired()])
    submit = SubmitField("kirish")


