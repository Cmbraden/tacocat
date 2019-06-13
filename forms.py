from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists')


class RegisterForm(Form):
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )

    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ]
    )

    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'password',
        validators=[
            DataRequired()
        ]
    )


class TacoForm(Form):
    protein = StringField(
        'protein',
        validators=[DataRequired()]
    )
    shell = StringField(
        'shell',
        validators=[DataRequired()]
    )
    cheese = BooleanField(
        'cheese',
        validators=[DataRequired()]
    )
    extras = StringField(
        'extras',
        validators=[DataRequired(),Length(100)]
    )