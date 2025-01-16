from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime
import os, requests

directory_library = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(directory_library, "data", "library.sqlite")}'
db.init_app(app)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handles both GET and POST requests for adding a new author.

    GET: Renders the form to add an author.
    POST: Processes the form data, creates a new Author record in the database,
    and displays a success or error message.
    """
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birthdate']
        date_of_death = request.form.get('date_of_death')  # Optional field

        # Convert the birth_date and date_of_death to Python date objects
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()

        # If date_of_death is empty, set it to None (it should be a date object or None)
        if date_of_death:
            date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d').date()
        else:
            date_of_death = None

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        try:
            db.session.add(new_author)
            db.session.commit()
            message = "Author added successfully!"
        except Exception as e:
            db.session.rollback()
            message = f"Error adding author: {str(e)}"

        return render_template('add_author.html', message=message)

    return render_template('add_author.html', message=None)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handles both GET and POST requests for adding a new book.

    GET: Renders the form to add a book with a dropdown to select an author.
    POST: Processes the form data, creates a new Book record in the database,
          and displays a success or error message.
    """
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author']  # Get the selected author ID

        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)

        try:
            db.session.add(new_book)
            db.session.commit()
            message = "Book added successfully!"
        except Exception as e:
            db.session.rollback()
            message = f"Error adding book: {str(e)}"

        return render_template('add_book.html', message=message, authors=Author.query.all())

    authors = Author.query.all()  # Fetch all authors to populate the dropdown
    return render_template('add_book.html', message=None, authors=authors)


@app.route('/')
def home():
    """
    Fetches all books from the database, queries Open Library API to get cover images
    for each book, and renders the home page with books and their covers.
    """
    search_query = request.args.get('search_query', '')
    sort_by = request.args.get('sort_by', 'title')  # Default to sorting by title

    if search_query:
        # Search books where title or author's name matches the search query
        books = Book.query.join(Author).filter(
            (Book.title.ilike(f'%{search_query}%')) |
            (Author.name.ilike(f'%{search_query}%'))
        ).all()
    else:
        # Sort books by title or author name
        if sort_by == 'author':
            books = Book.query.join(Author).order_by(Author.name).all()
        else:
            books = Book.query.order_by(Book.title).all()


    for book in books:
        # Query the Open Library API to get the cover image using the ISBN
        clean_isbn = ''.join([char for char in book.isbn if char.isdigit()])
        response = requests.get(f'https://covers.openlibrary.org/b/isbn/{clean_isbn}-L.jpg')

        if response.status_code == 200:
            book.cover_image_url = response.url
        else:
            book.cover_image_url = None

    return render_template('home.html', books=books)



"""with app.app_context():
    db.create_all()"""