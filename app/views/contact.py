from flask import Blueprint, render_template, request
from app.database import db
from app.models.contact import ContactMessage

contact_bp = Blueprint('contact', __name__)

@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # 獲取表單數據
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # 簡單的驗證
        if name and email and message:
            # 保存到資料庫
            contact_msg = ContactMessage(name=name, email=email, message=message)
            db.session.add(contact_msg)
            db.session.commit()
            success_message = f"謝謝 {name}！我們已收到你的訊息並保存到資料庫"
            return render_template("contact.html", message=success_message)
        else:
            error_message = "請填寫所有欄位"
            return render_template("contact.html", message=error_message)
    # GET請求時顯示空白表單
    return render_template("contact.html")

@contact_bp.route("/messages")
def messages():
    # 從資料庫取出所有訊息
    all_messages = ContactMessage.query.all()
    return render_template("messages.html", messages=all_messages)