from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 資料庫配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_demo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 會話管理配置
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 生產環境要改成隨機字串

# 初始化資料庫
db = SQLAlchemy(app)

# 用戶資料模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯：一個用戶可以有多個訊息
    messages = db.relationship('ContactMessage', backref='user', lazy=True)

    def set_password(self, password):
        """設置密碼雜湊"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """檢查密碼是否正確"""
        return check_password_hash(self.password_hash, password)
    
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
            # 保存到資料庫
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

@app.route("/messages")
def messages():
    # 從資料庫取出所有訊息
    all_messages = ContactMessage.query.all()
    return render_template("messages.html", messages=all_messages)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 驗證輸入
        if not all([username, email, password, confirm_password]):
            return render_template('register.html', message="請填寫所有欄位")
        
        if password != confirm_password:
            return render_template('register.html', message="密碼確認不一致")
        
        # 檢查用戶名是否已存在
        if User.query.filter_by(username=username).first():
            return render_template('register.html', message="用戶名已存在")
        
        # 檢查信箱是否已存在
        if User.query.filter_by(email=email).first():
            return render_template('register.html', message="信箱已被註冊")
        
        # 創建新用戶
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return render_template('register.html', message="註冊成功！請登入")
    
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', message="請填寫用戶名和密碼")
        
        # 查找用戶
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # 登入成功，設置會話
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('hello_world'))
        else:
            return render_template('login.html', message="用戶名或密碼錯誤")
        
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('hello_world'))


# 創建資料庫表格
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)