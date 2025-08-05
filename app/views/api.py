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