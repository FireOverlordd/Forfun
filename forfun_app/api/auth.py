from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from forfun_app.utils.decorators import admin_required
from forfun_app.utils.hash import Hash
from forfun_app.models.user_model import User
from forfun_app.models.player_model import Player

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    errors = {}

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.objects(username=username).first()

        #1. password or username incorrect
        if not user or not Hash.check(password, user.password):
            errors["common"] = "Username or password incorrect"
            return render_template("login.html", errors=errors)

        login_user(user, remember=True)

        if user.is_admin:
            return redirect(url_for("admin.admin"))

        return redirect(url_for("main.home"))
    return render_template("login.html", errors=errors)


@auth_bp.route("/register", methods=["GET", "POST"])
@admin_required
def register():

    errors = {}

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")


        #1. empty field
        if not username or not password:
            errors["common"] = "Field must be filled"

        #2. username already exists
        if User.objects(username=username).first():
            errors["register"] = "Username already exists"

        #3. password false repeated
        if password != repassword:
            errors["password"] = "Passwords are not equal"

        #4. password too short
        if password and len(password) < 8:
            errors["password"] = "Password must be at least 8 characters long"

        if errors:
            return render_template("register.html", errors=errors, username=username)
        else:
            user = User(
                username=username,
                password=Hash.hash(password)
            )
            user.save()

        return redirect(url_for("main.home"))
    return render_template("register.html", errors=errors)

