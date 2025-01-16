from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os

directory_library = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(directory_library, "data", "library.sqlite")}'

db.init_app(app)

"""with app.app_context():
    db.create_all()"""