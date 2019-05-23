from flask import render_template, flash, redirect
from app import app, db
from app.forms import AddBookForm, AuthorFilter, CategoryFilter, ImportBookForm
from app.models import Book, Author, Category
from app.helpers import BookHelper
import requests


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def show_books():
    author_filter = AuthorFilter()
    category_filter = CategoryFilter()

    # filter by author
    if author_filter.validate_on_submit() and author_filter.author_name.data:
        flash('Author filter: "{}"'.format(author_filter.author_name.data), category='filter_on')
        rows = Book.query.filter(Book.authors.any(Author.name.like(
                                                '%{}%'.format(author_filter.author_name.data)))).all()
        books_exist = True
        return render_template('list.html',
                               books_exist=books_exist,
                               rows=rows,
                               title="List of books",
                               author_filter=author_filter,
                               category_filter=category_filter)

    # filter by category
    if category_filter.validate_on_submit() and category_filter.category_name.data:
        flash('Category filter: "{}"'.format(category_filter.category_name.data), category='filter_on')
        rows = Book.query.filter(Book.categories.any(Category.category_name.like(
                                                '%{}%'.format(category_filter.category_name.data)))).all()
        books_exist = True
        return render_template('list.html',
                               books_exist=books_exist,
                               rows=rows,
                               title="List of books",
                               author_filter=author_filter,
                               category_filter=category_filter)

    # table without filters
    rows = Book.query.all()
    if rows:
        books_exist = True          # visible table
    else:
        books_exist = False         # empty database -> invisible table
    return render_template('list.html',
                           books_exist=books_exist,
                           rows=rows,
                           title="List of books",
                           author_filter=author_filter,
                           category_filter=category_filter)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    helper = BookHelper()
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book()
        book.title = form.title.data
        book.description = form.description.data

        authors_list = form.authors.data.split(',')
        authors = map(str.strip, authors_list)
        for author in helper.add_items(Author, 'name', db, authors):
            book.authors.append(author)

        categories_list = form.categories.data.split(',')
        categories = map(str.strip, categories_list)
        for category in helper.add_items(Category, 'category_name', db, categories):
            book.categories.append(category)

        # do not add if book is already in database
        if helper.test_duplicate(Book, book):
            flash('Book "{}" is already in the database'.format(book.title), category='add_book_no')
        else:
            db.session.add(book)
            db.session.commit()
            flash('New book "{}" was successfully added to the database'.format(book.title), category='add_book_yes')
        return redirect('/list')

    # no validation or bad validation -> stay on site
    return render_template('add_book.html', title='Add book', form=form)


@app.route('/import_book', methods=['GET', 'POST'])
def import_book():
    helper = BookHelper()
    import_form = ImportBookForm()
    if import_form.validate_on_submit():
        url = "https://www.googleapis.com/books/v1/volumes?q=" + import_form.term.data
        json_data = requests.get(url).json()
        for item in json_data['items']:
            info = item['volumeInfo']      # all book tags are in volumeInfo
            book = Book()

            # there can be no 'title' tag in data
            try:
                book.title = helper.add_item(info['title'])
            except KeyError:
                book.title = helper.add_item()

            # there can be no 'description' tag in data
            try:
                book.description = helper.add_item(info['description'])
            except KeyError:
                book.description = helper.add_item()

            # there can be no 'authors' tag in data
            try:
                for author in helper.add_items(Author, 'name', db, info['authors']):
                    book.authors.append(author)
            except KeyError:
                book.authors.append(helper.add_items(Author, 'name', db))

            # there can be no 'categories' tag in data
            try:
                for category in helper.add_items(Category, 'category_name', db, info['categories']):
                    book.categories.append(category)
            except KeyError:
                book.categories.append(helper.add_items(Category, 'category_name', db))

            # do not add if book is already in database
            if helper.test_duplicate(Book, book):
                flash('Book "{}" is already in the database'.format(book.title), category='add_book_no')
            else:
                db.session.add(book)
                db.session.commit()
                flash('New book "{}" was successfully added to the database'.format(book.title),
                      category='add_book_yes')
        return redirect('/list')

    # no validation or bad validation -> stay on site
    return render_template('import_book.html', title='Import book', import_form=import_form)
