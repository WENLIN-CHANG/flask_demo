from PIL import Image
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """檢查檔案類型是否允許"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    """生成唯一的檔案名稱"""
    if filename == '':
        return None
    
    # 取得副檔名
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    # 生成唯一ID + 副檔名
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return unique_filename

def ensure_upload_folder(folder_name):
    """確保資料夾存在"""
    upload_folder = current_app.config['UPLOAD_FOLDER']
    avatar_folder = current_app.config['AVATAR_FOLDER']

    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(avatar_folder, exist_ok=True)

def resize_image(file_path, output_path, size=(150, 150)):
    """
    縮放圖片到指定尺寸
    :param file_path: 原始圖片路徑
    :param output_path: 輸出圖片路徑
    :param size: 目標尺寸 (寬, 高)
    """
    try:
        with Image.open(file_path) as img:
            # 轉換為RGB模式（處理RGBA或其他模式）
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # 保持比例縮放
            img.thumbnail(size, Image.Resampling.LANCZOS)

            # 創建正方形背景
            new_img = Image.new('RGB', size, (255, 255, 255))

            # 居中貼上縮放後的圖片
            paste_x = (size[0] - img.width) // 2
            paste_y = (size[1] - img.height) // 2
            new_img.paste(img, (paste_x, paste_y))

            # 保存圖片
            new_img.save(output_path, 'JPEG', quality=85, optimize=True)
            return True
    except Exception as e:
        print(f"處理圖片時發生錯誤: {str(e)}")
        return False

def create_thumbnail(file_path, output_path, size=(50, 50)):
    """創建縮圖"""
    return resize_image(file_path, output_path, size)