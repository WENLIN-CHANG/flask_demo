from app.database import db
from app.models.user import User

class AuthService:
    @staticmethod
    def create_user(username, email, password):
        """創建新用戶"""
        # 檢查用戶名是否已存在
        if User.query.filter_by(username=username).first():
            return None, "用戶名已存在"
        
        # 檢查信箱是否已存在
        if User.query.filter_by(email=email).first():
            return None, "信箱已被註冊"
        
        # 創建新用戶
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        
        return new_user, "註冊成功"
    
    @staticmethod
    def authenticate_user(username, password):
        """驗證用戶"""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user, True
        return None, False
    
    @staticmethod
    def get_user_by_id(user_id):
        """根據ID獲取用戶"""
        return User.query.get(user_id)