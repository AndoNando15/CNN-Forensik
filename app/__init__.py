from flask import Flask
from app.routes import routes  # mengimpor blueprint dari routes.py

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.register_blueprint(routes)
    return app
