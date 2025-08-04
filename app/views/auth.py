from flask import Blueprint, render_template, request, session, redirect, url_for
from app.database import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
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

@auth_bp.route("/login", methods=['GET', 'POST'])
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
            return redirect(url_for('main.hello_world'))
        else:
            return render_template('login.html', message="用戶名或密碼錯誤")
        
    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('main.hello_world'))