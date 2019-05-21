from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///books_db.sqlite3'
app.config['SECRET_KEY'] = 'secret_stx_next_app'
db = SQLAlchemy(app)

from app.models import Book, Author, Category

db.create_all()
db.session.commit()

from app import routes, models, errors
