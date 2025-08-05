from datetime import datetime
from app.database import db

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
    
    def to_dict(self):
        """將聯絡人資料轉換為字典"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id
        }