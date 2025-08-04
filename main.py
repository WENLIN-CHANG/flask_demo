from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# 資料庫配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_demo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化資料庫
db = SQLAlchemy(app)

# 用戶資料模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯：一個用戶可以有多個訊息
    messages = db.relationship('ContactMessage', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# 聯絡訊息資料模型
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯：關聯到用戶
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"<ContactMessage {self.name}>"

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
            contact_msg = ContactMessage(name=name, email=email, message=message)
            db.session.add(contact_msg)
            db.session.commit()
            success_message = f"謝謝 {name}！我們已收到你的訊息並保存到資料庫"
            return render_template("contact.html", message=success_message)
        else:
            error_message = "請填寫所有欄位"
            return render_template("contact.html", message=error_message)
    # GET請求時顯示空白表單
    return render_template("contact.html")

# 創建資料庫表格
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)