from app import db


book_author_table = db.Table('books_authors',
                        db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                        db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


book_category_table = db.Table('books_categories',
                        db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                        db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    authors = db.relationship('Author',
                secondary=book_author_table)
    categories = db.relationship("Category",
                secondary=book_category_table)
    description = db.Column(db.String, nullable=False)


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, category_name):
        self.category_name = category_name
