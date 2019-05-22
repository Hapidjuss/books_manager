from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# used in add_book.html
class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Author (example: author1, author2, author3))', validators=[DataRequired()])
    categories = StringField('Category (example: cat1, cat2, cat3)', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Book')


# used in list.html
class AuthorFilter(FlaskForm):
    author_name = StringField('author_name', render_kw={'placeholder': 'filter'})


class CategoryFilter(FlaskForm):
    category_name = StringField('category_name', render_kw={'placeholder': 'filter'})


# used in import_book.html
class ImportBookForm(FlaskForm):
    term = StringField('Search term', validators=[DataRequired()])
    submit = SubmitField('Import')
