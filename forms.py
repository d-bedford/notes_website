from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField
from flask_ckeditor import CKEditorField


class HomeForm(FlaskForm):
    register_button = SubmitField(name="Register")
    login_button = SubmitField(name="Login")


class RegisterForm(FlaskForm):
    register_name = StringField()
    register_surname = StringField()
    register_email = EmailField()
    register_password = PasswordField()
    submit_button = SubmitField("Register")


class LoginForm(FlaskForm):
    login_email = StringField()
    login_password = PasswordField()
    login_submit = SubmitField("Login")


class NoteForm(FlaskForm):
    note_text = CKEditorField("Body")
    note_save = SubmitField("Save")

