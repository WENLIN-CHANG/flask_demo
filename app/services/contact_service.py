from app.database import db
from app.models.contact import ContactMessage

class ContactService:
    @staticmethod
    def create_message(name, email, message, user_id=None):
        """創建聯絡訊息"""
        if not all([name, email, message]):
            return None, "請填寫所有欄位"
        
        contact_msg = ContactMessage(
            name=name, 
            email=email, 
            message=message,
            user_id=user_id
        )
        
        db.session.add(contact_msg)
        db.session.commit()
        
        return contact_msg, f"謝謝 {name}！我們已收到你的訊息並保存到資料庫"
    
    @staticmethod
    def get_all_messages():
        """獲取所有聯絡訊息"""
        return ContactMessage.query.all()
    
    @staticmethod
    def get_messages_by_user(user_id):
        """根據用戶ID獲取訊息"""
        return ContactMessage.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_message_by_id(message_id):
        """根據ID獲取單個訊息"""
        return ContactMessage.query.get(message_id)