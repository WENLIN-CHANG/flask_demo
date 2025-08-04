from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get('q', '沒有搜索詞')
    return render_template("search.html", query=query)

@app.route("/user/<username>/<int:user_id>")
def user_profile(username, user_id):
    return render_template("user_profile.html", username=username, user_id=user_id)

@app.route("/<about>")
def hello(about):
    return f"Hello, {escape(about)}!"
