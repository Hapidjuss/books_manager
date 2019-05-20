from flask import render_template, flash, redirect
from app import app, db
from app.forms import AddBookForm, AuthorFilter, CategoryFilter, ImportBookForm
from app.models import Book, Author, Category
import requests


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def show_books():
    author_filter = AuthorFilter()
    category_filter = CategoryFilter()

    ''' FILTER BY AUTHOR '''
    if author_filter.validate_on_submit() and author_filter.author_name.data:
        flash('Author filter: "{}"'.format(author_filter.author_name.data))
        rows = Book.query.filter(Book.authors.any(Author.name.like('%{}%'.format(author_filter.author_name.data)))).all()
        books_exist = True
        return render_template('list.html',
                               books_exist=books_exist,
                               rows=rows,
                               title="List of books",
                               author_filter=author_filter,
                               category_filter=category_filter)

    ''' FILTER BY CATEGORY '''
    if category_filter.validate_on_submit() and category_filter.category_name.data:
        flash('Category filter: "{}"'.format(category_filter.category_name.data))
        rows = Book.query.filter(Book.categories.any(Category.category_name.like('%{}%'.format(category_filter.category_name.data)))).all()
        books_exist = True
        return render_template('list.html',
                               books_exist=books_exist,
                               rows=rows,
                               title="List of books",
                               author_filter=author_filter,
                               category_filter=category_filter)

    ''' TABLE WITHOUT FILTERS '''
    rows = Book.query.all()
    if rows:
        books_exist = True
    else:
        books_exist = False
    return render_template('list.html',
                           books_exist=books_exist,
                           rows=rows,
                           title="List of books",
                           author_filter=author_filter,
                           category_filter=category_filter)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book()
        book.title = form.title.data
        book.description = form.description.data
        authors_list = form.authors.data.split(',')
        authors = map(str.lstrip, authors_list)
        for author in authors:
            new_author = Author.query.filter(Author.name==author).first()
            if new_author is None:
                new_author = Author(name=author)
                db.session.add(new_author)
            book.authors.append(new_author)
        categories_list = form.categories.data.split(',')
        categories = map(str.lstrip, categories_list)
        for category in categories:
            new_category = Category.query.filter(Category.category_name==category).first()
            if new_category is None:
                new_category = Category(category_name=category)
                db.session.add(new_category)
            book.categories.append(new_category)
        db.session.add(book)
        db.session.commit()
        flash('New book "{}" was successfully added to database'.format(form.title.data))
        return redirect('/list')
    return render_template('add_book.html', title='Add book', form=form)


@app.route('/import_book', methods=['GET', 'POST'])
def import_book():
    import_form = ImportBookForm()
    if import_form.validate_on_submit():
        url = "https://www.googleapis.com/books/v1/volumes?q=" + import_form.term.data
        json_data = requests.get(url).json()
        for item in json_data['items']:
            info = item['volumeInfo']
            book = Book()

            ''' TRY BOOK TITLE IN DATA '''
            try:
                book.title = info['title']
            except KeyError:
                book.title = '_unknown_'

            ''' TRY BOOK DESCRIPTION IN DATA '''
            try:
                book.description = info['description']
            except KeyError:
                book.description = '_unknown_'

            ''' TRY BOOK AUTHORS IN DATA '''
            try:
                for author in info['authors']:
                    new_author = Author.query.filter(Author.name == author).first()
                    if new_author is None:
                        new_author = Author(name=author)
                        db.session.add(new_author)
                    book.authors.append(new_author)
            except KeyError:
                author_name = '_unknown_'
                new_author = Author.query.filter(Author.name == author_name).first()
                if new_author is None:
                    new_author = Author(name=author_name)
                    db.session.add(new_author)
                book.authors.append(new_author)

            ''' TRY BOOK CATEGORIES IN DATA '''
            try:
                for category in info['categories']:
                    new_category = Category.query.filter(Category.category_name == category).first()
                    if new_category is None:
                        new_category = Category(category_name=category)
                        db.session.add(new_category)
                    book.categories.append(new_category)
            except KeyError:
                category_name = '_unknown_'
                new_category = Category.query.filter(Category.category_name == category_name).first()
                if new_category is None:
                    new_category = Category(category_name=category_name)
                    db.session.add(new_category)
                book.categories.append(new_category)

            db.session.add(book)
            db.session.commit()
            flash('New book "{}" was successfully added to database'.format(info['title']))
        return redirect('/list')
    return render_template('import_book.html', title='Import book', import_form=import_form)
