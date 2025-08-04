def register_blueprints(app):
    """註冊所有藍圖"""
    from app.views.main import main_bp
    from app.views.auth import auth_bp
    from app.views.contact import contact_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)