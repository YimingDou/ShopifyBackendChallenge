from flask import Flask
from flask_jwt_extended import JWTManager
import pathlib

from auth import auth
from upload import upload
from model.common import db

app = Flask(__name__)

# TODO: Config file
app.config['UPLOAD_FOLDER'] = '/tmp/storage/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['JWT_SECRET_KEY'] = '0'  # TODO: Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

jwt = JWTManager(app)
db.init_app(app)
with app.app_context():
    db.create_all()
    print("Create all")

pathlib.Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(upload)
