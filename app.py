from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os
from datetime import datetime

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


"""with app.app_context():
    db.create_all()"""