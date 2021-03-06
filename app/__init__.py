from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)                    # it can use heroku database or database in books_db.sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///books_db.sqlite3'
app.config['SECRET_KEY'] = 'secret_stx_next_app'
db = SQLAlchemy(app)


bootstrap = Bootstrap()
bootstrap.init_app(app)

from app.models import Book, Author, Category

db.create_all()
db.session.commit()

from app import routes, models, errors
