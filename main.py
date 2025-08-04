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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # 獲取表單數據
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # 簡單的驗證
        if name and email and message:
        # 這裡可以處理數據（儲存到資料庫、發送郵件等）
            success_message = f"謝謝 {name}！我們已收到你的訊息，將會回覆到 {email}"
            return render_template("contact.html", message=success_message)
        else:
            error_message = "請填寫所有欄位"
            return render_template("contact.html", message=error_message)
    # GET請求時顯示空白表單
    return render_template("contact.html")