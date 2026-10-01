from flask import Blueprint, render_template, request, redirect, url_for

from forfun_app.models.player_model import Player

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def home():
    players = Player.objects().order_by("-wins")
    total_wins = sum(player.wins for player in players)

    return render_template("index.html", players=players, total_wins=total_wins)
