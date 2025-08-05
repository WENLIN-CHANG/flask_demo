from flask import Blueprint, jsonify, request
from app.database import db
from app.models.user import User
from app.models.contact import ContactMessage

# 創建API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 統一的JSON響應格式
def success_response(data=None, message="Success", status_code=200):
    """成功響應格式"""
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message="Error", status_code=400, errors=None):
    """錯誤響應格式"""
    response = {
        "success": False,
        "message": message,
        "errors": errors
    }
    return jsonify(response), status_code

# 測試API端點
@api_bp.route('/test', methods=['GET'])
def test_api():
    """測試API是否運作"""
    return success_response(
        data={"version": "1.0", "status": "running"},
        message="API is working!"
    )

# === 用戶管理API ===
@api_bp.route('/users', methods=['GET'])
def get_users():
    """獲取所有用戶"""
    users = User.query.all()
    user_data = [user.to_dict() for user in users]
    return success_response(data=user_data, message=f"找到{len(user_data)}個用戶")

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """取得特定用戶"""
    user = User.query.get(user_id)
    if not user:
        return error_response(message="用戶不存在", status_code=404)
    return success_response(data=user.to_dict(), message="用戶資料獲取成功")

@api_bp.route('/users', methods=['POST'])
def create_user():
    """創建新用戶"""
    # 取得JSON資料
    data = request.get_json()

    # 驗證必填欄位
    if not data:
        return error_response(message="請提供JSON資料", status_code=400)
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return error_response(message="請提供用戶名、電子郵件和密碼", status_code=400)
    
    # 檢查用戶名是否已存在
    if User.query.filter_by(username=username).first():
        return error_response(message="用戶名已存在", status_code=409)
    
    # 檢查電子郵件是否已存在
    if User.query.filter_by(email=email).first():
        return error_response(message="電子郵件已存在", status_code=409)
    
    # 創建新用戶
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return success_response(data=new_user.to_dict(), message="用戶創建成功", status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response("創建用戶失敗", status_code=500)
    
@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用戶資料"""
    user = User.query.get(user_id)
    if not user:
        return error_response("用戶不存在", status_code=404)
    
    data = request.get_json()
    if not data:
        return error_response("請提供JSON資料", status_code=400)
    
    # 更新用戶名（如果提供）
    if 'username' in data:
        # 檢查新用戶名是否與其他用戶衝突
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return error_response("用戶名已存在", status_code=409)
        user.username = data['username']
    
    # 更新電子郵件（如果提供）
    if 'email' in data:
        # 檢查新電子郵件是否與其他用戶衝突
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return error_response("電子郵件已存在", status_code=409)
        user.email = data['email']
    
    # 更新密碼（如果提供）
    if 'password' in data:
        user.set_password(data['password'])
    
    try:
        db.session.commit()
        return success_response(data=user.to_dict(), message="用戶資料更新成功")
    except Exception as e:
        db.session.rollback()
        return error_response("更新用戶資料失敗", status_code=500)
    
@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """刪除用戶"""
    user = User.query.get(user_id)
    if not user:
        return error_response("用戶不存在", status_code=404)
    
    try:
        # 保存要返回的用戶資料
        user_data = user.to_dict()

        # 刪除用戶
        db.session.delete(user)
        db.session.commit()
        return success_response(data=user_data, message="用戶刪除成功")
    except Exception as e:
        db.session.rollback()
        return error_response("刪除用戶失敗", status_code=500)
    
# === 聯絡人管理API ===
@api_bp.route('/contacts', methods=['GET'])
def get_contacts():
    """獲取所有聯絡人"""
    contacts = ContactMessage.query.all()
    contacts_data = [contact.to_dict() for contact in contacts]
    return success_response(data=contacts_data, message=f"找到{len(contacts_data)}則訊息")

@api_bp.route('/contacts', methods=['POST'])
def create_contact():
    """創建新聯絡訊息"""
    data = request.get_json()

    if not data:
        return error_response("請提供JSON資料", status_code=400)
    
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return error_response("請提供姓名、電子郵件和訊息", status_code=400)
    
    try:
        new_contact = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        return success_response(data=new_contact.to_dict(), message="聯絡訊息創建成功", status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response("創建聯絡訊息失敗", status_code=500)
    
    