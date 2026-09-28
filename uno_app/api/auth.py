from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from uno_app.utils.decorators import admin_required
from uno_app.utils.hash import Hash
from uno_app.models.user_model import User
from uno_app.models.player_model import Player

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def home():
    players = Player.objects()
    return render_template("index.html", players=players)


@auth_bp.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    players = Player.objects()
    errors = {}

    if request.method == "POST":
        name = request.form.get("name")

        #1. name already used
        if Player.objects(name=name).first():
            errors["common"] = "Name gibt es bereits"

        if errors:
            render_template("admin.html", players=players, errors=errors)
        else:
            player = Player(
                name=name,
                wins=1
            )

            player.save()
            players = Player.objects()

    return render_template("admin.html", players=players, errors=errors)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.home"))


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
            return redirect(url_for("auth.admin"))

        return redirect(url_for("auth.home"))
    return render_template("login.html", errors=errors)


@auth_bp.route("/register", methods=["GET", "POST"])
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
            player = Player(
                name=username,
                wins = 1
            )

            user.save()
            player.save()

        return redirect(url_for("auth.login"))
    return render_template("register.html", errors=errors)

