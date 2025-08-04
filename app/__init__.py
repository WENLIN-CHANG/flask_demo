from flask import Flask
from config import config
from app.database import db

import os

def create_app(config_name='default'):
    """應用工廠函數"""
    # 設定模板和靜態文件路徑為專案根目錄
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # 加載配置
    app.config.from_object(config[config_name])
    
    # 初始化擴展
    db.init_app(app)
    
    # 註冊藍圖
    from app.views import register_blueprints
    register_blueprints(app)
    
    # 創建資料庫表格
    with app.app_context():
        db.create_all()
    
    return app