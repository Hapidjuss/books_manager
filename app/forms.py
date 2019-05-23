from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# used in add_book.html
class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'title'})
    authors = StringField('Author', validators=[DataRequired()], render_kw={'placeholder': 'e.g. auth1, auth2, auth3'})
    categories = StringField('Category', validators=[DataRequired()],
                             render_kw={'placeholder': 'e.g. cat1, cat2, cat3'})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={'placeholder': 'description'})
    submit = SubmitField('Add Book')


# used in list.html
class AuthorFilter(FlaskForm):
    author_name = StringField('', render_kw={'placeholder': 'filter'})


class CategoryFilter(FlaskForm):
    category_name = StringField('', render_kw={'placeholder': 'filter'})


# used in import_book.html
class ImportBookForm(FlaskForm):
    term = StringField('Search term', validators=[DataRequired()], render_kw={'placeholder': 'term'})
    submit = SubmitField('Import')
