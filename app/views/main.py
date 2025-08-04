from flask import Blueprint, render_template, request
from markupsafe import escape

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def hello_world():
    return render_template("index.html")

@main_bp.route("/search")
def search():
    query = request.args.get('q', '沒有搜索詞')
    return render_template("search.html", query=query)

@main_bp.route("/user/<username>/<int:user_id>")
def user_profile(username, user_id):
    return render_template("user_profile.html", username=username, user_id=user_id)