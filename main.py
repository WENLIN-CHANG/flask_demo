import os
from app import create_app

# 獲取配置環境
config_name = os.environ.get('FLASK_ENV', 'development')

# 創建應用實例
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True)