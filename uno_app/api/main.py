from flask import Blueprint, render_template, request, redirect, url_for

from uno_app.models.player_model import Player

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def home():
    players = Player.objects()
    return render_template("index.html", players=players)
