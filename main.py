from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from forms import HomeForm, RegisterForm, LoginForm, NoteForm
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_KEY")
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bcrypt(app)
ckeditor = CKEditor(app)


class User(UserMixin):
    def __init__(self, id, name, surname, email, password):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.is_authenticated()

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    with (sqlite3.connect("user_info.db")) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM USERS WHERE ID = ?''', [user_id])
        user = cur.fetchone()
        if user is None:
            return None
        else:
            return User(int(user[0]), user[1], user[2], user[3], user[4])


@app.route("/", methods=["GET", "POST"])
def home():
    form = HomeForm()
    if request.method == "POST":
        if request.form.get("register_btn") == "register":
            return redirect(url_for("register"))
        elif request.form.get("login_btn") == "login":
            return redirect(url_for("login"))
    return render_template("index.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.is_submitted():
        with sqlite3.connect("user_info.db") as conn:
            cur = conn.cursor()
            password = generate_password_hash(form.register_password.data, 15)
            params = (form.register_name.data, form.register_surname.data, form.register_email.data, password)
            cur.execute(f'''INSERT INTO USERS (ID, NAME, SURNAME, EMAIL, PASSWORD)
                            VALUES (NULL,
                                    ?, 
                                    ?, 
                                    ?,
                                    ?)''', params)
            conn.commit()
        flash("You have successfully registered. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        with sqlite3.connect("user_info.db") as conn:
            cur = conn.cursor()
            cur.execute('''SELECT * FROM USERS WHERE EMAIL = ?''', [form.login_email.data])
            user = list(cur.fetchone())
            us = load_user(user[0])
        if check_password_hash(us.password, form.login_password.data):
            login_user(us)
            return redirect(url_for("notes"))
    return render_template("login.html", form=form)


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    form = NoteForm()
    if form.is_submitted():
        with sqlite3.connect("user_info.db") as conn:
            cur = conn.cursor()
            params = (current_user.id, form.note_text.data)
            cur.execute(f'''INSERT INTO NOTES (ID, USER_ID, NOTE_TEXT)
                            VALUES (NULL,
                                    ?,
                                    ?);''', params)
            conn.commit()
            return redirect(url_for("home"))
    return render_template("notes.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

