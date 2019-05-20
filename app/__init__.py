from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db.sqlite3'
app.config['SECRET_KEY'] = 'secret_stx_next_app'
db = SQLAlchemy(app)


from app import routes, models, errors
