from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# used in add_book.html
class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    authors = StringField('Author', validators=[DataRequired()], render_kw={'placeholder': 'E.g. auth1, auth2, auth3'})
    categories = StringField('Category', validators=[DataRequired()],
                             render_kw={'placeholder': 'E.g. cat1, cat2, cat3'})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={'placeholder': 'Description'})
    submit = SubmitField('Add Book')


# used in import_book.html
class ImportBookForm(FlaskForm):
    term = StringField('Search term', validators=[DataRequired()], render_kw={'placeholder': 'Term'})
    submit = SubmitField('Import')
