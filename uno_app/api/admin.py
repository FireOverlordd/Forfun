from flask import Blueprint, render_template, request, redirect, url_for

from uno_app.models.player_model import Player

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/", methods=["GET", "POST"])
def admin():
    players = Player.objects().order_by("-wins")
    errors = {}
    total_wins = sum(player.wins for player in players)

    return render_template("admin.html", players=players, errors=errors, total_wins=total_wins)


@admin_bp.route("add-player", methods=["POST"])
def add_player():
    players = Player.objects()
    errors = {}

    if request.method == "POST":
        name = request.form.get("name")

        #1. name already used
        if Player.objects(name=name).first():
            errors["common"] = "Name gibt es bereits"

        if errors:
            return render_template("admin.html", players=players, errors=errors)
        
        player = Player(
            name=name,
            wins=1
        )

        player.save()
        players = Player.objects()

    return redirect(url_for('admin.admin'))



@admin_bp.route("add-win", methods=["POST"])
def add_win():
    player_id = request.form.get("player_id")
    player = Player.objects(id=player_id).first()

    player.wins += 1
    player.save()

    return redirect(url_for('admin.admin'))