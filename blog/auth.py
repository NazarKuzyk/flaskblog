from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import pbkdf2_sha256

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user:
            if pbkdf2_sha256.verify(password, user.password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Username does not exist.', category='warning')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('Username is already in use.', category='warning')
        elif password1 != password2:
            flash('Password don\'t match!', category='warning')
        elif len(username) < 2:
            flash('Username is too short.', category='warning')
        elif len(password1) < 4:
            flash('Password is too short.', category='warning')
        else:
            new_user = User(username=username, password=pbkdf2_sha256.hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
