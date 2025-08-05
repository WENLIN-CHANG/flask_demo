from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db

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
    
    def to_dict(self):
        """將用戶資料轉換為字典"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }