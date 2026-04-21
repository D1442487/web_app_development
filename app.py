import os
from flask import Flask
from app.models.models import db
from app.routes.main import main_bp
from app.routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 確保 instance 資料夾存在，並設定 SQLite 路徑
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_path, 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 1. 綁定 資料庫
    db.init_app(app)

    # 2. 註冊前台與後台路由 Blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    return app

app = create_app()

if __name__ == '__main__':
    # 若需在首次自動建立 tables，可取消下方註解
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True, port=5000)
