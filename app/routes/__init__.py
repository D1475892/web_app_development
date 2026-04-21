from flask import Blueprint

def register_blueprints(app):
    """將各個模組註冊進主 Flask 應用中"""
    from .main import bp as main_bp
    from .income import bp as income_bp
    from .expense import bp as expense_bp
    from .report import bp as report_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(report_bp)
